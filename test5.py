from nfc import ContactlessFrontend
from time import sleep

def connected(tag):
    """Callback function when an NFC tag is detected."""
    ident = ''.join('{:02x}'.format(b) for b in tag.identifier)
    print(f"Tag ID: {ident}")
    return False  # Return False to stop connection after tag is read

def main():
    try:
        # Initialize the NFC reader
        clf = ContactlessFrontend('usb')
        print("NFC reader initialized. Waiting for tags...")
        
        while True:
            # Continuously look for NFC tags
            clf.connect(rdwr={'on-connect': connected})
            sleep(1)  # Sleep for 1 second to avoid busy-waiting

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure the NFC reader is closed properly
        if 'clf' in locals():
            clf.close()
            print("NFC reader connection closed.")

if __name__ == "__main__":
    main()
