import os
import platform
import psutil
import shutil
from collections import defaultdict
import heapq

def get_system_info():
    info = {}
    
    # System info
    info["System"] = {
        "OS": platform.system(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
    }
    
    # CPU info
    info["CPU"] = {
        "Processor": platform.processor(),
        "Physical cores": psutil.cpu_count(logical=False),
        "Logical cores": psutil.cpu_count(logical=True),
        "Current usage": f"{psutil.cpu_percent()}%"
    }
    
    # Memory info
    memory = psutil.virtual_memory()
    info["Memory"] = {
        "Total": f"{memory.total / (1024**3):.2f} GB",
        "Available": f"{memory.available / (1024**3):.2f} GB",
        "Used": f"{memory.used / (1024**3):.2f} GB ({memory.percent}%)"
    }
    
    # Disk info
    disk = psutil.disk_usage('/')
    info["Disk"] = {
        "Total": f"{disk.total / (1024**3):.2f} GB",
        "Used": f"{disk.used / (1024**3):.2f} GB ({disk.percent}%)",
        "Free": f"{disk.free / (1024**3):.2f} GB"
    }
    
    # Network info
    info["Network"] = {}
    for iface, stats in psutil.net_if_addrs().items():
        for addr in stats:
            if addr.family == 2:  # IPv4
                info["Network"][iface] = addr.address
                break
    
    return info

def analyze_disk_usage(path=None):
    if not path:
        path = os.getcwd()
    
    if not os.path.exists(path):
        raise Exception(f"Path does not exist: {path}")
    
    total_usage = 0
    file_sizes = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                total_usage += file_size
                heapq.heappush(file_sizes, (-file_size, file_path))
            except (OSError, PermissionError):
                pass
    
    top_10 = []
    for _ in range(min(10, len(file_sizes))):
        if file_sizes:
            size, path = heapq.heappop(file_sizes)
            size = -size  # Convert back to positive
            size_str = format_size(size)
            top_10.append((path, size_str))
    
    return top_10

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB" 