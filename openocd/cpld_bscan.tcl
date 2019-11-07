
set BSCAN_SAMPLE    0x005
set BSCAN_EXTEST    0x00F
set BSCAN_LEN       480

irscan EPM570.tap $BSCAN_SAMPLE
drscan EPM570.tap $BSCAN_LEN 0

#set result [drscan EP1AGX90EF1152C6N.tap $BSCAN_LEN 0]
#puts $result
