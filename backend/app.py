import gpxpy
import base64
from io import BytesIO

import streamlit as st

from utils import reverse_gpx, split_gpx

def create_download_link(gpx, index):
    b64 = base64.b64encode(gpx.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="split_{index}.gpx">split_{index}.gpx</a>'
    return href

st.title('GPX Editor for Garmin Etrex Solar')

uploaded_file = st.file_uploader("GPX file", type=["gpx"])
points_per_file = st.selectbox("How many points per file?", [200, 500, 1000, 2000], index=0)

if uploaded_file is not None:
  gpx_file = uploaded_file.read()
  gpx = gpxpy.parse(gpx_file)

  st.write("Do you want to reverse the GPX file?")
  col1, col2, = st.columns(2)
  with col1:
    if st.button('Yes'):
      gpx = reverse_gpx(gpx)
      st.success("GPX file reversed")
  with col2:
      if st.button('No'):
        st.info("GPX file NOT reversed")

  split_files = split_gpx(gpx, points_per_file)
  for i, split_gpx in enumerate(split_files):
    st.markdown(create_download_link(split_gpx, i), unsafe_allow_html=True)