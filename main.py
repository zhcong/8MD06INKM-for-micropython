from machine import SPI, Pin
from _8MD06INKM import _8MD06INKM
import time

rest_pin=Pin(27, Pin.OUT)
cs_pin=Pin(28, Pin.OUT)
hv_en_pin=Pin(29, Pin.OUT)

spi=SPI(id=1, baudrate=100_000, polarity=1, phase=1, sck=Pin(10, Pin.OUT), mosi=Pin(11,Pin.OUT))

display = _8MD06INKM(spi, rest_pin, cs_pin, hv_en_pin)
display.init()

display.set_brightness(100)
time.sleep(1)
display.set_brightness(255)

display.hv_off()
time.sleep(1)
display.hv_on()

def print_all(chars):
    for i in range(8):
        if type(chars[i]) == int:
            display.code(i, chars[i])
        else:
            display.print_char(i,chars[i])
print_all('Hello-  ')

bits=[0xff,0x41,0x41,0x41,0xff]
display.print_bits(7, bits);
