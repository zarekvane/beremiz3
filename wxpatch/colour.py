import wx

class HashableColour(wx.Colour):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
    
    def __hash__(self):
        return id(self)
