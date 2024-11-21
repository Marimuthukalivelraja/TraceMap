import subprocess
import re
import requests
import pandas as pd
import plotly.express as px
import os
import json
from concurrent.futures import ThreadPoolExecutor

CACHE_FILE = "ip_cache.json"  # File to store cached IP location data

def load_cache():
    """
    Loads cached IP location data from a file.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_cache(cache):
    """
    Saves cached IP location data to a file.
    """
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

def run_traceroute(target):
    """
    Runs the traceroute (or tracert on Windows) command and captures the output.
    """
    command = ["tracert", target] if subprocess.os.name == 'nt' else ["traceroute", target]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"Error running traceroute: {e}")
        return None

def extract_ips(traceroute_output):
    """
    Extracts IP addresses from traceroute output using regex.
    """
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return list(dict.fromkeys(ip_pattern.findall(traceroute_output)))  # Removes duplicates while preserving order

def get_location_data(ip):
    """
    Fetches latitude and longitude for a given IP using IP-API.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return ip, data['lat'], data['lon']
        else:
            return ip, None, None
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return ip, None, None

def get_location_data_with_cache(ip, cache):
    """
    Fetches IP location data using cache to reduce API calls.
    """
    if ip in cache:
        return ip, cache[ip][0], cache[ip][1]
    ip, lat, lon = get_location_data(ip)
    if lat is not None and lon is not None:
        cache[ip] = [lat, lon]
    return ip, lat, lon

def create_map(ip_data):
    """
    Creates a scatter-geo map using Plotly Express to visualize the traceroute path.
    """
    df = pd.DataFrame(ip_data, columns=["IP", "Latitude", "Longitude"])
    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="IP",
        title="TraceMAP - Visualizing Traceroute Paths",
        template="plotly_dark"
    )
    # Add lines connecting the points
    for i in range(len(df) - 1):
        fig.add_trace(px.line_geo(lat=df.iloc[i:i+2]['Latitude'], lon=df.iloc[i:i+2]['Longitude']).data[0])
    fig.show()

def main():
    target = input("Enter the domain or IP to trace (e.g., 'google.com'): ")
    print("Running traceroute...")
    traceroute_output = run_traceroute(target)
    if not traceroute_output:
        print("Traceroute failed. Please try again.")
        return
    
    print("Extracting IPs from traceroute...")
    ips = extract_ips(traceroute_output)
    if not ips:
        print("No IPs found in the traceroute output.")
        return
    
    print("Fetching location data for IPs...")
    cache = load_cache()
    ip_data = []

    # Use multithreading to speed up location data fetching
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda ip: get_location_data_with_cache(ip, cache), ips))

    ip_data = [result for result in results if result[1] is not None and result[2] is not None]
    save_cache(cache)  # Save updated cache to file
    
    if not ip_data:
        print("Failed to fetch location data for the IPs.")
        return
    
    print("Creating map...")
    create_map(ip_data)

if __name__ == "__main__":
    main()
