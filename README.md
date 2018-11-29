# cwkeyer

cwkeyer is a python based serial cw keyer for use with generic serial interfaces.  That is to say, it functions by manipulating the RTS or DTR pin of a serial port and can act like a computer controlled sstrait key.  Because of this, it works with any radio that has a key jack.

-d specifies the serial device. default is '/dev/ttyUSB0'
-w CW keying speed in words per minutes. default: 20 wpm
-t Text to transmit. Surround multiple words by quotes.
--dtr Use DTR pin instead of RTS pin for keying. default is to use RTS

