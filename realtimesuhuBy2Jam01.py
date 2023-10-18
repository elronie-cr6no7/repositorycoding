import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
import gspread

# Path ke msedgedriver.exe
msedge_driver_path = r"C:\Program Files\Python\msEdgeDriver\edgedriver_win64\msedgedriver.exe"

# Membuat driver
options = EdgeOptions()
options.use_chromium = True
driver = Edge(executable_path=msedge_driver_path, options=options)

# Buka halaman web
url = "https://www.msn.com/id-id/cuaca/prakiraanperjam/in-Joglo%2C-Kembangan,Jakarta-Raya?loc=eyJsIjoiSm9nbG8sIEtlbMh%2C9ODQxMzA4NTk0IiwieSI6Ii02LjIxOTA9OTk5ODQ3NDEyMSJ9&weadegreetype=C&cvid=a0abf03ce11345458553ea0ddbff59f3&ocid=msedgntp"
driver.get(url)

# Tunggu hingga elemen muncul (timeout dalam 10 detik)
try:
    suhu_element = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/div[1]/div/div/div/ul/li/div/span[2]")

    # Dapatkan teks dari elemen
    suhu = suhu_element.text

    # Sekarang Anda memiliki data suhu yang dapat Anda gunakan
    print("Suhu saat ini di Joglo, Kembangan, Jakarta Barat:", suhu)
except Exception as e:
    print("Gagal menemukan elemen suhu:", str(e))

# Tutup browser
driver.quit()

# Menghubungkan ke Google Sheets
gc = gspread.service_account(filename="C:/Program Files/Python/json/projecthtmldata-428fc35ff324.json")

# Buka spreadsheet dengan URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit?usp=sharing"
sh = gc.open_by_url(spreadsheet_url)

# Pilih worksheet (lembar kerja) yang akan digunakan
worksheet = sh.get_worksheet(0)

# Menambahkan data suhu ke Google Sheets
worksheet.append_table(values=[time.strftime("%Y-%m-%d %H:%M:%S"), suhu])
