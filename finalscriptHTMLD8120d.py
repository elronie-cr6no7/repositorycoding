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

# Menunggu elemen dengan ID "signin_btn" muncul selama 10 detik
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signin_btn")))

# Fungsi untuk mengambil data dari IRD Sumavision-D8120
def get_ird_data():
    try:
        # Buka halaman awal IRD Sumavision
        driver.get('http://10.0.12.105/home.asp')

        # Sekarang mencoba menemukan elemen
        english_button = driver.find_element(By.ID, "signin_btn")
        english_button.click()

        # Isi formulir login
        username_input = driver.find_element_by_id('username')  # Ganti dengan ID input username
        password_input = driver.find_element_by_id('password')  # Ganti dengan ID input password
        sign_in_button = driver.find_element_by_id('signin_btn')  # Ganti dengan ID tombol Sign In

        username_input.send_keys('USERNAME_ANDA')
        password_input.send_keys('PASSWORD_ANDA')
        sign_in_button.click()

        # Klik menu Function
        function_link = driver.find_element_by_id('funcLink')
        function_link.click()

        # Klik menu DVB-S/S2 In 1
        dvb_in_1 = driver.find_element_by_id('Functions_10_span')
        dvb_in_1.click()

        # Klik menu Monitor
        monitor_link = driver.find_element_by_xpath("//li[contains(@class, 'middle_selected')]")
        monitor_link.click()

        # Mengambil data-parameter yang diinginkan
        total_bitrate = driver.find_element_by_id('totalBitrate').text
        signal_level = driver.find_element_by_id('signalLevel').text
        cnr = driver.find_element_by_id('snr').text
        ber = driver.find_element_by_id('ber').text
        cnr_margin = driver.find_element_by_id('cnrMargin').text

        # Menghapus satuan dari data
        total_bitrate = total_bitrate.replace('Mbps', '')
        signal_level = signal_level.replace('dBm', '')
        cnr = cnr.replace('dB', '')
        ber = ber.replace('<1.0e-7', '0')  # Mengganti nilai '<1.0e-7' menjadi '0'
        cnr_margin = cnr_margin.replace('dB', '')

        return total_bitrate, signal_level, cnr, ber, cnr_margin

    except Exception as e:
        print(f"Error saat mengambil data IRD: {e}")
        return None, None, None, None, None

# Fungsi untuk mengupdate data ke Google Spreadsheet
def update_google_sheet(spreadsheet_url):
    try:
        # Mengambil waktu saat ini
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Mengambil data dari IRD
        total_bitrate, signal_level, cnr, ber, cnr_margin = get_ird_data()

        # Mengautentikasi ke Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "C:\\Program Files\\Python\\json\\projecthtmldata-428fc35ff324.json",
            scope
        )
        client = gspread.authorize(creds)

        # Membuka spreadsheet
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.sheet1

        # Menambahkan data ke Google Spreadsheet
        data = [current_time, total_bitrate, signal_level, cnr, ber, cnr_margin]
        sheet.append_row(data)

        print("Data berhasil diperbarui ke Google Spreadsheet.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit?usp=sharing"

    # Mengambil dan menyimpan data secara otomatis tiap 2 jam
    while True:
        try:
            update_google_sheet(spreadsheet_url)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

        # Menunggu 2 jam sebelum mengambil data lagi
        time.sleep(7200)
