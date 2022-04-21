from overrides import overrides
import wx
from wx.lib.agw.advancedsplash import AdvancedSplash

class Splash(AdvancedSplash):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.Painted = False

    @overrides
    def OnPaint(self, event: wx.PaintEvent):
        super().OnPaint(event)

        if not self.Painted:
            self.Painted = True
            wx.CallAfter(self.app.AppStart)

    @overrides
    def SetTextFont(self, font=None):
        if font is None:
            font = wx.Font(wx.FontInfo(10).Bold().Underlined())
        super().SetTextFont(font)
