from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fungsi untuk login ke IRD Sumavision (tanpa otomatis login)
def login_to_ird():
    driver = webdriver.Edge()  # Tidak perlu menyebutkan executable_path di sini
    driver.get(login_url)
    
    # Anda perlu melakukan login secara manual di browser yang terbuka
    input("Silakan masukkan username dan password secara manual di browser, lalu tekan Enter setelah selesai...")

    # Setelah login manual, tunggu hingga halaman yang Anda inginkan dimuat
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "funcLink"))
    )

    return driver

# Fungsi untuk mengambil data dari IRD Sumavision
def get_ird_data(driver):
    try:
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
        while True:
            # Mengambil waktu saat ini
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # Login ke IRD Sumavision (tanpa otomatis login)
            driver = login_to_ird()

            # Mengambil data dari IRD
            total_bitrate, signal_level, cnr, ber, cnr_margin = get_ird_data(driver)

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

            print(f"Data berhasil diperbarui ke Google Spreadsheet pada {current_time}")

            # Menunggu 2 jam sebelum memeriksa kembali waktu
            time.sleep(7200)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    login_url = 'http://10.0.12.105/home.asp'
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit?usp=sharing"

    try:
        update_google_sheet(spreadsheet_url)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
