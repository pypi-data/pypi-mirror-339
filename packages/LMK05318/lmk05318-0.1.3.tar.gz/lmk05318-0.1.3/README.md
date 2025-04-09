# Linux pure Python library for LMK05318 Ultra-Low Jitter Network Synchronizer Clock With Two Frequency Domains.
## Check if LMK05318 is present in the system.
By default the address is **0x64**. Check the device is present in your system (I2C bus **0** in our case):
```
# i2cdetect -y 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         08 -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- UU -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- UU -- -- -- 
50: -- -- UU UU -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- 64 -- -- -- -- UU -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --
```
## Debug and development
Create virtual environment
```
make venv
source ./venv/bin/activate
```
Run tests:
```
$ make test
venv/bin/python3 -m unittest discover -s tests
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
Copy the tarball with Python sources to your board */tmp* directory:
```
./copy_to_board.sh 192.168.2.21
```

Run on board as root:
```
cd /tmp && ./untar_install.sh LMK05318
```

Run as root:
```
# python3 -m lmk05318     
usage: __main__.py [-h] [-b BUS] [-a ADDR] [{wfile,rfile,sdpll,sapll,spll}] [arg2]

LMK05318 configuration and status utility.

positional arguments:
  {wfile,rfile,sdpll,sapll,spll}
                        wfile path    Write cfg regs to eeprom from file (path) prepared
                                      by TI utility TICSPRO-SW.
                        rfile path    Dump cfg regs to file (path)
                        sdpll         Get status of DPLL.
                        sapll         Get APLL and XO status.
                        spll          Get full status.
  arg2                  Optional parameter for cmd.

optional arguments:
  -h, --help            show this help message and exit
  -b BUS, --bus BUS     Specify I2C bus number, default - 0.
  -a ADDR, --addr ADDR  Specify I2C address, default - 0x64.
```
## Write to EEPROM the registers file prepared by TI utility TICS Pro
Copy the file to the board:
```
scp ./HexRegisterValues_free_run.txt   root@192.168.2.16:/tmp/LMK05318
```
Flash the file to the chip's EEPROM:
```
root@eccahemcmain1:/tmp/LMK05318# python3 -m lmk05318 -b 0 -a 0x64 wfile ./HexRegisterValues_free_run.txt 
INFO:lmk05318:Vendor ID Readback: 0x100B
INFO:lmk05318:Product ID Readback: 0x35
LMK05318 valid: True
INFO:lmk05318:Attention: writing to register 0c with masked bits, mask 0xa7 was applied, resulting in value 1b
INFO:lmk05318:Attention: writing to register 9d with masked bits, mask 0xff was applied, resulting in value 00
INFO:lmk05318:Attention: writing to register a4 with masked bits, mask 0xff was applied, resulting in value 00
INFO:lmk05318:Attention: writing to register 165 with masked bits, mask 0xff was applied, resulting in value 28
INFO:lmk05318:Attention: writing to register 16f with masked bits, mask 0xff was applied, resulting in value 00
INFO:lmk05318:Attention: writing to register 19b with masked bits, mask 0xff was applied, resulting in value 00
INFO:lmk05318:write current device register content to EEPROM
INFO:lmk05318:wait till busy bit becomes 1
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:wait till busy bit becomes 0
INFO:lmk05318:programming EEPROM done, power-cycle or hard-reset to take effect
root@eccahemcmain1:/tmp/LMK05318# 
```
## Read back all the registers from LMK05318 device to the file:
```
root@eccahemcmain1:/tmp# python3 -m lmk05318 -b 0 -a 0x64 rfile ./HexRegs.txt
INFO:lmk05318:Vendor ID Readback: 0x100B
INFO:lmk05318:Product ID Readback: 0x35
LMK05318 valid: True
```
## Check DPLL and APLL status:
Check DPLL:
```
root@eccahemcmain1:/tmp# python3 -m lmk05318 -b 0 -a 0x64 sdpll
INFO:lmk05318:Vendor ID Readback: 0x100B
INFO:lmk05318:Product ID Readback: 0x35
LMK05318 valid: True

        Loss of phase lock: 1
        Loss of freq. lock: 1
        Tuning word update: 1
        Holdover Event: 1
        Reference Switch Event: 0
        Active ref. missing clk: 0
        Active ref. loss freq.: 0
        Active ref. loss ampl.: 0
```
Check APLL:
```
root@eccahemcmain1:/tmp# python3 -m lmk05318 -b 0 -a 0x64 sapll
INFO:lmk05318:Vendor ID Readback: 0x100B
INFO:lmk05318:Product ID Readback: 0x35
LMK05318 valid: True

        Loss of freq. detection XO: 0
        Loss of lock APLL2: 1
        Loss of lock APLL1: 0
        Loss of source XO: 0
```
Check full (DPLL, APLL and XO) status:
```
root@eccahemcmain1:/tmp# python3 -m lmk05318 spll
INFO:lmk05318:Vendor ID Readback: 0x100B
INFO:lmk05318:Product ID Readback: 0x35
LMK05318 valid: True

        Loss of phase lock: 1
        Loss of freq. lock: 1
        Tuning word update: 1
        Holdover Event: 1
        Reference Switch Event: 0
        Active ref. missing clk: 0
        Active ref. loss freq.: 0
        Active ref. loss ampl.: 0
        

        Loss of freq. detection XO: 0
        Loss of lock APLL2: 1
        Loss of lock APLL1: 0
        Loss of source XO: 0
```
