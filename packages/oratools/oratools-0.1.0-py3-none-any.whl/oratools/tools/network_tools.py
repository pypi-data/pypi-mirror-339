import time
import socket
import subprocess
import sys
import requests
import dns.resolver
import re

def check_website_status(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response_time = time.time() - start_time
        
        return response.status_code, response_time
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to check website: {str(e)}")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code != 200:
            raise Exception(f"API returned status code {response.status_code}")
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get IP: {str(e)}")

def ping_host(host, count=4):
    try:
        param = '-n' if 'win' in sys.platform.lower() else '-c'
        command = ['ping', param, str(count), host]
        
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        
        if result.returncode == 0:
            return result.stdout.splitlines()
        else:
            return [f"Failed to ping {host}: {result.stderr}"]
    except Exception as e:
        raise Exception(f"Failed to ping host: {str(e)}")

def port_scan(host, port_range=None):
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy"
    }
    
    ports_to_scan = []
    if port_range:
        try:
            start, end = map(int, port_range.split('-'))
            ports_to_scan = range(start, end + 1)
        except:
            raise Exception("Invalid port range format. Use start-end (e.g., 1-100)")
    else:
        ports_to_scan = common_ports.keys()
    
    open_ports = []
    socket.setdefaulttimeout(0.5)
    
    for port in ports_to_scan:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((host, port))
        if result == 0:
            service = common_ports.get(port, "Unknown")
            open_ports.append((port, service))
        s.close()
    
    return open_ports

def lookup_dns(domain, record_type="A"):
    try:
        record_type = record_type.upper()
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return [] 