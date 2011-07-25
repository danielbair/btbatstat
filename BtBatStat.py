#!/usr/bin/python

import subprocess,re
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

start_time = NSDate.date()


class Timer(NSObject):
  statusbar = None

  # Load images
  kbImageRaw = "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".decode('base64')
  kbImageData = NSData.alloc().initWithBytes_length_(kbImageRaw, len(kbImageRaw))
  kbImage = NSImage.alloc().initWithData_(kbImageData)

  mouseImageRaw = "iVBORw0KGgoAAAANSUhEUgAAAAsAAAAPCAYAAAAyPTUwAAADHmlDQ1BJQ0MgUHJvZmlsZQAAeAGFVN9r01AU/tplnbDhizpnEQk+aJFuZFN0Q5y2a1e6zVrqNrchSJumbVyaxiTtfrAH2YtvOsV38Qc++QcM2YNve5INxhRh+KyIIkz2IrOemzRNJ1MDufe73/nuOSfn5F6g+XFa0xQvDxRVU0/FwvzE5BTf8gFeHEMr/GhNi4YWSiZHQA/Tsnnvs/MOHsZsdO5v36v+Y9WalQwR8BwgvpQ1xCLhWaBpXNR0E+DWie+dMTXCzUxzWKcECR9nOG9jgeGMjSOWZjQ1QJoJwgfFQjpLuEA4mGng8w3YzoEU5CcmqZIuizyrRVIv5WRFsgz28B9zg/JfsKiU6Zut5xCNbZoZTtF8it4fOX1wjOYA1cE/Xxi9QbidcFg246M1fkLNJK4RJr3n7nRpmO1lmpdZKRIlHCS8YlSuM2xp5gsDiZrm0+30UJKwnzS/NDNZ8+PtUJUE6zHF9fZLRvS6vdfbkZMH4zU+pynWf0D+vff1corleZLw67QejdX0W5I6Vtvb5M2mI8PEd1E/A0hCgo4cZCjgkUIMYZpjxKr4TBYZIkqk0ml0VHmyONY7KJOW7RxHeMlfDrheFvVbsrj24Pue3SXXjrwVhcW3o9hR7bWB6bqyE5obf3VhpaNu4Te55ZsbbasLCFH+iuWxSF5lyk+CUdd1NuaQU5f8dQvPMpTuJXYSWAy6rPBe+CpsCk+FF8KXv9TIzt6tEcuAcSw+q55TzcbsJdJM0utkuL+K9ULGGPmQMUNanb4kTZyKOfLaUAsnBneC6+biXC/XB567zF3h+rkIrS5yI47CF/VFfCHwvjO+Pl+3b4hhp9u+02TrozFa67vTkbqisXqUj9sn9j2OqhMZsrG+sX5WCCu0omNqSrN0TwADJW1Ol/MFk+8RhAt8iK4tiY+rYleQTysKb5kMXpcMSa9I2S6wO4/tA7ZT1l3maV9zOfMqcOkb/cPrLjdVBl4ZwNFzLhegM3XkCbB8XizrFdsfPJ63gJE722OtPW1huos+VqvbdC5bHgG7D6vVn8+q1d3n5H8LeKP8BqkjCtbCoV8yAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA/0lEQVQoFZWRMU7DQBBFd8YuIiTXUKXkCG7SIToaJCp67gEXAYkDcAaOElEgpXVhFDlhh/cdU2zkSLDSeHbmv/273rW2bS/d/TGldGVmF+Rt0zRvfd/f5ZwXEbEh3omnGvAFaEURgAlg23XdM9MbtAX5nHyPvPSqqlaCWGA0lWvKnfJUm3Rx9TdDLIFpFjgADTgN1Im8p+dgIfGakGMgukRcPpnfTu6Z3ugu+JWgDjQLcz4RZ175V4pDX7r8dK4lk3KMPrR+86TWbJdL8nSlY/hpuVT+DGrZv+Hx5coNZ6vgouzon2fBwwtzpx/zctkVpzM/EOtpg+Mj6aW0ai3uB2i3ch0QNwSSAAAAAElFTkSuQmCC".decode('base64')
  mouseImageData = NSData.alloc().initWithBytes_length_(mouseImageRaw, len(mouseImageRaw))
  mouseImage = NSImage.alloc().initWithData_(mouseImageData) 

  def applicationDidFinishLaunching_(self, notification):
    self.statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.MouseBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    self.KeyBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    # Set initial image
    self.KeyBat.setImage_(self.kbImage)
    self.MouseBat.setImage_(self.mouseImage)

    #Context Menu
    self.KeyBat.setHighlightMode_(1)
    self.MouseBat.setHighlightMode_(1)
    self.menu = NSMenu.alloc().init()
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)
    self.KeyBat.setMenu_(self.menu)
    self.MouseBat.setMenu_(self.menu)

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
      self.MouseBat.setTitle_(MouseBatStat +'%')
    elif self.MouseBat is not None:
      self.statusbar.removeStatusItem_(self.MouseBat)
      self.MouseBat = None

    if KeyBatStat:
      if self.KeyBat is None:
        self.KeyBat = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
	self.KeyBat.setImage_(self.kbImage)
      self.KeyBat.setTitle_(KeyBatStat +'%')
    elif self.KeyBat is not None:
      self.statusbar.removeStatusItem_(self.KeyBat)
      self.KeyBat = None

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
