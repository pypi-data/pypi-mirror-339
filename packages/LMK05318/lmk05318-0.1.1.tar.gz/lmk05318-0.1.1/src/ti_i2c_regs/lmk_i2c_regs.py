from smbus2 import SMBus, i2c_msg

class lmk_i2c_regs:
    def __init__(self, i2c_bus=0, i2c_addr=0x64):
        self.i2c_bus = i2c_bus
        self.i2c_addr = i2c_addr
        pass

    def peek8(self, addr):
        lsb = addr & 0xFF
        msb = (addr >> 8) & 0xFF
        write_data = [msb, lsb]
        received_byte = 0
        with SMBus(self.i2c_bus) as bus:
            write_msg = i2c_msg.write(self.i2c_addr, write_data)
            read_msg = i2c_msg.read(self.i2c_addr, 1)  # Request 1 byte
            bus.i2c_rdwr(write_msg, read_msg)  # Perform the read transaction
            # Convert the buffer to a list of bytes
            received_data = list(read_msg)  # This is a list of bytes
            if received_data:  # Ensure data was received
                received_byte = received_data[0]  # Extract the first byte
            else:
                raise Exception("No i2c register was read!")
        return received_byte

    def poke8(self, addr, val):
        lsb = addr & 0xFF
        msb = (addr >> 8) & 0xFF
        write_data = [msb, lsb, val]
        with SMBus(self.i2c_bus) as bus:
            write_msg = i2c_msg.write(self.i2c_addr, write_data)
            bus.i2c_rdwr(write_msg)  # Perform the write operation
