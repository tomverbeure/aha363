

* Altera EP1AGX90EF1152C6N: Arria GX 90E

    * [Arria GX Handbook](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/hb/agx/arriagx_handbook.pdf)
    * 1152 pins
    * [Arria GX pinout](https://www.intel.com/content/www/us/en/programmable/support/literature/lit-dp.html)
    * [BSDL files for Arria GX FPGAs](https://www.intel.com/content/www/us/en/programmable/support/support-resources/download/board-layout-test/bsdl/arriagx.html) and
      [BSDL file for this FPGA](https://www.intel.com/content/dam/altera-www/global/en_US/others/support/devices/bsdl/EP1AGX90EF1152.BSD)

    * [Quartus 11.0sp1 Download](https://www.intel.com/content/www/us/en/programmable/downloads/software/quartus-ii-we/110sp1.html)
      Last free version that supports Arria GX.

* Spansion GL128P10FFI01: S29GL128P MirrorBit Flash 128Mbit

* Altera EPM570F100C4N MAX II CPLD

    [MAX II Handbook](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/hb/max2/max2_mii5v1.pdf)
    
    See [Arria GX Development Board Reference Manual](http://static6.arrow.com/aropdfconversion/8a0fa1b74c4ba00b20a5b2c3e5429593b6c2bd57/rm_arria_gx_pcie_board.pdf)
    for 4x PCIe reference design with EPM570 to handle bootup and flash programming. 

    [Parallel Flash Load IP Core User Guide](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/an/an386.pdf)

    [BSDL files for MAX II CPLDs](https://www.intel.com/content/www/us/en/programmable/support/support-resources/download/board-layout-test/bsdl/max2.html)
    [BSDL file for EPM570F100](https://www.intel.com/content/dam/altera-www/global/en_US/others/support/devices/bsdl/EPM570F100.BSD)
    

* 2x AHA3610B HW Compression ASIC



Quartus install:

To avoid this error:
```
`ImportError: /usr/lib/i386-linux-gnu/libfreetype.so.6: symbol png_set_expand_gray_1_2_4_to_8, version PNG12_0 not defined in file libpng12.so.0 with link time reference`
```

Do:

```
sh ./Downloads/11.1_173_quartus_linux.sh 
bash ./Download/11.1_173_quartus_linux.sh 
cd 11.1_173_quartus_linux 
mv altera_installer/bin/libpng12.so.0 ../ 
bash ./setup 
```


JTAG connector:

top: from left to right

```
bottom   top
1: TDI   NC
2: TDO   GND
3: TCK   GND
---
4: TMS   GND 
5: VREF  GND
```

Arria TDI does not go to connector but goes to TDO of MAX2.

Pins:

```
AJ19: Y1, 100MHz
AN19: Y2, 100Mhz (Also connected to the CPLD on pin E1)

MSEL[3:0]: 4'b1100  - Remote system upgrade FPP with decompression feature enabled
RUnLU:     1'b0     - Local update

PCIe Pinout: https://en.wikipedia.org/wiki/PCI_Express#Pinout

REFCLKn     : V2
REFCLKp     : V1

HSIn(3)     : AB5
HSIp(3)     : AB4

HSIn(2)     : Y5
HSIp(2)     : Y4

HSIn(1)     : N5        // 1 and 0 have swapped positions
HSIp(1)     : N4

HSIn(0)     : R5
HSIp(0)     : R4

HSOn(3)     : AB2
HSOp(3)     : AB1

HSOn(2)     : Y2
HSOp(2)     : Y1

HSOn(1)     : N2        
HSOp(1)     : N1

HSOn(0)     : R2
HSOp(0)     : R1

SMCLK:      : AJ23
SMDATA:     : AK23
POWERGD     : AL24 (?!)

LED_1       : AM22
LED_2       : AM21
LED_3       : unknown
LED_4       : CPLD pin D8
LED_5       : AJ21
LED_6       : AL21

```

PSU configuration:

12V power is supplied via the PCIe edge connector, or via JP2. This is converted by U10 (VPOL5A-12-SMT) into 5v. This is then fed into the following:
* U14: EN5335QI, configured for 3.3v output (3A)
* U6: EN5365QI, configured for 3.3v output (6A)
* U7: EN5365QI, configured for 1.2v output (6A)
* U8: EN5365QI, configured for 2.5v output (6A)

However, the outputs of U6 and U7 have been bridged. This results in U7 becoming hot during use. The cause of this is unclear, but it is assumed that this is an error in the configuration of U7.

Dump Flash file:

* While plugged into a PC (!)
* Quartus Programmer
* Hardware Setup -> Double click on USB-Blaster -> Close 
* Auto Detect 
* CFG_128Mb -> Examine -> Start
* Right click on untitled1.pof -> Save File

Do this twice and compare the 2 POF files to make sure they're the same!

Erase the Flash file: (!)

* CFG_128Mb -> Erase -> Start

Reprogram the Flash file:

* CFG_128Mb -> Right click: Change File (NOT Add File!!!) -> Select .pof file -> Start


Dump JTAG boundary scan of original bitstream and dump:

```
cd openocd
sudo /opt/openocd/bin/openocd -f /opt/openocd/share/openocd/scripts/interface/altera-usb-blaster.cfg -f ./aha363.tcl
telnet localhost 4444
source bscan.tcl
```

Dump JTAG boundary scan of empty bitstream and dump

* Create design with only inputs

    First specify 1000 input -> Quartus will complain and say how many you can really use
    Then use that number...

* Also: set all unused pins to input-tristate

* Settings -> Assembler: Always enable input buffers

    "This option is required for the SAMPLE/PRELOAD JTAG instruction to function correctly on output pins."


* Load SOF:

    * 11ms of bursts of DCLK while STATUSn is high
    * then STATUSn goes low


