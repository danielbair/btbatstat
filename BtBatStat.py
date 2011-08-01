import subprocess,re,time,sys,webbrowser
from Foundation import NSDate,NSObject,NSTimer,NSRunLoop,NSDefaultRunLoopMode
from AppKit import NSImage,NSStatusBar,NSMenuItem,NSApplication,NSMenu,NSVariableStatusItemLength
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
  kbImage = NSImage.alloc().initByReferencingFile_('icons/kb.png')
  magicImage = NSImage.alloc().initByReferencingFile_('icons/magic_mouse.png')
  mightyImage = NSImage.alloc().initByReferencingFile_('icons/mighty_mouse.png')
  tpImage = NSImage.alloc().initByReferencingFile_('icons/TrackpadIcon.png')
  noDeviceImage = NSImage.alloc().initByReferencingFile_('icons/no_device.png')

  #Define menu items
  statusbar = NSStatusBar.systemStatusBar()
  menuAppName = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('BtBatStat', 'website:', '')
  separator_menu_item = NSMenuItem.separatorItem()
  menuQuit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')

  def website_(self, notification):
    webbrowser.open("http://code.google.com/p/btbatstat/")

  def applicationDidFinishLaunching_(self, notification):
    #Create menu
    self.menu = NSMenu.alloc().init()
    self.menu.addItem_(self.menuAppName)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 10.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

    self.menu.addItem_(self.separator_menu_item)
    self.menu.addItem_(self.menuQuit)

  def tick_(self, notification):
    if debug:
	start = time.time()

    devicesFound = 0

    KeyBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-rc", "AppleBluetoothHIDKeyboard"], stdout=subprocess.PIPE).communicate()[0]
    if not KeyBatStatCmd:
        KeyBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-n", "IOAppleBluetoothHIDDriver"], stdout=subprocess.PIPE).communicate()[0]
    KeyBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', KeyBatStatCmd)
    if KeyBatStatCmdOut:
	if debug:
	    print "Found Apple BT Keyboard..."
	devicesFound += 1
	KeyBatStat = KeyBatStatCmdOut.group(1)
    else:
	KeyBatStat = None

    MightyMouseBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-rc", "AppleBluetoothHIDMouse"], stdout=subprocess.PIPE).communicate()[0]
    MightyMouseBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', MightyMouseBatStatCmd)
    if MightyMouseBatStatCmdOut:
	if debug:
	    print "Found Apple BT Mighty Mouse..."
	devicesFound += 1
	MightyMouseBatStat = MightyMouseBatStatCmdOut.group(1)
    else:
	MightyMouseBatStat = None

    MagicMouseBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-rc", "BNBMouseDevice"], stdout=subprocess.PIPE).communicate()[0]
    MagicMouseBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', MagicMouseBatStatCmd)
    if MagicMouseBatStatCmdOut:
	if debug:
	    print "Found Apple BT Magic Mouse..."
	devicesFound += 1
	MagicMouseBatStat = MagicMouseBatStatCmdOut.group(1)
    else:
	MagicMouseBatStat = None

    TPBatStatCmd = subprocess.Popen(["/usr/sbin/ioreg", "-rc", "BNBTrackpadDevice"], stdout=subprocess.PIPE).communicate()[0]
    TPBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', TPBatStatCmd)
    if TPBatStatCmdOut:
	if debug:
	    print "Found Apple BT Magic Trackpad..."
	devicesFound += 1
	TPBatStat = TPBatStatCmdOut.group(1)
    else:
	TPBatStat = None

    if KeyBatStat:
      if self.KeyBat is None:
        self.KeyBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.KeyBat.setImage_(self.kbImage)
        self.KeyBat.setHighlightMode_(1)
        self.KeyBat.setMenu_(self.menu)
      self.KeyBat.setTitle_(KeyBatStat + '%')
    elif self.KeyBat is not None:
      self.statusbar.removeStatusItem_(self.KeyBat)
      self.KeyBat = None

    if MightyMouseBatStat is not None:
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

    if debug:
	print "Found", devicesFound, "Devices."

    if devicesFound == 0 and self.noDevice is None:
	if debug:
	    print "Did not found any Apple BT devices..."
	self.noDevice = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.noDevice.setImage_(self.noDeviceImage)
        self.noDevice.setHighlightMode_(1)
        self.menu.removeItem_(self.menuAppName)
        menuAppName = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('BtBatStat: No Apple bluetooth input device found.', '', '')
        self.menu.addItem_(menuAppName)
        self.noDevice.setMenu_(self.menu)
        self.noDevice.setToolTip_('BtBatStat: No Apple bluetooth input device found.')
    elif devicesFound > 0 and self.noDevice is not None:
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

