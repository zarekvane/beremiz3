import wx


def DrawRectangle(dc: wx.DC, x, y, width, height):
    dc.DrawRectangle(int(x), int(y), int(width), int(height))


def DrawLine(dc: wx.DC, x1, y1, x2, y2):
    dc.DrawLine(int(x1), int(y1), int(x2), int(y2))


def DrawText(dc: wx.DC, text, x, y):
    dc.DrawText(text, int(x), int(y))


def DrawCircle(dc: wx.DC, x, y, radius):
    dc.DrawCircle(int(x), int(y), int(radius))


def Point(x, y):
    return wx.Point(int(x), int(y))


def Rect(x, y, width, height):
    return wx.Rect(int(x), int(y), int(width), int(height))
