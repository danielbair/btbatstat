import subprocess,re,time,sys,webbrowser,urllib2,decimal,threading
from Foundation import NSDate,NSObject,NSTimer,NSRunLoop,NSDefaultRunLoopMode
from AppKit import NSImage,NSStatusBar,NSMenuItem,NSApplication,NSMenu,NSVariableStatusItemLength,NSRunAlertPanel
from PyObjCTools import AppHelper
from optparse import OptionParser

if len(sys.argv) > 1 and sys.argv[1][:4] == '-psn':
  del sys.argv[1]

VERSION = '0.8'

AboutText = """Writen by: Joris Vandalon
Code License: New BSD License

This software will always be free of charge.
Donation can be done via the website and will be much appreciated.
"""

updateText = """There is a new version of BtBatStat Available.
"""

debug = None
parser = OptionParser()
parser.add_option("-d", action="store_true", dest="debug")
(options, args)= parser.parse_args()

if options.debug is True:
  debug = 1

start_time = NSDate.date()

def versionCheck():
    try:
	LATEST = urllib2.urlopen("http://btbatstat.vandalon.org/VERSION", None, 1).read().strip()
    except:
	return 0
    if LATEST and decimal.Decimal(LATEST) > decimal.Decimal(VERSION):
	return 1

#Check for new version
def checkForUpdates():
    if versionCheck():
	check = NSRunAlertPanel("BtBatStat 0.8", updateText , "Download Update", "Ignore for now", None )
	if check == 1:
	    webbrowser.open(self.updateUrl)

class Timer(NSObject):
  statusbar = None
  KeyBat = None
  MagicMouseBat = None
  MightyMouseBat = None
  TPBat = None
  noDevice = None
  appUrl = 'http://code.google.com/p/btbatstat/'
  updateUrl = 'http://code.google.com/p/btbatstat/downloads/list'


  # Load images
  kbImage = NSImage.alloc().initByReferencingFile_('icons/kb.png')
  magicImage = NSImage.alloc().initByReferencingFile_('icons/magic_mouse.png')
  mightyImage = NSImage.alloc().initByReferencingFile_('icons/mighty_mouse.png')
  tpImage = NSImage.alloc().initByReferencingFile_('icons/TrackpadIcon.png')
  noDeviceImage = NSImage.alloc().initByReferencingFile_('icons/no_device.png')

  #Define menu items
  statusbar = NSStatusBar.systemStatusBar()
  menuAbout = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About BtBatStat', 'about:', '')
  separator_menu_item = NSMenuItem.separatorItem()
  menuQuit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')

  def about_(self, notification):
    if versionCheck():
	AboutTitle = "BtBatstat " + VERSION + " (Update Available!)"
        about = NSRunAlertPanel(AboutTitle, AboutText , "OK", "Visit Website", "Download Update" )
    else:
	AboutTitle = "BtBatstat " + VERSION
        about = NSRunAlertPanel(AboutTitle, AboutText , "OK", "Visit Website", None )
    if about == 0:
      webbrowser.open(self.appUrl)
    elif about == -1:
      webbrowser.open(self.updateUrl)
	
  def applicationDidFinishLaunching_(self, notification):
    #Create menu
    self.menu = NSMenu.alloc().init()

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 10.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

    self.menu.addItem_(self.menuAbout)
    self.menu.addItem_(self.separator_menu_item)
    self.menu.addItem_(self.menuQuit)

    #Check for updates
    checkForUpdates()

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
        menuNotice = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('BtBatStat: No devices found.', '', '')
        self.menu.addItem_(menuNotice)
        self.noDevice.setMenu_(self.menu)
        self.noDevice.setToolTip_('BtBatStat: No devices found.')
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

