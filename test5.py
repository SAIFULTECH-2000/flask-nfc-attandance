import nfc
import pandas as pd
from datetime import datetime

def read_nfc(tag):
    print("Tag detected")
    if tag.ndef:
        # Ambil data dari tag NFC
        data = tag.ndef.records[0].text
        print("Data read:", data)
        
        # Pecahkan data berdasarkan koma atau baris baru
        data_list = [item.strip() for item in data.replace('\n', ',').split(',')]
        
        if len(data_list) >= 2:  # Pastikan data mengandungi sekurang-kurangnya dua elemen
            return data_list
        else:
            print("Data format not correct. Expected at least 2 values separated by comma.")
            return None
    else:
        print("No NDEF data found")
        return None

def main():
    try:
        # Sambungkan ke NFC reader
        clf = nfc.ContactlessFrontend('usb')
        print("Waiting for NFC tag...")
        
        # Fungsi untuk membaca NFC tag
        def on_connect(tag):
            data = read_nfc(tag)
            if data:
                # Dapatkan tarikh dan waktu semasa
                current_date = datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.now().strftime('%H:%M:%S')
                
                # Sediakan data untuk disimpan
                nfc_data = {
                    'NAMA': data[0],
                    'KELAS': data[1] if len(data) > 1 else 'Unknown',
                    'TARIKH': current_date,
                    'WAKTU MASUK': current_time
                }
                
                # Simpan data ke dalam DataFrame
                df = pd.DataFrame([nfc_data])
                print("DataFrame created:", df)
                
                # Simpan DataFrame ke dalam CSV
                df.to_csv('nfc_data.csv', index=False, mode='a', header=False)
                print("Data saved to nfc_data.csv")
        
        clf.connect(rdwr={'on-connect': on_connect})
        
        # Tutup sambungan NFC reader
        clf.close()
        print("NFC reader connection closed")

    except Exception as e:
        print("An error occurred:", e)

if _name_ == "_main_":
    main()