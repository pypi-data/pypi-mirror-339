from lmk05318 import LMK05318, ConsoleHelper
from ti_i2c_regs import lmk_i2c_regs
import logging
import argparse
import sys

def get_lmk(i2c_bus, i2c_addr):
    lmk_regs_iface = lmk_i2c_regs(i2c_bus, i2c_addr)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    return lmk

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="LMK05318 configuration and status utility.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'cmd',
        nargs='?', default=None,
        choices=['wfile', 'rfile', 'sdpll', 'sapll', 'spll'],
        help=(
            'wfile path    Write cfg regs to eeprom from file (path) prepared\n'
            '              by TI utility TICSPRO-SW.\n'
            'rfile path    Dump cfg regs to file (path)\n'
            'sdpll         Get status of DPLL.\n'
            'sapll         Get APLL and XO status.\n'
            'spll          Get full status.\n'
        )
    )
    parser.add_argument('arg2', nargs='?', default=None, help='Optional parameter for cmd.')
    parser.add_argument('-b', '--bus', help='Specify I2C bus number, default - 0.', required=False)
    parser.add_argument('-a', '--addr', help='Specify I2C address, default - 0x64.', required=False)

    args = parser.parse_args()

    if args.bus is None:
        i2c_bus = 0
    else:
        i2c_bus = int(args.bus, 0)

    if args.addr is None:
        i2c_addr = int('0x64', 16)
    else:
        i2c_addr = int(args.addr, 0)

    if args.cmd == 'wfile':
        """
        Write to EEPROM the registers file prepared by TI utility TICS Pro
        """
        path = args.arg2
        if path is None:
            parser.print_help()  # Display help message
            sys.exit(1)  # Exit with an error code
        lmk = get_lmk(i2c_bus=i2c_bus, i2c_addr=i2c_addr)
        valid = lmk.is_chip_id_valid()
        print(f"LMK05318 valid: {valid}")
        if valid:
            ConsoleHelper.write_cfg_regs_to_eeprom_from_file(lmk, path)
    elif args.cmd == 'rfile':
        """
        Read back all the registers from LMK05318 device to the file.
        """
        path = args.arg2
        if path is None:
            parser.print_help()  # Display help message
            sys.exit(1)  # Exit with an error code
        lmk = get_lmk(i2c_bus=i2c_bus, i2c_addr=i2c_addr)
        valid = lmk.is_chip_id_valid()
        print(f"LMK05318 valid: {valid}")
        if valid:
            ConsoleHelper.dump_regs_to_file(lmk, path)
    elif args.cmd == 'sdpll':
        """
        Check DPLL status:
        """
        lmk = get_lmk(i2c_bus=i2c_bus, i2c_addr=i2c_addr)
        valid = lmk.is_chip_id_valid()
        print(f"LMK05318 valid: {valid}")
        if valid:
            status = lmk.get_status_dpll()
            print(status)
    elif args.cmd == 'spllxo':
        """
        Check APLL and XO status:
        """
        lmk = get_lmk(i2c_bus=i2c_bus, i2c_addr=i2c_addr)
        valid = lmk.is_chip_id_valid()
        print(f"LMK05318 valid: {valid}")
        if valid:
            status = lmk.get_status_pll_xo()
            print(status)
    elif args.cmd == 'spll':
        """
        Check DPLL, APLL and XO status:
        """
        lmk = get_lmk(i2c_bus=i2c_bus, i2c_addr=i2c_addr)
        valid = lmk.is_chip_id_valid()
        print(f"LMK05318 valid: {valid}")
        if valid:
            status = lmk.get_status_dpll()
            print(status)
            status = lmk.get_status_pll_xo()
            print(status)
    else:
        parser.print_help()  # Display help message
        sys.exit(1)  # Exit with an error code


    # main(path=args.path)
