import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# Ganti dengan path msedgedriver.exe yang sesuai
driver_path = r'C:\Program Files\Python\webdriver\edgedriver_win64\msedgedriver.exe'

# Inisialisasi WebDriver tanpa argumen executable_path
driver = webdriver.Edge()

# Fungsi untuk mengambil data dari IRD Sumavision-D8120
def get_ird_data(username, password, ird_ip):
    try:
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
        signal_level_elem = soup.find("td", {"id": "signalLevel"})
        cnr_elem = soup.find("td", {"id": "snr"})
        ber_elem = soup.find("td", {"id": "ber"})
        cnr_margin_elem = soup.find("td", {"id": "cnrMargin"})

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
    except Exception as e:
        print(f"Error saat mengambil data IRD: {e}")
        return None, None, None, None

# Fungsi untuk mengambil data dari Encoder EMR-3.0
def get_encoder_data(username, password, encoder_ip):
    try:
        # Membuka halaman login
        driver.get(f"http://{encoder_ip}/login.asp")

        # Mengisi username dan password
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)

        # Klik tombol login
        driver.find_element_by_name("Submit").click()

        # Klik link "Cards"
        driver.find_element_by_link_text("Cards").click()

        # Klik link "card4--4-ch.DVBS2 Demod Card"
        driver.find_element_by_link_text("card4--4-ch.DVBS2 Demod Card").click()

        # Klik tab "Status Info"
        driver.find_element_by_css_selector("li.tab_selected1[onclick='jump(4);']").click()

        # Tunggu beberapa detik agar halaman memuat data
        time.sleep(5)

        # Mengambil data dari tabel dengan XPath
        table = driver.find_element_by_xpath("//*[@id='table_info31']/tbody/tr[5]")

        # Mengambil teks dari sel dalam tabel
        total_bitrate = table.find_element_by_xpath("./td[1]").text

        return total_bitrate
    except Exception as e:
        print(f"Error saat mengambil data Encoder: {e}")
        return "Data not found"
    finally:
        # Menutup browser setelah selesai
        driver.quit()


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