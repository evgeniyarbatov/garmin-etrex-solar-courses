from geopy.distance import geodesic

import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

START_TOLERANCE_METERS = 0.001

def format_gpx(gpx, distance):
  gpx_file = xml.dom.minidom.parseString(
    tostring(gpx, encoding="unicode")
  ).toprettyxml()

  distance = round(distance / 1000.0)

  return (distance, gpx_file)

def create_gpx():
  gpx = Element('gpx', {
      'creator': 'StravaGPX',
      'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
      'version': '1.1',
      'xmlns': 'http://www.topografix.com/GPX/1/1'
  })
  trk = SubElement(gpx, "trk")
  trkseg = SubElement(trk, "trkseg")
  return gpx, trkseg

def reverse_gpx(gpx):
    for track in gpx.tracks:
        for segment in track.segments:
            segment.points.reverse()
    return gpx

def find_closest_point(
  gpx,
  start_lat=None,
  start_lng=None,
):
  closest_point = None
  min_distance = float('inf')
  for track in gpx.tracks:
    for segment in track.segments:
      for point in segment.points:
        distance = geodesic((point.latitude, point.longitude), (start_lat, start_lng)).meters
        if distance < min_distance:
          min_distance = distance
          closest_point = point
  return str(closest_point.latitude), str(closest_point.longitude)

def split_gpx(
  gpx, 
  points_per_file=200,
  start_lat=None,
  start_lng=None,
):
  split_gpx_files = []
  distance = 0
  gpx_out, trkseg_out = create_gpx()

  route_started = True
  closest_lat, closest_lng = None, None
  if start_lat != None and start_lng != None:
    closest_lat, closest_lng = find_closest_point(gpx, start_lat, start_lng)
    route_started = False

  for track in gpx.tracks:
    for segment in track.segments:
      for count, point in enumerate(segment.points, start=1):
        lat, lng = str(point.latitude), str(point.longitude)

        if start_lat != None and start_lng != None:
          if lat == closest_lat and lng == closest_lng:
            route_started = True

        if not route_started:
          continue

        if count > 1:
           prev_lat, prev_lng = str(segment.points[count-2].latitude), str(segment.points[count-2].longitude)
           distance += geodesic((prev_lat, prev_lng), (lat, lng)).meters

        if count % points_per_file == 0:
          split_gpx_files.append(format_gpx(gpx_out, distance))
          gpx_out, trkseg_out = create_gpx()

        SubElement(trkseg_out, "trkpt", attrib={"lat": lat, "lon": lng})

  split_gpx_files.append(format_gpx(gpx_out, distance))

  return split_gpx_files