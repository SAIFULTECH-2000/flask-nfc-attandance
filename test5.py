import nfc
import sys

def on_connect(tag):
    """Callback function called when an NFC tag is detected."""
    print("Tag detected!")
    if tag.ndef:
        # Read the first NDEF record
        record = tag.ndef.records[0]
        data = record.text
        print("Data read from tag:", data)
    else:
        print("No NDEF data found")

def main():
    try:
        # Initialize the NFC reader using 'usb' backend
        clf = nfc.ContactlessFrontend('pcsc')
        print("NFC reader initialized. Waiting for NFC tag...")

        # Connect to the NFC reader and set the callback function
        clf.connect(rdwr={'on-connect': on_connect})

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    
    finally:
        # Ensure the NFC reader is closed properly
        if 'clf' in locals():
            clf.close()
            print("NFC reader connection closed.")

if __name__ == "__main__":
    main()
