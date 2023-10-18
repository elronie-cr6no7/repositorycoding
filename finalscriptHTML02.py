import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver


# Fungsi untuk mengambil data dari IRD Sumavision-D8120
def get_ird_data(username, password, ird_ip):
    # Membuat sesi dan login
    session = requests.Session()
    login_url = f"http://{ird_ip}/login.asp"
    login_data = {"username": username, "password": password}
    session.post(login_url, data=login_data)

    # Mengakses halaman parameter
    parameter_url = f"http://{ird_ip}/home.asp"
    response = session.get(parameter_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Mencari elemen-elemen data-parameter
    signal_level_elem = soup.find("div", {"id": "signalLevel"})
    cnr_elem = soup.find("div", {"id": "cnr"})
    ber_elem = soup.find("div", {"id": "ber"})
    cnr_margin_elem = soup.find("div", {"id": "cnrMargin"})

    # Memeriksa apakah elemen-elemen ditemukan sebelum mencoba mengambil teks
    if signal_level_elem:
        signal_level = signal_level_elem.text
    else:
        signal_level = "Data not found"

    if cnr_elem:
        cnr = cnr_elem.text
    else:
        cnr = "Data not found"

    if ber_elem:
        ber = ber_elem.text
    else:
        ber = "Data not found"

    if cnr_margin_elem:
        cnr_margin = cnr_margin_elem.text
    else:
        cnr_margin = "Data not found"

    return signal_level, cnr, ber, cnr_margin


# Fungsi untuk mengambil data dari Encoder EMR-3.0
def get_encoder_data(username, password, encoder_ip):
    # Membuat sesi dan login
    session = requests.Session()
    login_url = f"http://{encoder_ip}/login.asp"
    login_data = {"username": username, "password": password}
    session.post(login_url, data=login_data)

    # Mengakses halaman parameter
    parameter_url = f"http://{encoder_ip}/home.asp"
    response = session.get(parameter_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Mencari elemen-elemen data-parameter
    total_bitrate_elem = soup.find("div", {"id": "totalBitrate"})
    signal_level_elem = soup.find("div", {"id": "signalLevel"})
    sn_elem = soup.find("div", {"id": "sn"})
    ber_elem = soup.find("div", {"id": "ber"})

    # Memeriksa apakah elemen-elemen ditemukan sebelum mencoba mengambil teks
    if total_bitrate_elem:
        total_bitrate = total_bitrate_elem.text
    else:
        total_bitrate = "Data not found"

    if signal_level_elem:
        signal_level = signal_level_elem.text
    else:
        signal_level = "Data not found"

    if sn_elem:
        sn = sn_elem.text
    else:
        sn = "Data not found"

    if ber_elem:
        ber = ber_elem.text
    else:
        ber = "Data not found"

    return total_bitrate, signal_level, sn, ber


# Fungsi untuk mengupdate data ke Google Spreadsheet
def update_google_sheet(username, password, ird_ip, encoder_ip, spreadsheet_url):
    # Mengambil data-parameter dari IRD dan Encoder
    ird_data = get_ird_data(username, password, ird_ip)
    encoder_data = get_encoder_data(username, password, encoder_ip)

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

    # Mengambil waktu saat ini
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # Menambahkan data ke Google Spreadsheet
    data = [current_time] + list(ird_data) + list(encoder_data)
    sheet.append_row(data)

# Fungsi untuk menampilkan pesan status
def print_status(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

# Main program
if __name__ == "__main__":
    username = "USERNAME_IRD_ENCODER"
    password = "PASSWORD_IRD_ENCODER"
    ird_ip = "10.0.12.105"
    encoder_ip = "10.0.12.110"
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit?usp=sharing"

    print_status("Program sedang berjalan...")

    # Mengambil dan menyimpan data secara otomatis tiap 2 jam
    while True:
        update_google_sheet(username, password, ird_ip, encoder_ip, spreadsheet_url)
        print_status("Data berhasil diperbarui ke Google Spreadsheet.")
        time.sleep(7200)  # Menunggu 2 jam sebelum mengambil data lagi

