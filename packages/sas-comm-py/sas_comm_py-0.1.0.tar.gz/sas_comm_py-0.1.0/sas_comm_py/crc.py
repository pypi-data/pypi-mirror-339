from ctypes import c_ushort

class CRC16K(object):
    crc_table = []

    CRC_CONSTANT = 0x8408

    def __init__(self):
        # Initialize the precalculated table
        if not len(self.crc_table):
            self.init_table()

    def compute(self, data_input=None):
        try:
            is_string = isinstance(data_input, str)
            is_bytes = isinstance(data_input, bytes)

            if not is_string and not is_bytes:
                raise Exception("Please provide a string or a byte sequence as argument for computation.")

            crc_val = 0x0000

            for ch in data_input:
                byte_val = ord(ch) if is_string else ch
                temp = crc_val ^ byte_val
                crc_val = c_ushort(crc_val >> 8).value ^ int(self.crc_table[(temp & 0x00ff)], 0)

            # After processing, swap the two bytes of the one's complement of the CRC.
            low_byte = (crc_val & 0xff00) >> 8
            high_byte = (crc_val & 0x00ff) << 8
            crc_val = low_byte | high_byte

            return crc_val
        except Exception as err:
            print("EXCEPTION(compute): {}".format(err))

    def init_table(self):
        '''Precalculate the CRC table values'''
        for i in range(0, 256):
            crc_value = c_ushort(i).value
            for j in range(0, 8):
                if (crc_value & 0x0001):
                    crc_value = c_ushort(crc_value >> 1).value ^ self.CRC_CONSTANT
                else:
                    crc_value = c_ushort(crc_value >> 1).value
            self.crc_table.append(hex(crc_value))
