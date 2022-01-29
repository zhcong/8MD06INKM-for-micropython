import time

class _8MD06INKM():
    
    def __init__(self, spi, rest_pin, cs_pin, hv_en_pin):
        self.spi = spi
        self.rest_pin = rest_pin
        self.cs_pin = cs_pin
        self.hv_en_pin = hv_en_pin

    def __msb_to_lsb(self, data):
        tran_data=0x00
        tran_data = tran_data | ((data & (0x80 >> 0)) >> 7)
        tran_data = tran_data | ((data & (0x80 >> 1)) >> 5)
        tran_data = tran_data | ((data & (0x80 >> 2)) >> 3)
        tran_data = tran_data | ((data & (0x80 >> 3)) >> 1)
        tran_data = tran_data | ((data & (0x80 >> 4)) << 1)
        tran_data = tran_data | ((data & (0x80 >> 5)) << 3)
        tran_data = tran_data | ((data & (0x80 >> 6)) << 5)
        tran_data = tran_data | ((data & (0x80 >> 7)) << 7)
        return tran_data
    
    def init(self):
        self.hv_on()
        self.rest_pin.value(1)
        time.sleep(0.1)
        self.cs_pin.value(1)
        self.__send_data_batch(0xE0, 0x07)
        self.__send_data_batch(0xE8, 0x00)

    # brightness： 0-255
    def set_brightness(self, brightness:int):
        self.__send_data_batch(0xE4, brightness)

    def hard_rest(self):
        self.rest_pin.value(0)
        time.sleep(0.1)
        self.rest_pin.value(1)

    def hv_off(self):
       self.hv_en_pin.value(0)
    
    def hv_on(self):
       self.hv_en_pin.value(1) 

    def __send_data_batch(self, command, data):
        self.cs_pin.value(0)
        data_list = bytearray(1)
        data_list[0]=self.__msb_to_lsb(command)
        self.spi.write(data_list)
        time.sleep_ms(1)
        data_list[0]=self.__msb_to_lsb(data)
        self.spi.write(data_list)
        time.sleep_ms(1)
        self.cs_pin.value(1)

    def __send_data(self, data):
        data_list = bytearray(1)
        data_list[0]=self.__msb_to_lsb(data)
        self.spi.write(data_list)
    
    def __write_customize_to_ram(self, data_list):
        self.cs_pin.value(0)
        # only use first customize ram
        self.__send_data(0x40 + 0x00)
        time.sleep_ms(1)
        self.__send_data(data_list[0])
        time.sleep_ms(1)
        self.__send_data(data_list[1])
        time.sleep_ms(1)
        self.__send_data(data_list[2])
        time.sleep_ms(1)
        self.__send_data(data_list[3])
        time.sleep_ms(1)
        self.__send_data(data_list[4])
        self.cs_pin.value(1)
    
    #one zone is 5*7, bits_list size is 5, and use first 7 bit(LSB) in all of the 8 bit
    def print_bits(self, position, bits_list):
        self.__write_customize_to_ram(bits_list)
        self.print_code(position, 0x00)
    
    def print_char(self, position, char):
        self.print_code(position, ord(char))

    def print_code(self, position, code):
        self.cs_pin.value(0)
        self.__send_data(0x20 + position)
        time.sleep_ms(1)
        self.__send_data(code);
        self.cs_pin.value(1)
