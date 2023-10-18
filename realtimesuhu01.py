import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Path ke msedgedriver.exe
msedge_driver_path = r"C:\Program Files\Python\msEdgeDriver\edgedriver_win64\msedgedriver.exe"

# Membuat driver
driver = webdriver.Edge(executable_path=msedge_driver_path)

# Buka halaman web
url = "https://www.msn.com/id-id/cuaca/prakiraanperjam/in-Joglo%2C-Kembangan,Jakarta-Raya?loc=eyJsIjoiSm9nbG8sIEtlbMh%2C9ODQxMzA4NTk0IiwieSI6Ii02LjIxOTA9OTk5ODQ3NDEyMSJ9&weadegreetype=C&cvid=a0abf03ce11345458553ea0ddbff59f3&ocid=msedgntp"
driver.get(url)

# Tunggu beberapa detik agar halaman sepenuhnya dimuat
time.sleep(5)

# Temukan elemen yang sesuai dengan XPath
suhu_element = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div[1]/ul/li/div/span[2]")

# Dapatkan teks dari elemen
suhu = suhu_element.text

# Sekarang Anda memiliki data suhu yang dapat Anda gunakan
print("Suhu saat ini di Joglo, Kembangan, Jakarta Barat:", suhu)

# Tutup browser
driver.quit()
