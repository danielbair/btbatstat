#!/usr/bin/python

import subprocess,re
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

start_time = NSDate.date()


class Timer(NSObject):
  statusbar = None
  KeyBat = None
  MouseBat = None
  noDevice = None

  # Load images
  kbImage = NSImage.alloc().initByReferencingFile_('kb.png')
  mouseImage = NSImage.alloc().initByReferencingFile_('mouse.png')
  noDeviceImage = NSImage.alloc().initByReferencingFile_('no_device.png')

  def applicationDidFinishLaunching_(self, notification):
    self.statusbar = NSStatusBar.systemStatusBar()
    self.menu = NSMenu.alloc().init()
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 5.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def tick_(self, notification):
    KeyBatStatCmd = subprocess.Popen(["ioreg -n 'IOAppleBluetoothHIDDriver'"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    KeyBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', KeyBatStatCmd)
    if KeyBatStatCmdOut:
	KeyBatStat = KeyBatStatCmdOut.group(1)
    else:
	KeyBatStat = None

    MouseBatStatCmd = subprocess.Popen(["ioreg -rc 'AppleBluetoothHIDMouse'"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    if MouseBatStatCmd == "":
        MouseBatStatCmd = subprocess.Popen(["ioreg -rc 'BNBMouseDevice'"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    MouseBatStatCmdOut = re.search('BatteryPercent" = (\d{1,2})', MouseBatStatCmd)
    if MouseBatStatCmdOut:
	MouseBatStat = MouseBatStatCmdOut.group(1)
    else:
	MouseBatStat = None

    if MouseBatStat:
      if self.MouseBat is None:
        self.MouseBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.MouseBat.setImage_(self.mouseImage)
        self.MouseBat.setHighlightMode_(1)
        self.MouseBat.setMenu_(self.menu)
      self.MouseBat.setTitle_(MouseBatStat +'%')
    elif self.MouseBat is not None:
      self.statusbar.removeStatusItem_(self.MouseBat)
      self.MouseBat = None

    if KeyBatStat:
      if self.KeyBat is None:
        self.KeyBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.KeyBat.setImage_(self.kbImage)
        self.KeyBat.setHighlightMode_(1)
        self.KeyBat.setMenu_(self.menu)
      self.KeyBat.setTitle_(KeyBatStat +'%')
    elif self.KeyBat is not None:
      self.statusbar.removeStatusItem_(self.KeyBat)
      self.KeyBat = None

    if self.MouseBat is None and self.KeyBat is None:
	self.noDevice = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.noDevice.setImage_(self.noDeviceImage)
        self.noDevice.setHighlightMode_(1)
        self.noDevice.setMenu_(self.menu)
        self.noDevice.setToolTip_('BtBatStat: No Apple mouse or keyboard found!')
    elif (self.MouseBat is not None or self.KeyBat is not None) and self.noDevice is not None:
	self.statusbar.removeStatusItem_(self.noDevice)
	self.noDevice = None	

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
