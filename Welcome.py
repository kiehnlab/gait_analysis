import wx
import os
import datetime
from Video_analyser import Video_analyser
from Video_analyser_combined import Video_analyser_combined
from Speed_coord import S_C_profiler
from Load_project import loaded_S_C_profiler
from Group_analysis import Group_plotter
from Load_project_lateral import loaded_lateral_profiler
from Load_project_combined import loaded_combined_analysis


class Welcome(wx.Panel):
    def __init__(self,parent, gui_size):
        h = gui_size[0]
        w = gui_size[1]
        self.parent=parent
        self.gui_size=gui_size
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER,size=(w,h))
        sizer = wx.GridBagSizer(10,7)
        txt = 'Welcome to a tool for Locomotor Analysis!'
        self.welcome_txt = wx.StaticText(self,label = txt,style=wx.ALIGN_CENTRE)

        font = self.welcome_txt.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.welcome_txt.SetFont(font)
        sizer.Add(self.welcome_txt,pos=(1,11),flag = wx.ALIGN_CENTER_HORIZONTAL)



        self.select_opt = wx.RadioBox(
            self,
            label='Select origin of your project:',
            choices=['Create new project', 'Load existing project'],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        sizer.Add(self.select_opt,pos=(3,11),flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.select_mode = wx.RadioBox(
            self,
            label='Select type of analysis:',
            choices=['Bottom view', 'Lateral view','Combined view'],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        sizer.Add(self.select_mode, pos=(4,11),flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.image = wx.StaticBitmap(self,-1,wx.Bitmap('gait1.png',wx.BITMAP_TYPE_ANY))
        sizer.Add(self.image, pos=(5,11),flag=wx.ALIGN_CENTER_HORIZONTAL)



        self.start = wx.Button(self,label='START')
        sizer.Add(self.start,pos=(5,12),flag=wx.ALIGN_RIGHT)
        self.start.Bind(wx.EVT_BUTTON,self.On_start)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def On_start(self,event):
        if self.parent.GetPageCount() > 1:
            for i in range(self.parent.GetPageCount()-1,0,-1):
                self.parent.DeletePage(i)
                self.parent.SendSizeEvent()
        if self.select_opt.GetStringSelection() == 'Create new project':
            if self.select_mode.GetStringSelection() == 'Combined view':
                new_project = Video_analyser_combined(self.parent, self.gui_size,self.select_mode.GetStringSelection())
                self.parent.AddPage(new_project, 'Combined Video Analyser')
                self.parent.SetSelection(1)
            else:
                new_project = Video_analyser(self.parent,self.gui_size,self.select_mode.GetStringSelection())
                self.parent.AddPage(new_project,'Video Analyser')
                self.parent.SetSelection(1)
        elif self.select_opt.GetStringSelection() == 'Load existing project' and self.select_mode.GetStringSelection() == 'Bottom view':
            load_project = loaded_S_C_profiler(self.parent,self.gui_size)
            group_plot = Group_plotter(self.parent,self.gui_size)
            self.parent.AddPage(load_project,'Speed and Coordination')
            self.parent.AddPage(group_plot,'Group analysis')
            self.parent.SetSelection(1)
        elif self.select_opt.GetStringSelection() == 'Load existing project' and self.select_mode.GetStringSelection() == 'Lateral view':
            load_project = loaded_lateral_profiler(self.parent,self.gui_size)
            group_plot = Group_plotter(self.parent,self.gui_size)
            self.parent.AddPage(load_project,'Lateral analysis')
            self.parent.AddPage(group_plot,'Group analysis')
            self.parent.SetSelection(1)
        elif self.select_opt.GetStringSelection() == 'Load existing project' and self.select_mode.GetStringSelection() == 'Combined view':
            load_project = loaded_combined_analysis(self.parent, self.gui_size)
            group_plot = Group_plotter(self.parent, self.gui_size)
            self.parent.AddPage(load_project, 'Combined Video Analyser')
            self.parent.AddPage(group_plot, 'Group analysis')
            self.parent.SetSelection(1)

