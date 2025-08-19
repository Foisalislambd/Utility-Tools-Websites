"""Network utility functions"""
import ipaddress
import socket
import struct
from typing import Dict, Any, List
import re

def ip_calculator(ip: str, operation: str = "info") -> Dict[str, Any]:
    """Calculate IP address information"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        
        if operation == "info":
            return {
                "ip": str(ip_obj),
                "version": ip_obj.version,
                "is_private": ip_obj.is_private,
                "is_global": ip_obj.is_global,
                "is_multicast": ip_obj.is_multicast,
                "is_loopback": ip_obj.is_loopback,
                "is_link_local": ip_obj.is_link_local,
                "compressed": str(ip_obj) if ip_obj.version == 6 else None,
                "exploded": ip_obj.exploded if ip_obj.version == 6 else None,
                "binary": format(int(ip_obj), f'0{ip_obj.max_prefixlen}b'),
                "decimal": int(ip_obj)
            }
        
        elif operation == "reverse":
            # Reverse DNS lookup
            try:
                hostname = socket.gethostbyaddr(str(ip_obj))[0]
                return {"ip": str(ip_obj), "hostname": hostname, "success": True}
            except socket.herror:
                return {"ip": str(ip_obj), "hostname": "Not found", "success": False}
        
    except ValueError as e:
        return {"error": str(e)}

def subnet_calculator(network: str) -> Dict[str, Any]:
    """Calculate subnet information"""
    try:
        net = ipaddress.ip_network(network, strict=False)
        
        # Calculate subnet info
        network_address = str(net.network_address)
        broadcast_address = str(net.broadcast_address) if net.version == 4 else "N/A (IPv6)"
        netmask = str(net.netmask)
        prefix_length = net.prefixlen
        
        # Host information
        total_addresses = net.num_addresses
        usable_hosts = total_addresses - 2 if net.version == 4 else total_addresses
        
        # First and last usable IPs
        hosts = list(net.hosts())
        first_host = str(hosts[0]) if hosts else "N/A"
        last_host = str(hosts[-1]) if hosts else "N/A"
        
        # Wildcard mask (for IPv4)
        wildcard = None
        if net.version == 4:
            wildcard_int = (2 ** (32 - prefix_length)) - 1
            wildcard = str(ipaddress.IPv4Address(wildcard_int))
        
        return {
            "network": str(net),
            "network_address": network_address,
            "broadcast_address": broadcast_address,
            "netmask": netmask,
            "wildcard_mask": wildcard,
            "prefix_length": prefix_length,
            "total_addresses": total_addresses,
            "usable_hosts": usable_hosts,
            "first_host": first_host,
            "last_host": last_host,
            "ip_version": net.version,
            "is_private": net.is_private
        }
    
    except ValueError as e:
        return {"error": str(e)}

def cidr_calculator(ip: str, cidr: int) -> Dict[str, Any]:
    """Calculate CIDR block information"""
    try:
        network = f"{ip}/{cidr}"
        return subnet_calculator(network)
    except Exception as e:
        return {"error": str(e)}

def mac_lookup(mac: str) -> Dict[str, Any]:
    """Lookup MAC address vendor (basic implementation)"""
    # Clean MAC address
    mac = re.sub(r'[^0-9a-fA-F]', '', mac.upper())
    
    if len(mac) != 12:
        return {"error": "Invalid MAC address format"}
    
    # Format MAC address
    formatted_mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
    
    # Get OUI (first 3 bytes)
    oui = mac[:6]
    
    # Basic vendor database (in production, use a real OUI database)
    vendor_db = {
        "000000": "Xerox Corporation",
        "001122": "Cimsys Inc",
        "00155D": "Microsoft Corporation",
        "001B63": "Apple Inc.",
        "0050C2": "IEEE Registration Authority",
        "080027": "PCS Systemtechnik GmbH",
        "525400": "QEMU Virtual NIC"
    }
    
    vendor = vendor_db.get(oui, "Unknown Vendor")
    
    return {
        "mac_address": formatted_mac,
        "oui": oui,
        "vendor": vendor,
        "is_local": mac[1] in '26AE',  # Check if locally administered
        "is_multicast": int(mac[1], 16) & 1 == 1
    }

def port_checker(host: str, port: int, timeout: int = 5) -> Dict[str, Any]:
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        is_open = result == 0
        
        # Get service name if possible
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown"
        
        return {
            "host": host,
            "port": port,
            "is_open": is_open,
            "service": service,
            "timeout": timeout
        }
    
    except Exception as e:
        return {"error": str(e)}

def dns_propagation(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """Check DNS propagation across different servers"""
    dns_servers = [
        {"name": "Google", "ip": "8.8.8.8"},
        {"name": "Cloudflare", "ip": "1.1.1.1"},
        {"name": "OpenDNS", "ip": "208.67.222.222"},
        {"name": "Quad9", "ip": "9.9.9.9"}
    ]
    
    results = []
    
    for server in dns_servers:
        try:
            # This is a simplified implementation
            # In production, you'd use a proper DNS library
            import subprocess
            
            cmd = f"nslookup -type={record_type} {domain} {server['ip']}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse the output (simplified)
                output = result.stdout
                records = []
                if record_type == "A":
                    records = re.findall(r'Address: (\d+\.\d+\.\d+\.\d+)', output)
                
                results.append({
                    "server": server["name"],
                    "server_ip": server["ip"],
                    "records": records,
                    "status": "success" if records else "no_records"
                })
            else:
                results.append({
                    "server": server["name"],
                    "server_ip": server["ip"],
                    "records": [],
                    "status": "error"
                })
        
        except Exception:
            results.append({
                "server": server["name"],
                "server_ip": server["ip"],
                "records": [],
                "status": "timeout"
            })
    
    # Check consistency
    all_records = [set(r["records"]) for r in results if r["records"]]
    is_consistent = len(set(frozenset(records) for records in all_records)) <= 1 if all_records else False
    
    return {
        "domain": domain,
        "record_type": record_type,
        "results": results,
        "is_consistent": is_consistent,
        "propagated": len([r for r in results if r["status"] == "success"]) >= 3
    }

def bandwidth_tester() -> Dict[str, Any]:
    """Basic bandwidth estimation (mock implementation)"""
    import time
    import random
    
    # Simulate bandwidth test
    start_time = time.time()
    
    # Mock download test
    download_speeds = []
    for _ in range(5):
        # Simulate varying speeds
        speed = random.uniform(50, 100)  # Mbps
        download_speeds.append(speed)
        time.sleep(0.1)  # Simulate test duration
    
    # Mock upload test
    upload_speeds = []
    for _ in range(3):
        speed = random.uniform(10, 50)  # Mbps
        upload_speeds.append(speed)
        time.sleep(0.1)
    
    end_time = time.time()
    
    avg_download = sum(download_speeds) / len(download_speeds)
    avg_upload = sum(upload_speeds) / len(upload_speeds)
    
    # Mock ping test
    ping = random.uniform(10, 50)  # ms
    
    return {
        "download_speed": {
            "average": round(avg_download, 2),
            "max": round(max(download_speeds), 2),
            "min": round(min(download_speeds), 2),
            "unit": "Mbps"
        },
        "upload_speed": {
            "average": round(avg_upload, 2),
            "max": round(max(upload_speeds), 2),
            "min": round(min(upload_speeds), 2),
            "unit": "Mbps"
        },
        "ping": round(ping, 2),
        "test_duration": round(end_time - start_time, 2),
        "disclaimer": "This is a mock test for demonstration purposes"
    }

def network_scanner(network: str, port_range: str = "22,80,443") -> Dict[str, Any]:
    """Scan network for active hosts (basic implementation)"""
    try:
        net = ipaddress.ip_network(network, strict=False)
        ports = [int(p.strip()) for p in port_range.split(',')]
        
        active_hosts = []
        
        # Limit scan to first 10 hosts for demo
        host_count = 0
        for host in net.hosts():
            if host_count >= 10:
                break
            
            host_info = {
                "ip": str(host),
                "hostname": None,
                "open_ports": []
            }
            
            # Try to get hostname
            try:
                hostname = socket.gethostbyaddr(str(host))[0]
                host_info["hostname"] = hostname
            except:
                pass
            
            # Check ports
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((str(host), port))
                    if result == 0:
                        host_info["open_ports"].append(port)
                    sock.close()
                except:
                    pass
            
            # Only include hosts with open ports or hostname
            if host_info["open_ports"] or host_info["hostname"]:
                active_hosts.append(host_info)
            
            host_count += 1
        
        return {
            "network": str(net),
            "scanned_ports": ports,
            "active_hosts": active_hosts,
            "total_scanned": host_count,
            "active_count": len(active_hosts)
        }
    
    except Exception as e:
        return {"error": str(e)}

def email_validator(email: str) -> Dict[str, Any]:
    """Validate email address format and domain"""
    # Basic email regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    is_valid_format = bool(re.match(email_pattern, email))
    
    if not is_valid_format:
        return {
            "email": email,
            "is_valid": False,
            "format_valid": False,
            "domain_valid": None,
            "mx_record": None
        }
    
    # Extract domain
    domain = email.split('@')[1]
    
    # Check domain format
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid_domain = bool(re.match(domain_pattern, domain))
    
    # Check MX record (simplified)
    has_mx = False
    try:
        import subprocess
        result = subprocess.run(['nslookup', '-type=MX', domain], 
                              capture_output=True, text=True, timeout=5)
        has_mx = 'mail exchanger' in result.stdout.lower()
    except:
        has_mx = None
    
    return {
        "email": email,
        "is_valid": is_valid_format and is_valid_domain,
        "format_valid": is_valid_format,
        "domain": domain,
        "domain_valid": is_valid_domain,
        "mx_record": has_mx,
        "local_part": email.split('@')[0],
        "length": len(email)
    }