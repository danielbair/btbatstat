#!/usr/bin/python

import subprocess,re,time,sys,webbrowser
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
from optparse import OptionParser

if len(sys.argv) > 1 and sys.argv[1][:4] == '-psn':
  del sys.argv[1]

debug = None
parser = OptionParser()
parser.add_option("-d", action="store_true", dest="debug")
(options, args)= parser.parse_args()

if options.debug is True:
  debug = 1

start_time = NSDate.date()

class Timer(NSObject):
  statusbar = None
  KeyBat = None
  MagicMouseBat = None
  MightyMouseBat = None
  TPBat = None
  noDevice = None

  # Load images
  kbImage = NSImage.alloc().initByReferencingFile_('kb.png')
  magicImage = NSImage.alloc().initByReferencingFile_('magic_mouse.png')
  mightyImage = NSImage.alloc().initByReferencingFile_('mighty_mouse.png')
  tpImage = NSImage.alloc().initByReferencingFile_('TrackpadIcon.png')
  noDeviceImage = NSImage.alloc().initByReferencingFile_('no_device.png')

  def website_(self, notification):
    webbrowser.open("http://code.google.com/p/btbatstat/")

  def applicationDidFinishLaunching_(self, notification):
    #Define menu items
    self.statusbar = NSStatusBar.systemStatusBar()
    menuAppName = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('BtBatStat', 'website:', '')
    self.separator_menu_item = NSMenuItem.separatorItem()
    menuQuit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')

    #Create menu
    self.menu = NSMenu.alloc().init()
    self.menu.addItem_(menuAppName)
    self.menu.addItem_(self.separator_menu_item)
    self.menu.addItem_(menuQuit)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 10.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def tick_(self, notification):
    if debug:
	start = time.time()

    KeyBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-n", "IOAppleBluetoothHIDDriver"], stdout=subprocess.PIPE).communicate()[0]
    KeyBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', KeyBatStatCmd)
    if KeyBatStatCmdOut:
	KeyBatStat = KeyBatStatCmdOut.group(1)
        if debug:
            print "Keyboard battery: ", KeyBatStat
    else:
	KeyBatStat = None

    MightyMouseBatStatCmd = subprocess.Popen(["ioreg", "-rc", "AppleBluetoothHIDMouse"], stdout=subprocess.PIPE).communicate()[0]
    if MightyMouseBatStatCmd:
    	MightyMouseBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', MightyMouseBatStatCmd)
	MightyMouseBatStat = MightyMouseBatStatCmdOut.group(1)
        if debug:
            print "Mighty Mouse battery: ", KeyBatStat
    else:
	MightyMouseBatStat = None

    MagicMouseBatStatCmd = subprocess.Popen(["ioreg", "-rc", "BNBMouseDevice"], stdout=subprocess.PIPE).communicate()[0]
    if MagicMouseBatStatCmd:
    	MagicMouseBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', MagicMouseBatStatCmd)
	MagicMouseBatStat = MagicMouseBatStatCmdOut.group(1)
        if debug:
            print "Magic Mouse battery: ", KeyBatStat
    else:
	MagicMouseBatStat = None

    TPBatStatCmd = subprocess.Popen(["ioreg", "-rc", "BNBTrackpadDevice"], stdout=subprocess.PIPE).communicate()[0]
    if TPBatStatCmd:
    	TPBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', TPBatStatCmd)
	TPBatStat = TPBatStatCmdOut.group(1)
        if debug:
            print "Trackpad battery: ", KeyBatStat
    else:
	TPBatStat = None

    if KeyBatStat:
      if self.KeyBat is None:
        self.KeyBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.KeyBat.setImage_(self.kbImage)
        self.KeyBat.setHighlightMode_(1)
        self.KeyBat.setMenu_(self.menu)
        if debug:
            print "No device found..."
      self.KeyBat.setTitle_(KeyBatStat +'%')
    elif self.KeyBat is not None:
      self.statusbar.removeStatusItem_(self.KeyBat)
      self.KeyBat = None

    if MightyMouseBatStat:
      if self.MightyMouseBat is None:
        self.MightyMouseBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.MightyMouseBat.setImage_(self.mightyImage)
        self.MightyMouseBat.setHighlightMode_(1)
        self.MightyMouseBat.setMenu_(self.menu)
      self.MightyMouseBat.setTitle_(MightyMouseBatStat +'%')
    elif self.MightyMouseBat is not None:
      self.statusbar.removeStatusItem_(self.MightyMouseBat)
      self.MightyMouseBat = None

    if MagicMouseBatStat:
      if self.MagicMouseBat is None:
        self.MagicMouseBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.MagicMouseBat.setImage_(self.magicImage)
        self.MagicMouseBat.setHighlightMode_(1)
        self.MagicMouseBat.setMenu_(self.menu)
      self.MagicMouseBat.setTitle_(MagicMouseBatStat +'%')
    elif self.MagicMouseBat is not None:
      self.statusbar.removeStatusItem_(self.MagicMouseBat)
      self.MagicMouseBat = None

    if TPBatStat:
      if self.TPBat is None:
        self.TPBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.TPBat.setImage_(self.tpImage)
        self.TPBat.setHighlightMode_(1)
        self.TPBat.setMenu_(self.menu)
      self.TPBat.setTitle_(TPBatStat +'%')
    elif self.TPBat is not None:
      self.statusbar.removeStatusItem_(self.TPBat)
      self.TPBat = None

    if self.MagicMouseBat is None and self.KeyBat is None and self.TPBat is None and self.noDevice is None:
	self.noDevice = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.noDevice.setImage_(self.noDeviceImage)
        self.noDevice.setHighlightMode_(1)
        self.noDevice.setMenu_(self.menu)
        self.noDevice.setToolTip_('BtBatStat: No Apple mouse or keyboard found!')
    elif (self.MagicMouseBat is not None or self.KeyBat is not None) and self.noDevice is not None:
	self.statusbar.removeStatusItem_(self.noDevice)
	self.noDevice = None

    if debug:
	end = time.time()
	print "Time elapsed = ", end - start, "seconds"

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
