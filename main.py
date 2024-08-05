import nfc
import requests
from datetime import datetime

def read_nfc(tag):
    print("Tag detected")
    if tag.ndef:
        data = tag.ndef.records[0].text
        print("Data read:", data)
        
        data_list = [item.strip() for item in data.replace('\n', ',').split(',')]
        
        if len(data_list) >= 2:
            return data_list
        else:
            print("Data format not correct. Expected at least 2 values separated by comma.")
            return None
    else:
        print("No NDEF data found")
        return None

def handle_tag(tag):
    data = read_nfc(tag)
    if data:
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        nfc_data = {
            'name': data[0],
            'class': data[1] if len(data) > 1 else 'Unknown',
            'date': current_date,
            'time': current_time
        }
        
        response = requests.post('http://127.0.0.1:5000/api/save_attendance', json=nfc_data)
        if response.status_code == 200:
            print("Thank you, attendance has been received.")
        else:
            print("Failed to save attendance data")

def main():
    try:
        clf = nfc.ContactlessFrontend('usb')
        print("Waiting for NFC tag...")

        while True:
            clf.connect(rdwr={'on-connect': handle_tag})

    except Exception as e:
        print("An error occurred:", e)
    finally:
        clf.close()
        print("NFC reader connection closed")

if __name__ == "__main__":
    main()
