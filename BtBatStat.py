import subprocess,re,time,sys,webbrowser,urllib2,decimal
from Foundation import NSDate,NSObject,NSTimer,NSRunLoop,NSDefaultRunLoopMode
from AppKit import NSImage,NSStatusBar,NSMenuItem,NSApplication,NSMenu,NSVariableStatusItemLength,NSRunAlertPanel
from PyObjCTools import AppHelper
from optparse import OptionParser

if len(sys.argv) > 1 and sys.argv[1][:4] == '-psn':
  del sys.argv[1]

VERSION = '0.8'
LONGVERSION = 'BtBatStat ' + VERSION

AboutText = """Writen by: Joris Vandalon
Code License: New BSD License

This software will always be free of charge.
Donation can be done via the website and will be much appreciated.
"""

updateText = "There is a new version of BtBatStat Available."
appUrl = 'http://code.google.com/p/btbatstat/'
updateUrl = 'http://code.google.com/p/btbatstat/downloads/list'

parser = OptionParser()
parser.add_option("-d", action="store_true", dest="debug")
(options, args)= parser.parse_args()

start_time = NSDate.date()

def versionCheck():
    try:
	LATEST = urllib2.urlopen("http://btbatstat.vandalon.org/VERSION", None, 2).read().strip()
    except:
	return False
    return ( LATEST and decimal.Decimal(LATEST) > decimal.Decimal(VERSION) )

#Check for new version
def checkForUpdates():
    if versionCheck():
	if NSRunAlertPanel(LONGVERSION, updateText , "Download Update", "Ignore for now", None ) == 1:
	    webbrowser.open(updateUrl)

class Timer(NSObject):
  def about_(self, notification):
    if versionCheck():
	AboutTitle = LONGVERSION + " (Update Available!)"
        about = NSRunAlertPanel(AboutTitle, AboutText , "OK", "Visit Website", "Download Update" )
    else:
        about = NSRunAlertPanel(LONGVERSION, AboutText , "OK", "Visit Website", None )
    if about == 0:
      webbrowser.open(appUrl)
    elif about == -1:
      webbrowser.open(updateUrl)
	
  def applicationDidFinishLaunching_(self, notification):
    #Create menu
    self.menu = NSMenu.alloc().init()

    self.barItem = dict()
    self.noDevice = False
    self.devicesFound = 0

    # Load images
    self.noDeviceImage = NSImage.alloc().initByReferencingFile_('icons/no_device.png')
    self.barImage = dict(kb = NSImage.alloc().initByReferencingFile_('icons/kb.png'),
			 magicMouse = NSImage.alloc().initByReferencingFile_('icons/magic_mouse.png'),
			 mightyMouse = NSImage.alloc().initByReferencingFile_('icons/mighty_mouse.png'),
			 magicTrackpad = NSImage.alloc().initByReferencingFile_('icons/TrackpadIcon.png'))

    #Define menu items
    self.statusbar = NSStatusBar.systemStatusBar()
    self.menuAbout = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About BtBatStat', 'about:', '')
    self.separator_menu_item = NSMenuItem.separatorItem()
    self.menuQuit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 10.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

    #Add menu items
    self.menu.addItem_(self.menuAbout)
    self.menu.addItem_(self.separator_menu_item)
    self.menu.addItem_(self.menuQuit)

    #Check for updates
    checkForUpdates()

  def ioreg(self, key, flags):
    return subprocess.Popen(["/usr/sbin/ioreg", flags, key], stdout=subprocess.PIPE).communicate()[0]

  def createBarItem(self, icon):
    barItem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    barItem.setImage_(icon)
    barItem.setHighlightMode_(1)
    barItem.setMenu_(self.menu)
    return barItem

  def tick_(self, notification):
    noDevice = False
    if options.debug:
	start = time.time()

    deviceCmd = dict( mightyMouse = self.ioreg("AppleBluetoothHIDMouse","-rc"),
	 	      magicMouse = self.ioreg("BNBMouseDevice","-rc"),
	 	      magicTrackpad = self.ioreg("BNBTrackpadDevice","-rc"))
    deviceCmd['kb'] = self.ioreg("AppleBluetoothHIDKeyboard","-rc")
    if not deviceCmd['kb']:
        deviceCmd['kb'] = self.ioreg("IOAppleBluetoothHIDDriver","-n")

    for device,Output in deviceCmd.items():
	if Output:
	    Percentage = re.search('BatteryPercent" = (\d{1,2})', Output)
	    if Percentage:
	        print Percentage
		if options.debug:
		    print "Found " + device
		self.devicesFound += 1
		if not device in self.barItem:
		    self.barItem[device] = self.createBarItem(self.barImage[device])
		self.barItem[device].setTitle_(Percentage.group(1) + '%')
	    elif device in self.barItem:
	    	self.statusbar.removeStatusItem_(self.barItem[device])
		del self.barItem[device]
    
    if options.debug:
	print "Found", self.devicesFound, "Devices."

    if self.devicesFound == 0 and self.noDevice == False:
	if options.debug:
	    print "Did not find any Apple BT devices..."
	self.noDevice = self.createBarItem(self.noDeviceImage)
        menuNotice = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('BtBatStat: No devices found.', '', '')
        self.menu.addItem_(menuNotice)
    elif self.devicesFound > 0 and self.noDevice == False:
	self.statusbar.removeStatusItem_(self.noDevice)
	self.noDevice == False

    if options.debug:
	end = time.time()
	print "Time elapsed = ", end - start, "seconds"

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
