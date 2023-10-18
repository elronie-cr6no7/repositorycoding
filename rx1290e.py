#rx1290e akan di gabung ke rx1290d
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Fungsi untuk mengonversi nilai teks ke bilangan real
def parse_as_float(value):
    try:
        return float(value)
    except ValueError:
        return None

# Fungsi untuk menampilkan data-parameter angka numerik sesuai persyaratan
def display_real_values(xml_root):
    if xml_root is not None:
        for node in xml_root.findall(".//Node[@N='SAT']"):
            print("Data dari Node SAT:")
            for child in node:
                if child.get("N") in ["Signal Level", "Post Viterbi BER", "C/N margin", "C/N"]:
                    param_name = child.get("N")
                    param_value = child.get("V")
                    numeric_value = parse_as_float(param_value)
                    if numeric_value is not None:
                        print(f"{param_name}: {numeric_value}")

if __name__ == "__main__":
    xml_file = r"C:\Program Files\Python\rx1290ii.xml"  # Ganti dengan path ke file XML yang sesuai

    # Path ke msedgedriver.exe
    driver_path = r'C:\Program Files\Python\webdriver\edgedriver_win64\msedgedriver.exe'

    # Inisialisasi driver Microsoft Edge
    driver = webdriver.Edge(executable_path=driver_path)

    # Buka halaman web dengan alamat IP lokal
    ip_address = "192.168.1.105"
    url = f"http://{ip_address}"  # Ganti dengan URL yang sesuai
    driver.get(url)

    while True:
        xml_root = parse_xml_file(xml_file)
        if xml_root:
            display_real_values(xml_root)
        else:
            print("Gagal mengurai XML. Pastikan file XML tersedia.")

        # Mengambil nilai dari halaman web menggunakan JavaScript path
        signal_level_element = driver.execute_script('return document.querySelector("body > table:nth-child(2) > tbody > tr > td.nSelected > p").innerText')
        post_viterbi_ber_element = driver.execute_script('return document.querySelector("body > table.nav > tbody > tr > td > form > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2) > div > div > table > tbody").innerText')
        c_n_element = driver.find_element(By.XPATH, '//*[@id="C/N_name"]').text
        c_n_margin_element = driver.find_element(By.XPATH, '//*[@id="C/N margin_name"]').text

        # Menampilkan nilai dari elemen-elemen yang diambil
        print(f"Signal Level: {signal_level_element}")
        print(f"Post Viterbi BER: {post_viterbi_ber_element}")
        print(f"C/N: {c_n_element}")
        print(f"C/N Margin: {c_n_margin_element}")

        time.sleep(30)  # Menunggu 30 detik sebelum membaca lagi (real-time)
