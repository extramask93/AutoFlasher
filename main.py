#pip3 install pyserial
#pip3 install argparse
#running: python3 main.py -d COMXX

import argparse
import serial
from PowerSupply import PowerSupply
from time import sleep
def flash_image(ser, image, ram_addr, hyperflash_addr):
    ser.write(b"xls2\r\n")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(b"3\r\n")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(b"yyy")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(ram_addr.encode('utf_8')+b"\r\n")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(hyperflash_addr.encode('utf_8')+b"\r\n")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(open(image, "rb").read())
    while True:
        a = ser.read_until(b"\r\n")
        print(a+b'dupa')
        if(b'ORER' in a):
            break
    ser.write(b"y\r\n")
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
    print(ser.read_until(b"\r\n"))
def init_serial(com):
    ser = serial.Serial(com, 115200, timeout=15)
    ser.write(open("Minimot_B2Sample_v2.srec", "rb").read())
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.write(b"sup\r\n")
    print(ser.read_until())
    print(ser.read_until())
    print(ser.read_until())
    ser.baudrate = 921600
    return ser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flasher tool')

    parser.add_argument('--dev', '-d', type=str, dest='device', required=True,
                        help='')
    parser.add_argument('--supply', '-s', type=str, dest='supply', required=False,
                        help='')
    parser.add_argument('--arduino', '-a', type=str, dest='arduino', required=False,
                        help='')
    
    args = parser.parse_args()

    arduino = serial.Serial(args.arduino, 9600, timeout=1)
    powerSupply = PowerSupply(args.supply)

    powerSupply.poweroff()
    sleep(0.5)
    arduino.write(b'\x00') # switch 1,3,4 off
    sleep(0.5)
    powerSupply.poweron()
    sleep(1.5)

    ser = init_serial(args.device)
    flash_image(ser, 'eCockpit_RcarH3_CR7.srec', '48000000', '1000000')
    #flash_image(ser, 'FirmwareInfo_0xE6320000_0x1FC0000.srec', 'e6320000','1fc0000')

    arduino.write(b'\xFF') #switch 1,3,4 on
    powerSupply.poweroff()
    sleep(1)
    powerSupply.poweron()

