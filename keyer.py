import time
import sys
import serial
import argparse

chars =   {'A':'._',
           'B':'_...',
           'C':'_._.',
           'D':'_..',
           'E':'.',
           'F':'.._.',
           'G':'__.',
           'H':'....',
           'I':'..',
           'J':'.___',
           'K':'_._',
           'L':'._..',
           'M':'__',
           'N':'_.',
           'O':'___',
           'P':'.__.',
           'Q':'__._',
           'R':'._.',
           'S':'...',
           'T':'_',
           'U':'.._',
           'V':'..._',
           'W':'.__',
           'X':'_.._',
           'Y':'_.__',
           'Z':'__..',
           '0':'_____',
           '1':'.____',
           '2':'..___',
           '3':'...__',
           '4':'...._',
           '5':'.....',
           '6':'_....',
           '7':'__...',
           '8':'___..',
           '9':'____.',
           '?':'..__..',
	   '.':'._._._',
           ',':'__..__',
           '/':'_.._.'
           }

cut_nums = {
            '1':'._',
            '9':'_.',
            '0':'_'
           }

class cw_text_parser:
  def __init__(self, wpm):
    self.recalculate_speeds(wpm)

  def recalculate_speeds(self, wpm):
    self.ditspeed = (1200.0 / float(wpm)) / 1000.0
    self.dahspeed = ((1200.0 / float(wpm)) / 1000.0) * 3
    self.charspace = ((1200.0 / float(wpm)) / 1000.0) * 1
    self.wordspace = ((1200.0 / float(wpm)) / 1000.0) * 7

  # sleep for the given amount of time
  def space(self, duration):
    time.sleep(duration)

  # keydown for "duration" time, and pad after with "gap" time
  def key(self, keydown_time, space_time):
    cw_key(key_open)
    cw_key(key_close)
    time.sleep(keydown_time)
    cw_key(key_open)
    time.sleep(space_time)

  def word(self, w, wpm):
    i=0
    while i < len(w):
      c=w[i]
      # catch a new macro escape
      if c == "<":
        # setup the first char of the macro past the macro escape char '<'
        i+=1
        macro=w[i]
        # loop matching macro commands, till we find '>'
        # each time a macro "match" is found, execute it
        # then reset the macro command, and increment index
        while True:
          if macro == "+" or macro == "-":
            if macro == "+":
              wpm+=5
            else:
              wpm+=-5
            self.recalculate_speeds(wpm)
            #reset current macro command
            macro = ""
          elif macro == ">":
            #break out of the while loop
            if i < len(w)-1:
              i+=1
              c=w[i]
            break
          i+=1
          macro = macro + str(w[i])
      else:
        try:
          code = chars[c]
          i+=1
        except KeyError:
          # skip unknown chars
          i+=1
          continue

        for dahdit in code:
          if dahdit == '_':
            self.key(self.dahspeed, self.charspace)
          else:
            self.key(self.ditspeed, self.charspace)
        self.space(self.charspace)
    self.space(self.wordspace)

# this is for diagnostic purposes only
def paris():
  count=0
  while True:
    word("PARIS")
    count+=1
    print(count)

parser = argparse.ArgumentParser(description='CW keyer for serial interface.')
parser.add_argument('-d', '--device', dest='device', default='/dev/ttyUSB0', help='Path to serial device. (default: /dev/ttyUSB0)')
parser.add_argument('-w', '--wpm', dest='wpm', type=int, default=20, help='CW keying speed in words per minutes. (default: 20 wpm)')
parser.add_argument('-t', '--text', dest='text', required=True, help='Text to transmit. Surround multiple words by quotes.')
parser.add_argument('--dtr', dest='dtr', action='store_true', help='Use DTR pin instead of RTS pin for keying.')
parser.add_argument('--invert', dest='invert', action='store_true', help='Invert logic signals on pin used for keying.')
parser.add_argument('--cut-nums',dest='cutnums',action='store_true',help='Use contest-style abbreviated numbers.')
args = parser.parse_args()

ser = serial.Serial(args.device, 9600)
if args.dtr:
  cw_key = ser.setDTR
else:
  cw_key = ser.setRTS

if args.invert:
  key_close = False
  key_open = True
else:
  key_close = True
  key_open = False

if args.cutnums:
  chars.update(cut_nums)

# iterate over the passed string as individual words
p = cw_text_parser(args.wpm)
for w in args.text.upper().split():
  p.word(w, args.wpm)
