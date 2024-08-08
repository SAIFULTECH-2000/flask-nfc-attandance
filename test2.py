import nfc
import requests
from datetime import datetime

def on_connect(tag):
    try:
        if tag.ndef:
            data = tag.ndef.records[0].text
            print("Data read:", data)
            
            # Assuming the card ID is stored in the first NDEF record's text
            send_attendance(data)
        else:
            print("No NDEF data found")
    except Exception as e:
        print(f"Error reading tag: {e}")
    
    return False  # Disconnect after the first tag is read

def send_attendance(nfc_card_id):
    url = 'http://localhost:5000/api/save_attendance'
    response = requests.post(url, json={'nfc_card_id': nfc_card_id})
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print('Attendance record saved successfully!')
        else:
            print('Error:', result['error'])
    else:
        print(f"Failed to connect to server, status code: {response.status_code}")

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        print("Waiting for NFC tag...")
        while True:
            clf.connect(rdwr={'on-connect': on_connect})

if __name__ == "__main__":
    main()
