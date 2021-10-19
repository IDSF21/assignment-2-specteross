# Citations:
# [1] Streamlit cheatsheet to learn and code this application 
#     https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
# [2] This demo app helped me understand how to build the map view in Part 2, and I borrowed the below map function from it
#     https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py

import streamlit as st
import pydeck as pdk

from constants import LONGITUDE, LATITUDE

def map(data, lat, lon, zoom=11):  # \cite{[2]}
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=[LONGITUDE, LATITUDE],
                auto_highlight=True, 
                radius=40,
                elevation_scale=3,
                # elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ], 
        tooltip = {
            'html': 'Number of Accidents: {elevationValue}',
            'style': {
                'color': 'white'
            }
        }
    )
)