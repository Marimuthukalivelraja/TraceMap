# TraceMAP 🌍  
**TraceMAP** is a Python-based tool that visualizes the journey of data packets as they traverse through various networks to reach a target destination. By leveraging traceroute and geolocation APIs, TraceMAP plots the path on an interactive world map, connecting each hop with lines for a cinematic hacker-movie-like effect.

---

## Features ✨  
- **Traceroute Integration**: Runs `traceroute` (or `tracert` on Windows) to capture the path packets take.  
- **IP Geolocation**: Fetches latitude and longitude of each IP hop using the IP-API.  
- **Interactive Map**: Displays the packet path on a world map using Plotly's `scatter_geo` module.  
- **Dynamic Visualization**: Draws lines between hops to visually connect the path.  
- **Cross-Platform Support**: Works on both Linux (traceroute) and Windows (tracert).  

---

## How It Works 🚀  

1. **Run Traceroute**  
   - The script executes the traceroute command to determine the path packets take to the target IP or domain.

2. **Extract IP Addresses**  
   - Parses the traceroute output to extract all IP addresses encountered during the journey.

3. **Fetch Geolocation Data**  
   - Uses [IP-API](http://ip-api.com/) to retrieve latitude and longitude for each IP address.

4. **Generate World Map**  
   - Uses Pandas and Plotly Express to create an interactive map displaying the hops and connections.


