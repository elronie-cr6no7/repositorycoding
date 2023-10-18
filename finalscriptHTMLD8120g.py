# Import library requests
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# Ganti dengan path msedgedriver.exe yang sesuai
driver_path = r'C:\Program Files\Python\webdriver\edgedriver_win64\msedgedriver.exe'

# Ganti driver_path dengan None atau biarkan kosong
driver = webdriver.Edge()

# Fungsi untuk mengambil data numerik dari IRD Sumavision
def get_ird_data_realtime():
    try:
        # URL halaman IRD Sumavision yang berisi data numerik
        ird_url = "http://10.0.12.105/home.asp"

        # Kirim permintaan GET ke halaman IRD Sumavision
        response = requests.get(ird_url)

        # Pastikan respons sukses (kode status 200)
        if response.status_code == 200:
            # Menggunakan library BeautifulSoup untuk mengekstrak data
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Gantilah 'id_element' dengan id atau atribut lainnya yang sesuai dengan data numerik
            data_element = soup.find(id='id_element')
            
            if data_element:
                # Mengambil teks dari elemen
                data = data_element.text.strip()
                return data
            else:
                print("Elemen tidak ditemukan.")
                return None
        else:
            print("Gagal mengambil halaman IRD Sumavision.")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
