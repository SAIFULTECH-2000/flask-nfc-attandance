import nfc

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
        clf = nfc.ContactlessFrontend('pcsc')
        print("Waiting for NFC tag...")
        
        # Fungsi untuk membaca NFC tag
        def on_connect(tag):
            data = read_nfc(tag)
            if data:
                print("Data read from NFC tag:", data)
        
        clf.connect(rdwr={'on-connect': on_connect})
        
        # Tutup sambungan NFC reader
        clf.close()
        print("NFC reader connection closed")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
