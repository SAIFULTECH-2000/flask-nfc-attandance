import time
import board
import busio
from adafruit_pn532 import PN532_I2C

# Create library object
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Initialize the NFC reader
pn532.SAM_configuration()

print("Waiting for an NFC card...")

while True:
    # Scan for an NFC card
    uid = pn532.read_passive_target()
    
    # Check if we have a card
    if uid is not None:
        print("Found an NFC card!")
        print("UID:", [hex(i) for i in uid])
        # Convert UID to a string
        uid_str = ''.join([f"{i:02x}" for i in uid])
        print(f"UID as text: {uid_str}")
        
        # Wait a bit before scanning again
        time.sleep(1)
