#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Beremiz, a Integrated Development Environment for
# programming IEC 61131-3 automates supporting plcopen standard and CanFestival.
#
# Copyright (C) 2016 - 2017: Andrey Skvortsov <andrej.skvortzov@gmail.com>
#
# See COPYING file for copyrights details.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import os
import sys
import getopt

import wx
import wx.adv

import util.paths as paths


class Splash(wx.adv.SplashScreen):
    def __init__(self, app, bitmap,
                 splashStyle=wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_NO_TIMEOUT,
                 milliseconds=3000,
                 parent=None,
                 id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SIMPLE | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP):

        super().__init__(bitmap=bitmap, splashStyle=splashStyle,
                         milliseconds=milliseconds, parent=parent,
                         id=id, pos=pos, size=size, style=style)
        self.app = app
        self.Painted = False

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.timer = wx.Timer(self)
        self.timer.Start(2000)

        self.Bind(wx.EVT_TIMER, self.OnTimeOut, self.timer)

    def OnTimeOut(self, event: wx.TimerEvent):
        self.Close()

    def OnClose(self, event: wx.CloseEvent):
        event.Skip()
        self.Hide()

        if self.timer.IsRunning():
            # Stop the gauge timer.
            self.timer.Stop()

        if not self.Painted:
            self.Painted = True
            wx.CallAfter(self.app.AppStart)


class BeremizApp(wx.App):
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        super().SetAppName("beremiz")
        self.frame: wx.Frame = None
        self.updateinfo_url = None
        self.extensions = []
        self.app_dir = paths.AbsDir(__file__)
        self.projectOpen = None
        self.buildpath = None
        self.splash = None
        self.splashPath = self.Bpath("images", "splash.png")
        self.modules = ["BeremizIDE"]
        self.debug = os.path.exists("BEREMIZ_DEBUG")
        self.handle_exception = None

    def Bpath(self, *args):
        return os.path.join(self.app_dir, *args)

    def Usage(self):
        print("Usage:")
        print("%s [Options] [Projectpath] [Buildpath]" % sys.argv[0])
        print("")
        print("Supported options:")
        print("-h --help                    Print this help")
        print("-u --updatecheck URL         Retrieve update information by checking URL")
        print("-e --extend PathToExtension  Extend IDE functionality by loading at start additional extensions")
        print("")
        print("")

    def SetCmdOptions(self):
        self.shortCmdOpts = "hu:e:"
        self.longCmdOpts = ["help", "updatecheck=", "extend="]

    def ProcessOption(self, o, a):
        if o in ("-h", "--help"):
            self.Usage()
            sys.exit()
        if o in ("-u", "--updatecheck"):
            self.updateinfo_url = a
        if o in ("-e", "--extend"):
            self.extensions.append(a)

    def ProcessCommandLineArgs(self):
        self.SetCmdOptions()
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], self.shortCmdOpts, self.longCmdOpts)
        except getopt.GetoptError:
            # print help information and exit:
            self.Usage()
            sys.exit(2)

        for o, a in opts:
            self.ProcessOption(o, a)

        if len(args) > 2:
            self.Usage()
            sys.exit()

        elif len(args) == 1:
            self.projectOpen = args[0]
            self.buildpath = None
        elif len(args) == 2:
            self.projectOpen = args[0]
            self.buildpath = args[1]

    def ShowSplashScreen(self):
        bmp = wx.Image(self.splashPath).ConvertToBitmap()
        self.splash = Splash(app=self, bitmap=bmp)

    def BackgroundInitialization(self):
        self.InitI18n()
        self.CheckUpdates()
        self.LoadExtensions()
        self.ImportModules()

    def InitI18n(self):
        from util.misc import InstallLocalRessources
        InstallLocalRessources(self.app_dir)

    def globals(self):
        """
        allows customizations to specify what globals
        are passed to extensions
        """
        return globals()

    def locals(self):
        return locals()

    def LoadExtensions(self):
        for extfilename in self.extensions:
            from util.TranslationCatalogs import AddCatalog
            from util.BitmapLibrary import AddBitmapFolder
            extension_folder = os.path.split(os.path.realpath(extfilename))[0]
            sys.path.append(extension_folder)
            AddCatalog(os.path.join(extension_folder, "locale"))
            AddBitmapFolder(os.path.join(extension_folder, "images"))

            with open(extfilename, "rb") as source_file:
                code = compile(source_file.read(), extfilename, "exec")
            exec(code, self.globals(), self.locals())

    def CheckUpdates(self):
        if self.updateinfo_url is not None:
            self.updateinfo = _("Fetching %s") % self.updateinfo_url

            def updateinfoproc():
                try:
                    from urllib import request
                    self.updateinfo = request.urlopen(
                        self.updateinfo_url, None).read()
                except Exception:
                    self.updateinfo = _("update info unavailable.")

            from threading import Thread

            assert self.splash is not None

            self.splash.SetText(text=self.updateinfo)
            updateinfoThread = Thread(target=updateinfoproc)
            updateinfoThread.start()
            updateinfoThread.join(2)
            self.splash.SetText(text=self.updateinfo)

    def ImportModules(self):
        for modname in self.modules:
            mod = __import__(modname)
            setattr(self, modname, mod)

    def InstallExceptionHandler(self):
        import version
        import util.ExceptionHandler
        self.handle_exception = util.ExceptionHandler.AddExceptHook(
            version.app_version)

    def CreateUI(self):
        self.frame = self.BeremizIDE.Beremiz(
            None, self.projectOpen, self.buildpath)

    def CloseSplash(self):
        if self.splash:
            self.splash.Close()

    def ShowUI(self):
        if self.frame is not None:
            self.frame.Show()

    def PreStart(self):
        self.ProcessCommandLineArgs()
        self.ShowSplashScreen()

    def AppStart(self):
        try:
            self.BackgroundInitialization()
            self.CreateUI()
            self.CloseSplash()
            self.ShowUI()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            if self.handle_exception is not None:
                self.handle_exception(*sys.exc_info(), exit=True)
            else:
                raise

    def Start(self):
        self.PreStart()
        self.InstallExceptionHandler()
        self.MainLoop()


if __name__ == '__main__':
    beremiz = BeremizApp()
    beremiz.Start()
