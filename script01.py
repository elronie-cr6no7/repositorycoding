import time
import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Fungsi untuk mengambil data dari IRD Sumavision-D8120
def get_ird_data(driver):
    driver.switch_to.window(driver.window_handles[0])  # Beralih ke tab IRD
    driver.get("http://10.0.12.105/frame_en.asp")
    
    # Masukkan langkah-langkah untuk mengambil data dari IRD
    # Contoh: driver.find_element_by_id('element_id').text

    # Ubah data teks menjadi numerik jika diperlukan
    # Contoh: data = float(data)

    return data

# Fungsi untuk mengambil data dari Encoder EMR-3.0
def get_encoder_data(driver):
    driver.switch_to.window(driver.window_handles[1])  # Beralih ke tab Encoder
    driver.get("http://10.0.12.110/en/theframe.asp#")

    # Masukkan langkah-langkah untuk mengambil data dari Encoder
    # Contoh: driver.find_element_by_id('element_id').text

    # Ubah data teks menjadi numerik jika diperlukan
    # Contoh: data = float(data)

    return data

# Fungsi untuk menyimpan data ke Google Spreadsheet
def save_to_google_sheets(data):
    gc = gspread.service_account(filename='path_ke_google_sheets_credentials.json')
    sh = gc.open("StorageDataEquipment")
    worksheet = sh.get_worksheet(0)

    # Ubah data menjadi list yang sesuai dengan baris di Spreadsheet
    # Contoh: row_data = [data1, data2, data3, ...]

    worksheet.append_row(row_data)

# Fungsi utama
def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jalankan Chrome dalam mode headless (tanpa GUI)
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\Python\\ChromeDriver.exe", options=chrome_options)

    # Masukkan langkah-langkah untuk login ke Google dan akses spreadsheet

    for _ in range(12):  # Lakukan ini selama 12 kali (2 jam sekali)
        ird_data = get_ird_data(driver)
        encoder_data = get_encoder_data(driver)
        
        # Simpan data ke Google Spreadsheet
        save_to_google_sheets([ird_data, encoder_data])

        # Tunggu selama 2 jam sebelum mengambil data lagi
        time.sleep(7200)

    driver.quit()

if __name__ == "__main__":
    main()
