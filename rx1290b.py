import xml.etree.ElementTree as ET
import time

# Fungsi untuk membaca dan mengurai data dari file XML
def parse_xml_file(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"Error parsing XML file: {str(e)}")
        return None

# Fungsi untuk menampilkan data-parameter tertentu
def display_data_parameters(xml_root):
    if xml_root is not None:
        for node in xml_root.findall(".//Node[@N='SAT']"):
            print("Data dari Node SAT:")
            for child in node:
                if child.tag in ["Choice", "Str", "Int32"]:
                    param_name = child.get("N")
                    param_value = child.get("V")
                    print(f"{param_name}: {param_value}")

if __name__ == "__main__":
    xml_file = r"C:\Program Files\Python\rx1290ii.xml"  # Ganti dengan path ke file XML yang sesuai

    while True:
        xml_root = parse_xml_file(xml_file)
        if xml_root:
            display_data_parameters(xml_root)
        else:
            print("Gagal mengurai XML. Pastikan file XML tersedia.")
        
        time.sleep(30)  # Menunggu 30 detik sebelum membaca lagi (real-time)

