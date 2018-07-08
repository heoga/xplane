import os
import simplekml

XPLANE = "F:\\Games\\X-Plane 11"

def read_data(xplane):
    data_file = os.path.join(xplane, 'Data.txt')
    data = []
    with open(data_file) as h:
        lines = [x.strip() for x in h.readlines()]
    for line in lines:
        if not line:
            continue
        fields = [y for y in [x.strip() for x in line.split('|')] if y]
        if ',' in line:
            # header line.
            headers = fields
            continue
        for i in range(0, len(fields)):
            fields[i] = float(fields[i])
        entry = dict(zip(headers, fields))
        data.append(entry)
    return data

def data_to_kml(data, name):
    kml_points = []
    for entry in data:
        kml_points.append(
            (entry['__lon,__deg'], entry['__lat,__deg'], entry['__alt,ftmsl'] * 0.3048)
        )
    kml = simplekml.Kml(open=1)
    line = kml.newlinestring(name="Track")
    line.coords = kml_points
    line.linestyle.color = 'FFCC00CC'
    line.linestyle.width = 5  # Make the text twice as big
    kml.save(os.path.join(name, '{}.kml'.format(name)))
    
if __name__ == "__main__":
    data = read_data(XPLANE)
    name = input('Enter a name for the output KML: ')
    os.makedirs(name, exist_ok=True)
    data_to_kml(data, name)
    