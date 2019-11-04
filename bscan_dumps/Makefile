

# bsdl2json.py can be found here: 
# https://github.com/cyrozap/python-bsdl-parser
BSDL2JSON	= ../../python-bsdl-parser/bsdl2json.py

EPM570F100_URL     = https://www.intel.com/content/dam/altera-www/global/en_US/others/support/devices/bsdl/EPM570F100.BSD
EP1AGX90EF1152_URL = https://www.intel.com/content/dam/altera-www/global/en_US/others/support/devices/bsdl/EP1AGX90EF1152.BSD

all: EP1AGX90EF1152.json EPM570F100.json

EPM570F100.json: EPM570F100.BSD
	$(BSDL2JSON) EPM570F100.BSD > EPM570F100.json

EP1AGX90EF1152.json: EP1AGX90EF1152.BSD
	$(BSDL2JSON) EP1AGX90EF1152.BSD > EP1AGX90EF1152.json

EPM570F100.BSD: 
	curl $(EPM570F100_URL) > $@

EP1AGX90EF1152.BSD:
	curl $(EP1AGX90EF1152_URL) > $@

clean:
	\rm -f EPM570F100.json EP1AGX90EF1152.json EPM570F100.BSD EP1AGX90EF1152.BSD
