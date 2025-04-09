from lmk05318 import LMK05318, ConsoleHelper
from ti_i2c_regs import lmk_i2c_regs
import logging
import argparse
import sys


def wfile(path):
    lmk_regs_iface = lmk_i2c_regs(0, 0x64)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    valid = lmk.is_chip_id_valid()
    print(f"LMK05318 valid: {valid}")
    if valid:
        ConsoleHelper.write_cfg_regs_to_eeprom_from_file(lmk, path)

def rfile(path):
    lmk_regs_iface = lmk_i2c_regs(0, 0x64)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    valid = lmk.is_chip_id_valid()
    print(f"LMK05318 valid: {valid}")
    if valid:
        ConsoleHelper.dump_regs_to_file(lmk, path)

def sdpll():
    lmk_regs_iface = lmk_i2c_regs(0, 0x64)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    valid = lmk.is_chip_id_valid()
    print(f"LMK05318 valid: {valid}")
    if valid:
        status = lmk.get_status_dpll()
        print(status)

def spllxo():
    lmk_regs_iface = lmk_i2c_regs(0, 0x64)
    lmk = LMK05318(regs_iface=lmk_regs_iface)
    valid = lmk.is_chip_id_valid()
    print(f"LMK05318 valid: {valid}")
    if valid:
        status = lmk.get_status_pll_xo()
        print(status)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="LMK05318 configuration and status utility.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'cmd',
        nargs='?', default=None,
        choices=['wfile', 'rfile', 'sdpll', 'spllxo'],
        help=(
            'wfile path    Write cfg regs to eeprom from file (path) prepared\n'
            '              by TI utility TICSPRO-SW.\n'
            'rfile path    Dump cfg regs to file (path)\n'
            'sdpll         Get status dpll.\n'
            'spllxo        Get status pll xo.\n'
        )
    )
    parser.add_argument('arg2', nargs='?', default=None, help='Optional parameter for cmd.')
    args = parser.parse_args()

    if args.cmd == 'wfile':
        path = args.arg2
        if path is None:
            parser.print_help()  # Display help message
            sys.exit(1)  # Exit with an error code
        wfile(path)
    elif args.cmd == 'rfile':
        path = args.arg2
        if path is None:
            parser.print_help()  # Display help message
            sys.exit(1)  # Exit with an error code
        rfile(path)
    elif args.cmd == 'sdpll':
        sdpll()
    elif args.cmd == 'spllxo':
        spllxo()
    else:
        parser.print_help()  # Display help message
        sys.exit(1)  # Exit with an error code


    # main(path=args.path)
