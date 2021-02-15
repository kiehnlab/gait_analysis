import wx
import os
import datetime


class Welcome(wx.Panel):
    def __init__(self,parent, gui_size):
        h = gui_size[0]
        w = gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER,size=(w,h))
        sizer = wx.GridBagSizer(10,7)
        txt = 'Welcome to gait analysis for Kiehn Lab!'
        self.welcome_txt = wx.StaticText(self,label = txt,style=wx.ALIGN_CENTRE)

        font = self.welcome_txt.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.welcome_txt.SetFont(font)
        sizer.Add(self.welcome_txt,pos=(0,16),flag = wx.CENTER)

        self.ole = wx.StaticBitmap(self,-1,wx.Bitmap('mice.jpg',wx.BITMAP_TYPE_ANY))
        sizer.Add(self.ole, pos=(1,16),flag=wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)