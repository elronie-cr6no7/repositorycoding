import xml.etree.ElementTree as ET

# Membaca file XML
tree = ET.parse('rx1290i.xml')
root = tree.getroot()

# Temukan elemen yang mengandung parameter data Unit IRD RX1290
for node in root.findall(".//Node[@N='Device Info']"):
    device_info = node

# Mengambil semua parameter data Unit IRD RX1290
parameters = {}
for child in device_info:
    if 'N' in child.attrib and 'V' in child.attrib:
        parameters[child.attrib['N']] = child.attrib['V']

# Menampilkan parameter-parameter
for key, value in parameters.items():
    print(f"{key}: {value}")
