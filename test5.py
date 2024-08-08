from nfc import ContactlessFrontend
from time import sleep
 
def connected(tag):
    ident = ''.join('{:02x}'.format(ord(c)) for c in tag.identifier)
    print(ident)
    return False
 
clf = ContactlessFrontend('usb')
while True:
    clf.connect(rdwr={'on-connect': connected})
    sleep(1)