"""
MacIDS Network Monitor for macOS

This module uses Scapy to capture and analyze network traffic on macOS.
"""

import os
import sys
import threading
import time
import socket
import logging
import ipaddress
import subprocess
import geoip2.database
import geoip2.errors
import psutil
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS
from collections import defaultdict, deque
import traceback
import pandas as pd
import numpy as np
from datetime import datetime
import queue
import json
import csv
import dns.resolver
import dns.reversename
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('macids_traffic.log')
    ]
)
logger = logging.getLogger(__name__)

# Import GeoIP database downloader
try:
    from .download_geoip_db import download_geolite2_db
except ImportError:
    # Define a minimal version if the module is not available
    def download_geolite2_db():
        print("GeoIP database downloader not available. Using default paths.")
        return "geoip_db/GeoLite2-City.mmdb", "geoip_db/GeoLite2-Country.mmdb"

class SystemNetworkMonitor:
    """
    A system-wide network traffic monitor using Scapy to capture packets
    across the entire macOS system.
    """
    
    def __init__(self, interface=None, port=0):
        self.interface = interface  # If None, will capture on all interfaces
        self.port = port
        self.stop_flag = threading.Event()
        self.packet_queue = queue.Queue()
        self.session_tracker = defaultdict(dict)
        self.traffic_stats = defaultdict(int)
        self.dns_cache = {}  # Cache for DNS lookups
        self.app_traffic = defaultdict(lambda: {'sent_bytes': 0, 'recv_bytes': 0, 'connections': set()})
        self.geo_cache = {}  # Cache for GeoIP lookups
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('macids_traffic.log'),
                logging.StreamHandler()
            ]
        )
        
        # Initialize statistics
        self.stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'protocols': defaultdict(int),
            'ports': defaultdict(int),
            'connections': defaultdict(int),
            'sessions': defaultdict(dict),
            'applications': defaultdict(lambda: {'bytes': 0, 'connections': set(), 'domains': set()}),
            'domains': defaultdict(int),
            'countries': defaultdict(int),  # Track packets by country
            'geo_connections': []  # Store geolocation data for connections
        }
        
        # Initialize GeoIP database
        self._init_geoip()
        
        # Initialize DNS cache
        self.dns_cache = {}
        self.domain_queue = deque(maxlen=100)
        self.dns_thread = None
        
        # Initialize process cache
        self.process_cache = {}
        
        # Initialize analysis thread
        self.analysis_thread = None
        
        # Get available interfaces
        self.interfaces = self._get_interfaces()
        if self.interface is None and self.interfaces:
            # Use the first non-loopback interface by default
            for iface in self.interfaces:
                if not iface.startswith('lo'):
                    self.interface = iface
                    break
            
            # If no valid interface found, use the first one
            if self.interface is None and self.interfaces:
                self.interface = self.interfaces[0]
                
        logger.info(f"Using interface: {self.interface}")
    
    def _get_interfaces(self):
        """Get available network interfaces on macOS"""
        try:
            # Use scapy's get_if_list function
            interfaces = scapy.get_if_list()
            return interfaces
        except Exception as e:
            logger.error(f"Error getting interfaces: {e}")
            # Fallback to using ifconfig if scapy fails
            try:
                output = subprocess.check_output(['ifconfig', '-l']).decode('utf-8')
                interfaces = output.strip().split()
                return interfaces
            except Exception as e:
                logger.error(f"Error getting interfaces using ifconfig: {e}")
                return ['en0']  # Default to en0 if all else fails
    
    def _init_geoip(self):
        """Initialize GeoIP database for IP location lookup"""
        self.geoip_city = None
        self.geoip_country = None
        
        try:
            # Download GeoIP database if needed
            city_db_path, country_db_path = download_geolite2_db()
            
            # Verify database files exist
            if not os.path.exists(city_db_path) or not os.path.exists(country_db_path):
                logging.warning("GeoIP database files not found at expected paths")
                logging.info("Using fallback for GeoIP lookups - location data will be limited")
                return
            
            # Open GeoIP readers
            self.geoip_city = geoip2.database.Reader(city_db_path)
            self.geoip_country = geoip2.database.Reader(country_db_path)
            logging.info(f"Initialized GeoIP database from {city_db_path}")
        except Exception as e:
            logging.error(f"Failed to initialize GeoIP database: {e}")
            logging.info("Using fallback for GeoIP lookups - location data will be limited")
    
    def get_ip_location(self, ip):
        """Get location information for an IP address"""
        if ip in self.geo_cache:
            return self.geo_cache[ip]
        
        # Skip private IP addresses
        try:
            if ipaddress.ip_address(ip).is_private:
                self.geo_cache[ip] = {
                    'country': 'Private',
                    'country_code': 'XX',
                    'city': 'Private Network',
                    'latitude': 0,
                    'longitude': 0
                }
                return self.geo_cache[ip]
        except:
            # If IP parsing fails, return unknown
            self.geo_cache[ip] = {
                'country': 'Unknown',
                'country_code': 'XX',
                'city': 'Unknown',
                'latitude': 0,
                'longitude': 0
            }
            return self.geo_cache[ip]
        
        # Lookup location
        try:
            if self.geoip_city and hasattr(self.geoip_city, 'city'):
                response = self.geoip_city.city(ip)
                location = {
                    'country': response.country.name or 'Unknown',
                    'country_code': response.country.iso_code or 'XX',
                    'city': response.city.name or 'Unknown',
                    'latitude': response.location.latitude or 0,
                    'longitude': response.location.longitude or 0
                }
                self.geo_cache[ip] = location
                return location
            else:
                # Return placeholder if GeoIP database is not available
                self.geo_cache[ip] = {
                    'country': 'Unknown',
                    'country_code': 'XX',
                    'city': 'Unknown',
                    'latitude': 0,
                    'longitude': 0
                }
                return self.geo_cache[ip]
        except Exception as e:
            # If lookup fails, return unknown
            logging.debug(f"GeoIP lookup failed for {ip}: {e}")
            self.geo_cache[ip] = {
                'country': 'Unknown',
                'country_code': 'XX',
                'city': 'Unknown',
                'latitude': 0,
                'longitude': 0
            }
            return self.geo_cache[ip]
    
    def start_capture(self):
        """Start system-wide traffic capture"""
        try:
            # Start packet capture thread
            self.capture_thread = threading.Thread(target=self._capture_packets)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            # Start analysis thread
            self.analysis_thread = threading.Thread(target=self._analyze_packets)
            self.analysis_thread.daemon = True
            self.analysis_thread.start()

            # Start statistics thread
            self.stats_thread = threading.Thread(target=self._print_stats)
            self.stats_thread.daemon = True
            self.stats_thread.start()

            # Start DNS resolution thread
            self.dns_thread = threading.Thread(target=self._resolve_domains)
            self.dns_thread.daemon = True 
            self.dns_thread.start()

            logging.info("Started system-wide network monitoring")
            return True

        except Exception as e:
            logging.error(f"Failed to start capture: {e}")
            traceback.print_exc()
            return False
    
    def _capture_packets(self):
        """Capture network packets using Scapy"""
        try:
            # Start sniffing packets in a non-blocking mode - packets will be processed in _packet_callback
            logging.info(f"Starting packet capture on interface {self.interface}")
            
            # Filter string - empty string means capture everything
            filter_str = ""
            if self.port > 0:
                filter_str = f"port {self.port}"
            
            # Start packet sniffing
            scapy.sniff(
                iface=self.interface,
                prn=self._packet_callback,
                filter=filter_str,
                store=False,
                stop_filter=lambda x: self.stop_flag.is_set()
            )
            
        except Exception as e:
            if not self.stop_flag.is_set():
                logging.error(f"Capture error: {e}")
                traceback.print_exc()
    
    def _packet_callback(self, packet):
        """Process captured packets and put them in the queue"""
        try:
            # Put packet in queue for processing
            self.packet_queue.put(packet)
        except Exception as e:
            logging.error(f"Error in packet callback: {e}")
    
    def _analyze_packets(self):
        """Analyze packets from the queue"""
        while not self.stop_flag.is_set():
            try:
                # Get packet from queue
                packet = self.packet_queue.get(timeout=1)
                
                # Process the packet
                try:
                    # Make sure it's an IP packet
                    if packet.haslayer(IP):
                        # Get process information
                        process_info = self._get_process_by_connection(packet)
                        
                        # Analyze the packet details
                        self._analyze_packet_details(packet, process_info)
                    
                except Exception as e:
                    logging.debug(f"Error analyzing packet: {e}")
                    continue
                    
            except queue.Empty:
                continue
            except Exception as e:
                if not self.stop_flag.is_set():
                    logging.error(f"Error in packet analysis: {e}")
                    continue

    def _get_process_by_connection(self, packet):
        """Identify the process that owns a network connection on macOS"""
        try:
            # Extract connection details
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Extract ports if TCP or UDP
                src_port = 0
                dst_port = 0
                proto = 'other'
                
                if packet.haslayer(TCP):
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    proto = 'tcp'
                elif packet.haslayer(UDP):
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                    proto = 'udp'
                
                # Create connection key
                key = f"{src_ip}:{src_port}-{dst_ip}:{dst_port}-{proto}"
                
                # Check if process is already cached
                if key in self.session_tracker and 'pid' in self.session_tracker[key]:
                    return self.session_tracker[key]
                
                # Check if any application has this connection
                for app_name, app_data in self.stats['applications'].items():
                    if key in app_data.get('connections', set()):
                        if 'pid' in app_data:
                            try:
                                # Get process details
                                proc = psutil.Process(app_data['pid'])
                                process_info = {
                                    'pid': app_data['pid'],
                                    'name': app_name,
                                    'path': proc.exe() if hasattr(proc, 'exe') else '',
                                    'create_time': proc.create_time() if hasattr(proc, 'create_time') else 0
                                }
                                # Cache process info
                                self.session_tracker[key] = process_info
                                return process_info
                            except Exception:
                                pass
                
                # Initialize the session tracker entry if it doesn't exist
                if key not in self.session_tracker:
                    self.session_tracker[key] = {'pid': 0, 'name': 'Unknown', 'path': '', 'create_time': 0}
                
                # Try to find the process using lsof on macOS
                try:
                    # For outgoing connections
                    if src_ip not in ('127.0.0.1', '::1') and src_port > 0:
                        # Use lsof to find process using this port
                        cmd = f"lsof -i {proto}:{src_port} -n -P"
                        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
                        
                        for line in output.splitlines()[1:]:  # Skip header
                            parts = line.split()
                            if len(parts) >= 9:
                                process_name = parts[0]
                                pid = int(parts[1])
                                
                                try:
                                    proc = psutil.Process(pid)
                                    process_info = {
                                        'pid': pid,
                                        'name': process_name,
                                        'path': proc.exe() if hasattr(proc, 'exe') else '',
                                        'create_time': proc.create_time() if hasattr(proc, 'create_time') else 0
                                    }
                                    # Cache process info
                                    self.session_tracker[key] = process_info
                                    return process_info
                                except Exception:
                                    pass
                    
                    # For incoming connections
                    if dst_ip not in ('127.0.0.1', '::1') and dst_port > 0:
                        # Use lsof to find process using this port
                        cmd = f"lsof -i {proto}:{dst_port} -n -P"
                        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
                        
                        for line in output.splitlines()[1:]:  # Skip header
                            parts = line.split()
                            if len(parts) >= 9:
                                process_name = parts[0]
                                pid = int(parts[1])
                                
                                try:
                                    proc = psutil.Process(pid)
                                    process_info = {
                                        'pid': pid,
                                        'name': process_name,
                                        'path': proc.exe() if hasattr(proc, 'exe') else '',
                                        'create_time': proc.create_time() if hasattr(proc, 'create_time') else 0
                                    }
                                    # Cache process info
                                    self.session_tracker[key] = process_info
                                    return process_info
                                except Exception:
                                    pass
                except Exception:
                    pass
                
                # Fallback to checking all connections with psutil
                try:
                    for proc in psutil.process_iter(['pid', 'name', 'exe', 'connections']):
                        for conn in proc.info.get('connections', []):
                            if conn.type == getattr(socket, f'SOCK_{proto.upper()}'):
                                # Check for local port match
                                if conn.laddr and len(conn.laddr) >= 2 and conn.laddr[1] == src_port:
                                    process_info = {
                                        'pid': proc.info['pid'],
                                        'name': proc.info['name'],
                                        'path': proc.info.get('exe', ''),
                                        'create_time': proc.create_time() if hasattr(proc, 'create_time') else 0
                                    }
                                    # Cache process info
                                    self.session_tracker[key] = process_info
                                    return process_info
                except Exception:
                    pass
                
                # If we get here, no process was found
                return self.session_tracker[key]
                
        except Exception as e:
            logging.debug(f"Error getting process: {e}")
            return {'pid': 0, 'name': 'Unknown', 'path': '', 'create_time': 0}
    
    def _update_process_list(self):
        """Update the list of all running processes with network activity on macOS"""
        try:
            # Update every 5 seconds at most to avoid performance issues
            current_time = time.time()
            if hasattr(self, '_last_process_update') and current_time - self._last_process_update < 5:
                return
            
            self._last_process_update = current_time
            
            # Track already added processes to avoid duplicates
            added_processes = set()
            
            # Use psutil to get network connections with processes
            try:
                # Track already added processes to avoid duplicates
                for proc in psutil.process_iter(['pid', 'name', 'exe', 'connections']):
                    try:
                        # Skip if already processed
                        if proc.pid in added_processes:
                            continue
                            
                        connections = proc.connections(kind='inet')
                        if connections:
                            added_processes.add(proc.pid)
                            app_name = proc.name()
                            
                            # Add to application stats if not already there
                            if app_name not in self.stats['applications']:
                                self.stats['applications'][app_name] = {
                                    'bytes': 0,
                                    'connections': set(),
                                    'domains': set(),
                                    'pid': proc.pid
                                }
                            
                            # Add connections to the app
                            for conn in connections:
                                if conn.type == socket.SOCK_STREAM:
                                    proto = 'tcp'
                                elif conn.type == socket.SOCK_DGRAM:
                                    proto = 'udp'
                                else:
                                    continue
                                
                                if conn.laddr and len(conn.laddr) >= 2 and conn.raddr and len(conn.raddr) >= 2:
                                    # Create connection key
                                    conn_key = f"{conn.laddr[0]}:{conn.laddr[1]}-{conn.raddr[0]}:{conn.raddr[1]}-{proto}"
                                    self.stats['applications'][app_name]['connections'].add(conn_key)
                                    
                                    # Add process to session tracker for future packets
                                    self.session_tracker[conn_key] = {
                                        'pid': proc.pid,
                                        'name': app_name,
                                        'path': proc.exe() if hasattr(proc, 'exe') else '',
                                        'create_time': proc.create_time() if hasattr(proc, 'create_time') else 0
                                    }
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                    except Exception as e:
                        logging.debug(f"Error processing process {proc.pid}: {e}")
            except Exception as e:
                logging.debug(f"Error listing processes: {e}")
            
            # Use lsof as a fallback to find processes with network activity
            if not added_processes:
                try:
                    output = subprocess.check_output("lsof -i -n -P", shell=True).decode('utf-8')
                    for line in output.splitlines()[1:]:  # Skip header
                        parts = line.split()
                        if len(parts) >= 9:
                            try:
                                process_name = parts[0]
                                pid = int(parts[1])
                                
                                # Skip if already processed
                                if pid in added_processes:
                                    continue
                                    
                                added_processes.add(pid)
                                
                                # Add to application stats if not already there
                                if process_name not in self.stats['applications']:
                                    self.stats['applications'][process_name] = {
                                        'bytes': 0,
                                        'connections': set(),
                                        'domains': set(),
                                        'pid': pid
                                    }
                            except:
                                pass
                except Exception as e:
                    logging.debug(f"Error using lsof: {e}")
            
            # Log the number of applications found
            logging.debug(f"Found {len(self.stats['applications'])} applications with network activity")
            
        except Exception as e:
            logging.debug(f"Error updating process list: {e}")
    
    def _analyze_packet_details(self, packet, process_info):
        """Analyze packet details and update statistics"""
        try:
            # Update the process list periodically
            self._update_process_list()
            
            # Make sure it's an IP packet
            if not packet.haslayer(IP):
                return
                
            # Get IP addresses
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            
            # Skip localhost traffic
            if ip_src == '127.0.0.1' and ip_dst == '127.0.0.1':
                return
            
            # Update basic statistics
            packet_len = len(packet)
            self.stats['total_packets'] += 1
            self.stats['total_bytes'] += packet_len
            
            # Check protocol
            proto = 'Other'
            src_port = 0
            dst_port = 0
            domain = None
            
            # Parse TCP packet
            if packet.haslayer(TCP):
                proto = 'TCP'
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                
                # Check if this is HTTP/HTTPS
                if src_port == 80 or dst_port == 80:
                    proto = 'HTTP'
                elif src_port == 443 or dst_port == 443:
                    proto = 'HTTPS'
                
                # Try to extract HTTP host
                try:
                    if proto == 'HTTP' and raw(packet).find(b'Host: ') != -1:
                        raw_data = raw(packet)
                        host_idx = raw_data.find(b'Host: ')
                        if host_idx != -1:
                            end_idx = raw_data.find(b'\r\n', host_idx)
                            if end_idx != -1:
                                domain = raw_data[host_idx + 6:end_idx].decode()
                                self.stats['domains'][domain] = self.stats['domains'].get(domain, 0) + 1
                                
                                # Associate domain with application
                                if process_info and process_info.get('name') != 'Unknown':
                                    app_name = process_info.get('name')
                                    if app_name in self.stats['applications']:
                                        self.stats['applications'][app_name]['domains'].add(domain)
                except:
                    pass
                
            # Parse UDP packet
            elif packet.haslayer(UDP):
                proto = 'UDP'
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                
                # Check if this is DNS
                if src_port == 53 or dst_port == 53:
                    proto = 'DNS'
                    # Try to extract domain from DNS query
                    try:
                        if packet.haslayer(DNS) and packet[DNS].qr == 0:  # It's a query
                            if packet[DNS].qd:
                                query_domain = packet[DNS].qd.qname.decode()
                                if query_domain:
                                    domain = query_domain.rstrip('.')
                                    self.stats['domains'][domain] = self.stats['domains'].get(domain, 0) + 1
                                    
                                    # Associate domain with application
                                    if process_info and process_info.get('name') != 'Unknown':
                                        app_name = process_info.get('name')
                                        if app_name in self.stats['applications']:
                                            self.stats['applications'][app_name]['domains'].add(domain)
                    except:
                        pass
            
            # Update protocol counter
            self.stats['protocols'][proto] += 1
            
            # Update port statistics (skip port 0)
            if src_port > 0:
                self.stats['ports'][src_port] = self.stats['ports'].get(src_port, 0) + 1
            if dst_port > 0:
                self.stats['ports'][dst_port] = self.stats['ports'].get(dst_port, 0) + 1
            
            # Update session information
            session_key = f"{ip_src}:{src_port}-{ip_dst}:{dst_port}-{proto}"
            if session_key not in self.stats['sessions']:
                self.stats['sessions'][session_key] = {
                    'src_ip': ip_src,
                    'dst_ip': ip_dst,
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'protocol': proto,
                    'bytes': 0,
                    'packets': 0,
                    'start_time': time.time(),
                    'last_time': time.time(),
                    'process': process_info.get('name', 'Unknown'),
                    'pid': process_info.get('pid', 0)
                }
                
                # Add domain if available
                if domain:
                    self.stats['sessions'][session_key]['domain'] = domain
            
            # Update session counters
            self.stats['sessions'][session_key]['bytes'] += packet_len
            self.stats['sessions'][session_key]['packets'] += 1
            self.stats['sessions'][session_key]['last_time'] = time.time()
            
            # Update application information
            app_name = process_info.get('name', 'Unknown')
            if app_name != 'Unknown':
                # Get or create application entry
                if app_name not in self.stats['applications']:
                    self.stats['applications'][app_name] = {
                        'bytes': 0,
                        'connections': set(),
                        'domains': set(),
                        'pid': process_info.get('pid', 0)
                    }
                
                # Update application traffic
                self.stats['applications'][app_name]['bytes'] += packet_len
                self.stats['applications'][app_name]['connections'].add(session_key)
                
                # Add domain if available
                if domain:
                    self.stats['applications'][app_name]['domains'].add(domain)
            
            # Add connection to geolocation data if it's not a private IP
            try:
                if not ipaddress.ip_address(ip_dst).is_private:
                    # Get destination location
                    dst_location = self.get_ip_location(ip_dst)
                    self.stats['countries'][dst_location['country']] = self.stats['countries'].get(dst_location['country'], 0) + 1
                    
                    # Add unique connection to geo_connections list if it's not already there
                    connection = {
                        'src_ip': ip_src,
                        'dst_ip': ip_dst,
                        'dst_country': dst_location['country'],
                        'dst_city': dst_location['city'],
                        'latitude': dst_location['latitude'],
                        'longitude': dst_location['longitude'],
                        'protocol': proto,
                        'port': dst_port,
                        'process': process_info.get('name', 'Unknown'),
                        'bytes': packet_len
                    }
                    
                    # Check if this connection already exists
                    exists = False
                    for conn in self.stats['geo_connections']:
                        if (conn['src_ip'] == ip_src and conn['dst_ip'] == ip_dst and
                            conn['protocol'] == proto and conn['port'] == dst_port):
                            # Update existing connection
                            conn['bytes'] += packet_len
                            exists = True
                            break
                    
                    # Add new connection
                    if not exists:
                        self.stats['geo_connections'].append(connection)
                        # Keep list manageable size
                        if len(self.stats['geo_connections']) > 100:
                            self.stats['geo_connections'].pop(0)
            except Exception as e:
                logging.debug(f"Error updating geolocation data: {e}")
        
        except Exception as e:
            logging.debug(f"Error analyzing packet details: {e}")
            traceback.print_exc()
    
    def _resolve_domains(self):
        """Resolve domain names for IP addresses"""
        while not self.stop_flag.is_set():
            try:
                # Sleep to avoid excessive CPU usage
                time.sleep(5)
                
                # Process up to 10 sessions
                count = 0
                for session_key, session in list(self.stats['sessions'].items()):
                    # Limit updates per cycle
                    if count >= 10:
                        break
                    
                    # Only resolve non-private IPs
                    try:
                        dst_ip = session['dst_ip']
                        if (not ipaddress.ip_address(dst_ip).is_private and
                            'domain' not in session):
                            
                            # Check cache first
                            if dst_ip in self.dns_cache:
                                session['domain'] = self.dns_cache[dst_ip]
                            else:
                                # Try to resolve domain
                                try:
                                    addr = dns.reversename.from_address(dst_ip)
                                    domain = str(dns.resolver.resolve(addr, "PTR")[0])
                                    self.dns_cache[dst_ip] = domain
                                    session['domain'] = domain
                                    count += 1
                                except:
                                    self.dns_cache[dst_ip] = "Unknown"
                                    session['domain'] = "Unknown"
                    except:
                        pass
            except Exception as e:
                logging.debug(f"Error resolving domains: {e}")
    
    def _print_stats(self):
        """Print statistics periodically for debugging"""
        last_time = time.time()
        last_packets = 0
        last_bytes = 0
        
        while not self.stop_flag.is_set():
            try:
                # Wait a bit
                time.sleep(5)
                
                # Calculate rates
                now = time.time()
                elapsed = now - last_time
                
                if elapsed > 0:
                    # Calculate rates
                    packets_rate = (self.stats['total_packets'] - last_packets) / elapsed
                    bytes_rate = (self.stats['total_bytes'] - last_bytes) / elapsed
                    
                    # Log statistics
                    logging.info(f"Traffic: {packets_rate:.1f} packets/sec, {bytes_rate/1024:.1f} KB/sec")
                    
                    # Top 5 active sessions
                    active_sessions = sorted(
                        self.stats['sessions'].values(),
                        key=lambda x: x['last_time'],
                        reverse=True
                    )[:5]
                    
                    for session in active_sessions:
                        logging.info(f"Session: {session['src_ip']}:{session['src_port']} -> "
                                    f"{session['dst_ip']}:{session['dst_port']} ({session['protocol']}) - "
                                    f"{session['bytes']/1024:.1f} KB - "
                                    f"Process: {session['process']}")
                    
                    # Clean up old sessions
                    self._cleanup_old_sessions()
                    
                    # Update previous values
                    last_time = now
                    last_packets = self.stats['total_packets']
                    last_bytes = self.stats['total_bytes']
            
            except Exception as e:
                logging.error(f"Error printing stats: {e}")
    
    def _cleanup_old_sessions(self):
        """Clean up old sessions to prevent memory growth"""
        # Remove sessions older than 5 minutes
        now = time.time()
        cutoff = now - 300  # 5 minutes
        
        for key in list(self.stats['sessions'].keys()):
            if self.stats['sessions'][key]['last_time'] < cutoff:
                del self.stats['sessions'][key]

    def stop_capture(self):
        """Stop capturing packets"""
        try:
            # Set stop flag to stop all threads
            self.stop_flag.set()
            
            # Wait for threads to finish
            if hasattr(self, 'capture_thread') and self.capture_thread:
                self.capture_thread.join(timeout=1.0)
            if hasattr(self, 'analysis_thread') and self.analysis_thread:
                self.analysis_thread.join(timeout=1.0)
            if hasattr(self, 'stats_thread') and self.stats_thread:
                self.stats_thread.join(timeout=1.0)
            if hasattr(self, 'dns_thread') and self.dns_thread:
                self.dns_thread.join(timeout=1.0)
            
            # Close GeoIP readers
            if hasattr(self, 'geoip_city') and self.geoip_city:
                self.geoip_city.close()
            if hasattr(self, 'geoip_country') and self.geoip_country:
                self.geoip_country.close()
            
            return True
        except Exception as e:
            logging.error(f"Error stopping capture: {e}")
            return False
    
    def get_statistics(self):
        """Get current statistics"""
        return self.stats
    
    def get_application_traffic(self):
        """Get application traffic statistics"""
        return self.app_traffic
    
    def get_geo_data(self):
        """Get geolocation data"""
        return {
            'connections': self.stats['geo_connections'],
            'countries': self.stats['countries']
        } 