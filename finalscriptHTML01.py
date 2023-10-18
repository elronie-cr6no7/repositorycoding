import requests
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Variabel path ke file kredensial
CREDENTIALS_FILE = 'C:\\Program Files\\Python\\json\\client_secret_731550070748-08np5cofq3gt9j0iniptblqe05uj7bf8.apps.googleusercontent.com.json'

# URL perangkat Sumavision-D8120 dan Encoder EMR-3.0
sumavision_url = 'http://10.0.12.105/home.asp'
encoder_url = 'http://10.0.12.110/home.asp'

# Fungsi untuk mengambil data parameter dari perangkat
def get_device_data(url, params):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Jika permintaan HTTP gagal, raise exception
        soup = BeautifulSoup(response.text, 'html.parser')

        data = []
        for param in params:
            elem = soup.find('div', {'id': param})
            if elem:
                try:
                    data.append(float(elem.text))
                except (ValueError, AttributeError):
                    data.append(0.0)  # Nilai default jika tidak ada data atau kesalahan konversi
            else:
                data.append(0.0)  # Nilai default jika elemen tidak ditemukan

        return data
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data: {str(e)}")
        return [0.0] * len(params)  # Nilai default jika terjadi kesalahan

# Fungsi untuk menyimpan data ke Google Spreadsheet
def save_to_google_sheet(data):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        gc = gspread.authorize(credentials)

        # Buka Google Spreadsheet
        spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Mb8RxmRzeCdlEeZSZwPckZzp5qUfaQ1kicI7zbrk44s/edit')

        # Pilih lembar kerja yang sesuai
        worksheet = spreadsheet.worksheet('Sheet1')

        # Tambahkan data ke lembar kerja
        worksheet.append_row(data)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Spreadsheet: {str(e)}")

# Fungsi utama
def main():
    params_sumavision = ['signal_level', 'cnr', 'ber', 'cnr_margin']
    params_encoder = ['total_bitrate', 'signal_level', 'sn', 'ber']

    try:
        while True:
            print("Memulai pengambilan data...")

            # Ambil data dari perangkat Sumavision-D8120
            sumavision_data = get_device_data(sumavision_url, params_sumavision)

            # Ambil data dari perangkat Encoder EMR-3.0
            encoder_data = get_device_data(encoder_url, params_encoder)

            # Gabungkan data dari kedua perangkat
            all_data = sumavision_data + encoder_data

            # Simpan data ke Google Spreadsheet
            save_to_google_sheet(all_data)

            print("Pengambilan data selesai.")

            # Tunggu selama 2 jam sebelum mengambil data lagi
            time.sleep(7200)
    except KeyboardInterrupt:
        print("Program dihentikan secara manual.")

if __name__ == '__main__':
    main()
