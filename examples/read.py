import mfrc522
from os import uname
import time


def do_read():

    if uname()[0] == 'WiPy':
        rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    elif uname()[0] == 'esp32':
        #                  sck, mosi, miso, rst, cs
        rdr = mfrc522.MFRC522(14, 13, 12, 5, 27)
    else:
        raise RuntimeError("Unsupported platform")

    print("")
    print("Place card before reader to read from address 0x08")
    print("")

    try:
        while True:
            print("Trying request")
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            print(f"Stat: {stat}")
            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            print("Address 8 data: %s" % rdr.read(8))
                            rdr.stop_crypto1()
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")
            time.sleep(10)
    except KeyboardInterrupt:
		print("Bye")
