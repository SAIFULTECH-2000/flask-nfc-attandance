import nfc

def list_devices():
    with nfc.ContactlessFrontend('pcsc') as clf:
        print("NFC reader initialized. Listing devices...")
        print(clf.list_devices())

if __name__ == "__main__":
    list_devices()
