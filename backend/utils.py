import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

def format_gpx(gpx):
  gpx_file = xml.dom.minidom.parseString(
    tostring(gpx, encoding="unicode")
  ).toprettyxml()
  return gpx_file

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

def split_gpx(gpx, points_per_file=200):
  split_gpx_files = []
  gpx_out, trkseg_out = create_gpx()

  for track in gpx.tracks:
    for segment in track.segments:
      for count, point in enumerate(segment.points, start=1):
        if count % points_per_file == 0:
          split_gpx_files.append(format_gpx(gpx_out))

          gpx_out, trkseg_out = create_gpx()

        lat, lng = str(point.latitude), str(point.longitude)
        SubElement(trkseg_out, "trkpt", attrib={"lat": lat, "lon": lng})

  split_gpx_files.append(format_gpx(gpx_out))

  return split_gpx_files