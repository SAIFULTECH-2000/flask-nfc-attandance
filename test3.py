import nfc

def on_connect(tag):
    # Extract and print the tag's data
    print("NFC Tag detected")
    print("Tag ID: ", tag.identifier.hex())
    if hasattr(tag, 'text'):
        print("Text Data: ", tag.text)
    else:
        print("No text data available on this tag.")

# Initialize NFC reader
with nfc.ContactlessFrontend('usb') as clf:
    while True:
        print("Waiting for NFC Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
