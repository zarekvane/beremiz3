#!/usr/bin/env python
# -*- coding: utf-8 -*-

# See COPYING file for copyrights details.


import wx


# class RichMessageDialog is still not available in wxPython 3.0.2
class IDMergeDialog(wx.Dialog):
    def __init__(self, parent, title, question, optiontext, button_texts):
        super().__init__(parent, title=title)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        message = wx.StaticText(self, label=question)
        main_sizer.Add(message, border=20,
                             flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.LEFT | wx.RIGHT)

        self.check = wx.CheckBox(self, label=optiontext)
        main_sizer.Add(self.check, border=20,
                             flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for label, wxID in zip(button_texts, [wx.ID_YES, wx.ID_NO, wx.ID_CANCEL]):
            Button = wx.Button(self, label=label)

            def OnButtonFactory(_wxID):
                return lambda event: self.EndModal(_wxID)

            self.Bind(wx.EVT_BUTTON, OnButtonFactory(wxID), Button)
            buttons_sizer.Add(Button)

        main_sizer.Add(buttons_sizer, border=20,
                            flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT)

        self.SetSizer(main_sizer)
        self.Fit()

        self.Bind(wx.EVT_CHAR_HOOK, self.OnEscapeKey)

    def OnEscapeKey(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()

    def OptionChecked(self):
        return self.check.GetValue()
