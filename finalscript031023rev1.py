#scriptfullfinal

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time
import schedule

# Fungsi untuk mengambil data dari IRD
def get_ird_data(driver):
    driver.switch_to.window(driver.window_handles[0])  # Beralih ke tab pertama
    driver.find_element_by_link_text("Function").click()
    driver.find_element_by_link_text("DVB-S/S2 In1").click()
    driver.find_element_by_link_text("Monitor").click()

    # Mengambil data dari IRD
    signal_level = float(driver.find_element_by_id("signal_level").text)
    cnr = float(driver.find_element_by_id("cnr").text)
    ber = float(driver.find_element_by_id("ber").text)
    cnr_margin = float(driver.find_element_by_id("cnr_margin").text)

    return signal_level, cnr, ber, cnr_margin

# Fungsi untuk mengambil data dari Encoder
def get_encoder_data(driver):
    driver.switch_to.window(driver.window_handles[1])  # Beralih ke tab kedua
    driver.find_element_by_link_text("Cards").click()
    driver.find_element_by_link_text("card4-ch.DVBS2 Demod Card").click()
    driver.find_element_by_link_text("Status Info").click()

    # Mengambil data dari Encoder
    total_bitrate = float(driver.find_element_by_id("total_bitrate").text)
    encoder_signal_level = float(driver.find_element_by_id("encoder_signal_level").text)
    sn = float(driver.find_element_by_id("sn").text)
    encoder_ber = float(driver.find_element_by_id("encoder_ber").text)

    return total_bitrate, encoder_signal_level, sn, encoder_ber

# Fungsi untuk mengirim data ke Google Sheets
def send_data_to_sheets(data):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Program Files\\Python\\json\\client_secret_731550070748-08np5cofq3gt9j0iniptblqe05uj7bf8.apps.googleusercontent.com.json', scope)
    client = gspread.authorize(creds)

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit"
    worksheet = client.open_by_url(spreadsheet_url).worksheet("Sheet1")

    worksheet.append_row(data)

# Fungsi utama untuk menjalankan semua langkah
def main():
    chrome_driver_path = "C:\\Program Files\\Python\\ChromeDriver\\chromedriver-114.0.5735.90.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # Buka tab pertama
    ird_url = "http://10.0.12.105/frame_en.asp"
    driver.get(ird_url)

    # Buka tab kedua
    encoder_url = "http://10.0.12.110/en/theframe.asp#"
    driver.execute_script("window.open('" + encoder_url + "', '_blank')")

    # Ambil data dari IRD
    ird_data = get_ird_data(driver)

    # Ambil data dari Encoder
    encoder_data = get_encoder_data(driver)

    # Gabungkan data IRD dan Encoder
    all_data = ird_data + encoder_data

    # Kirim data ke Google Sheets
    send_data_to_sheets(all_data)

    driver.quit()

# Indikator bahwa script sedang berjalan dengan rentang 1 menit
while True:
    print("Script sedang berjalan...")
    time.sleep(60)  # Tunggu 1 menit

# Jadwal untuk menjalankan tugas setiap 2 jam
schedule.every(2).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

