from lmk05318 import LMK05318
from ti_i2c_regs import lmk_i2c_regs

class ConsoleHelper:
    """
    Parse file prepared by Texas Instruments utility: 
    """
    @staticmethod
    def parse(path):
        register_list = []
        with open(path, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    hex_str = line.strip().split('\t0x')[1]
                    if len(hex_str) != 6:
                        raise Exception("Wrong file format!")
                    addr = int(hex_str[0:4], 16)
                    val = int(hex_str[4:6], 16)
                    register_list.append((addr, val))
        return register_list


    @staticmethod
    def write_cfg_regs_to_eeprom_from_file(lmk, path):
        register_list = ConsoleHelper.parse(path)
        lmk.pokes8(register_list)
        lmk.write_cfg_regs_to_eeprom(method=LMK05318.LMK_EEPROM_REG_COMMIT)


    @staticmethod
    def dump_regs_to_file(lmk, path):
        line_list=[]
        def append_reg_to_list(addr):
            val = lmk.peek8(addr)
            reg_str = 'R'+str(addr)
            addr_str = f"0x{addr:04X}{val:02X}"
            out_str = reg_str + '\t' + addr_str + '\n'
            line_list.append(out_str)
        for addr in range(353):
            append_reg_to_list(addr)
        append_reg_to_list(357)
        append_reg_to_list(367)
        append_reg_to_list(411)

        with open(path, 'w') as file:
            file.writelines(line_list)


def main():
    lmk_regs_iface = lmk_i2c_regs(0, 0x64)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    vendor_id = lmk.get_vendor_id()
    print(f"LMK05318 vendor_id: {hex(vendor_id)}")
    status = lmk.get_status_dpll()
    print(f"LMK05318 status {status}")
    valid = lmk.is_chip_id_valid()
    print(f"LMK05318 valid: {valid}")
if __name__ == '__main__':
    main()