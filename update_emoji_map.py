
import sqlite3
import folium
from folium.plugins import MarkerCluster
import pandas as pd

def get_emoji(description):
    if not description:
        return '✅'
    description = description.lower()
    if 'mice' in description:
        return '🐁'
    if 'rat' in description:
        return '🐀'
    if 'roache' in description:
        return '🪳'
    if 'flies' in description:
        return '🪰'
    if 'harborage' in description or 'pests' in description:
        return '🏞️'
    if 'cold' in description and 'held' in description:
        return '🥶'
    if 'hot' in description and 'held' in description:
        return '🔥'
    if 'thawing' in description:
        return '🧊'
    if 'cooled' in description:
        return '🥵'
    if 'adulterated' in description or 'contaminated' in description:
        return '🤢'
    if 'sanitized' in description or 'washed' in description:
        return '🧼'
    if 'dishwashing' in description:
        return '🍽️'
    if 'personal cleanliness' in description:
        return '🧍'
    if 'wiping cloths' in description:
        return '🧻'
    if 'hand washing' in description:
        return '🤲'
    if 'bare hand' in description:
        return '🧤'
    if 'non-food contact surface' in description:
        return '🔩'
    if 'plumbing' in description or 'sewage' in description or 'anti-siphonage' in description:
        return '💧'
    if 'ventilation' in description:
        return '💨'
    if 'garbage' in description:
        return '🗑️'
    if 'toilet' in description:
        return '🚽'
    if 'certificate' in description:
        return '📝'
    if 'poster' in description:
        return '🖼️'
    if 'sign' in description:
        return '팻'
    if 'allergy' in description:
        return '🥜'
    if 'policy' in description:
        return '🚭'
    return '❓'

# Connect to the database
conn = sqlite3.connect('nyc_restaurant_inspections.db')
query = "SELECT dba, violation_description, latitude, longitude, inspection_date FROM inspections ORDER BY inspection_date DESC LIMIT 500"
df = pd.read_sql_query(query, conn)
conn.close()

# Create a map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles="CartoDB positron")

# Add markers to the map
marker_cluster = MarkerCluster().add_to(m)

for index, row in df.iterrows():
    if pd.notna(row['latitude']) and pd.notna(row['longitude']):
        emoji = get_emoji(row['violation_description'])
        popup_html = f"<b>{row['dba']}</b><br>{row['violation_description']}<br><small>{row['inspection_date']}</small>"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_html,
            icon=folium.DivIcon(html=f'<div style="font-size: 20pt; text-align: center;">{emoji}</div>', icon_size=(30,30), icon_anchor=(15,15))
        ).add_to(marker_cluster)

# Save the map
m.save('restaurant_inspections_emoji_map.html')
