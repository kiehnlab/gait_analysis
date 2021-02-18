import wx
import os
import datetime
from Video_analyser import Video_analyser
from Speed_coord import S_C_profiler
from Load_project import loaded_S_C_profiler


class Welcome(wx.Panel):
    def __init__(self,parent, gui_size):
        h = gui_size[0]
        w = gui_size[1]
        self.parent=parent
        self.gui_size=gui_size
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER,size=(w,h))
        sizer = wx.GridBagSizer(10,7)
        txt = 'Welcome to gait analysis for Kiehn Lab!'
        self.welcome_txt = wx.StaticText(self,label = txt,style=wx.ALIGN_CENTRE)

        font = self.welcome_txt.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.welcome_txt.SetFont(font)
        sizer.Add(self.welcome_txt,pos=(1,7),flag = wx.ALIGN_CENTER_HORIZONTAL)

        self.select_opt = wx.RadioBox(
            self,
            label='',
            choices=['Create new project', 'Load existing project'],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        sizer.Add(self.select_opt, pos=(3,7),flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.image = wx.StaticBitmap(self,-1,wx.Bitmap('gait1.png',wx.BITMAP_TYPE_ANY))
        sizer.Add(self.image, pos=(5,7),flag=wx.ALIGN_CENTER_HORIZONTAL)



        self.start = wx.Button(self,label='START')
        sizer.Add(self.start,pos=(6,7),flag=wx.ALIGN_RIGHT)
        self.start.Bind(wx.EVT_BUTTON,self.On_start)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def On_start(self,event):
        if self.select_opt.GetStringSelection() == 'Create new project':
            new_project = Video_analyser(self.parent,self.gui_size)
            self.parent.AddPage(new_project,'Video Analyser')
        else:
            load_project = loaded_S_C_profiler(self.parent,self.gui_size)
            self.parent.AddPage(load_project,'Speed and Coordination')