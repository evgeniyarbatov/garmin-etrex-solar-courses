import gpxpy
import base64
from io import BytesIO

import streamlit as st

from utils import reverse_gpx, split_gpx

def create_download_link(gpx, distance):
    b64 = base64.b64encode(gpx.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{distance}km.gpx">{distance}km.gpx</a>'
    return href

st.title('GPX Editor')

uploaded_file = st.file_uploader("GPX file", type=["gpx"])
points_per_file = st.selectbox("How many points per file?", [200, 500, 1000, 10000], index=0)

if uploaded_file is not None:
  gpx_file = uploaded_file.read()
  gpx = gpxpy.parse(gpx_file)

  reverse_direction_choice = st.radio(
      "Reverse direction?",
      ("Yes", "No"),
      index=1,
  )
  if reverse_direction_choice == "Yes":
    gpx = reverse_gpx(gpx)
    st.success("GPX file reversed")
  else:
    st.info("GPX file NOT reversed")

  gpx_segments = split_gpx(gpx, points_per_file)

  for distance, gpx_segment in gpx_segments:
    st.markdown(create_download_link(gpx_segment, distance), unsafe_allow_html=True)