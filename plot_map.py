#!/usr/bin/env python3

import sqlite3
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from datetime import datetime

# Database setup
DATABASE_URL = "nyc_restaurant_inspections.db"

def plot_inspections_map():
    """
    Plots restaurant inspections from 2025 on a map.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Query to select the last 3000 inspections in 2025 with a violation description,
    # sorted by inspection_date.
    query = "SELECT latitude, longitude, dba, violation_description, inspection_date FROM inspections WHERE strftime('%Y', inspection_date) = '2025' AND violation_description IS NOT NULL AND violation_description != '' ORDER BY inspection_date DESC LIMIT 3000"
    
    try:
        cursor.execute(query)
        inspections = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Error querying the database: {e}")
        print("Please ensure the data has been fetched and stored correctly.")
        conn.close()
        return
    finally:
        conn.close()

    if not inspections:
        print("No inspections with descriptions found for the year 2025.")
        return

    # Create a map centered on New York City
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

    # Create a MarkerCluster object
    marker_cluster = MarkerCluster().add_to(nyc_map)

    # Add markers for each inspection to the cluster
    for lat, lon, dba, violation_description, inspection_date in inspections:
        if lat and lon:
            # Ensure lat and lon are floats
            try:
                lat = float(lat)
                lon = float(lon)
                inspection_date_obj = datetime.strptime(inspection_date.split(' ')[0], '%Y-%m-%d')
                formatted_date = inspection_date_obj.strftime('%B %d, %Y')
                popup_text = f"<b>{dba}</b><br>{violation_description}<br><small>{formatted_date}</small>"
                folium.Marker(
                    [lat, lon],
                    popup=popup_text,
                    icon=DivIcon(
                        icon_size=(30,30),
                        icon_anchor=(15,15),
                        html=f'<div style="font-size: 20pt; text-align: center;">🐟</div>',
                    )
                ).add_to(marker_cluster)
            except (ValueError, TypeError):
                print(f"Skipping invalid coordinates for {dba}: lat={lat}, lon={lon}")


    # Save the map to an HTML file
    map_file = "restaurant_inspections_emoji_map.html"
    nyc_map.save(map_file)
    print(f"Map with emoji markers saved to {map_file}")

if __name__ == "__main__":
    plot_inspections_map()
