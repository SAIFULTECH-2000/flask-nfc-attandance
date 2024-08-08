import nfc
import nfc.ndef

def on_connect(tag):
    """Callback function called when an NFC tag is detected."""
    print("Tag detected!")
    
    # Check if the tag is writable
    if not tag.ndef:
        print("Tag does not support NDEF.")
        return

    # Data to write
    text_data = "Hello, NFC World!"
    
    # Create an NDEF text record
    text_record = nfc.ndef.TextRecord(text_data)
    
    # Create an NDEF message containing the text record
    ndef_message = nfc.ndef.Message(text_record)

    # Write the NDEF message to the tag
    tag.ndef.message = ndef_message
    print(f"Data '{text_data}' written to the tag.")

def main():
    try:
        # Initialize the NFC reader using 'usb' backend
        clf = nfc.ContactlessFrontend('usb')
        print("NFC reader initialized. Waiting for NFC tag...")

        # Connect to the NFC reader and set the callback function
        clf.connect(rdwr={'on-connect': on_connect})

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the NFC reader is closed properly
        if 'clf' in locals():
            clf.close()
            print("NFC reader connection closed.")

if __name__ == "__main__":
    main()
