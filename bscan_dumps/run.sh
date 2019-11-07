
../../bscan_tools/bscan_proc.py -r fpga_pin_renamings.txt EP1AGX90EF1152.json bscan_sample_empty.txt      > fpga_pin_report.empty.txt
../../bscan_tools/bscan_proc.py -r fpga_pin_renamings.txt EP1AGX90EF1152.json bscan_sample_orig.txt       > fpga_pin_report.orig.txt
../../bscan_tools/bscan_proc.py -r fpga_pin_renamings.txt EP1AGX90EF1152.json bscan_sample_empty2orig.txt > fpga_pin_report.empty2orig.txt

../../bscan_tools/bscan_proc.py -r cpld_pin_renamings.txt EPM570F100.json cpld_sample_empty_in_pcie.txt > cpld_pin_report.empty_in_pcie.txt
../../bscan_tools/bscan_proc.py -r cpld_pin_renamings.txt EPM570F100.json cpld_sample_orig_in_pcie.txt  > cpld_pin_report.orig_in_pcie.txt
../../bscan_tools/bscan_proc.py -r cpld_pin_renamings.txt EPM570F100.json cpld_sample_empty_in_pcie.txt cpld_sample_orig_in_pcie.txt  > cpld_pin_report.diff.txt
