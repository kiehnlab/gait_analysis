import wx
import warnings
import os
warnings.filterwarnings("ignore")
import gait_analysis
#from Video_analyser import *
#from coordination.constants import *
#from coordination.profiler import *
#from coordination.plotter import *
#from Accel_plotter import *
#from coordination.plotter import *
#from coordination.coord import iqrMean, heurCircular
#from coordination.tools import videoMetadata
#from coordination.constants import *
#from coordination.accel import *


from gait_analysis.Video_analyser import *
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.profiler import *
from gait_analysis.coordination.plotter import *
from gait_analysis.Accel_plotter import *
from gait_analysis.coordination.plotter import *
from gait_analysis.coordination.coord import iqrMean, heurCircular
from gait_analysis.coordination.tools import videoMetadata
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.accel import *



class Group_plotter(wx.Panel):
    def __init__(self, parent, gui_size):
        self.group1 = []
        self.group2 = []
        self.group3 = []
        self.group4 = []

        self.parent = parent
        self.gui_size = gui_size
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))
        sizer = wx.GridBagSizer(10, 7)

        self.txt = wx.StaticText(self,label='Perform custom group analysis')
        font = self.txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.txt.SetFont(font)
        sizer.Add(self.txt,pos=(0,0),flag=wx.ALIGN_LEFT)

        line = wx.StaticLine(self)
        sizer.Add(line,pos=(1,0),span=(1,w), flag=wx.EXPAND | wx.BOTTOM, border =5)

        sb = wx.StaticBox(self, label='Select type of analysis:')
        sb_sizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        self.choices = wx.Choice(self, choices=['Single Group', 'Pairwise (2 Groups)',
                                                'Pairwise (3 Groups)', 'Pairwise (4 Groups)'])
        sb_sizer.Add(self.choices)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(3,1),span=(3,2),flag=wx.EXPAND)


        # txt = wx.StaticText(self,label='Select type of analysis:')
        # sizer.Add(txt,pos=(3,1),flag=wx.ALIGN_BOTTOM)
        # self.choices = wx.Choice(self,choices=['Single Group','Pairwise (2 Groups)',
        #                                      'Pairwise (3 Groups)','Pairwise (4 Groups)'])
        # sizer.Add(self.choices,pos=(4,1),flag=wx.ALIGN_TOP)

        self.txt = wx.StaticText(self, label='Group1:')
        font = self.txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.txt.SetFont(font)
        self.group_name1 = wx.TextCtrl(self)
        self.txt1 = wx.StaticText(self, label='Group name:')
        self.txt2 = wx.StaticText(self, label='Group members:')
        self.select_animals1 = wx.Button(self, label='Select animals')
        sizer.Add(self.select_animals1, pos=(3, 16), span=(0,9), flag=wx.TOP | wx.EXPAND, border=5)
        self.select_animals1.Bind(wx.EVT_BUTTON, self.select_group1)
        sizer.Add(self.txt1, pos=(2, 5),span=(0,10),flag=wx.EXPAND|wx.ALIGN_CENTER)
        sizer.Add(self.txt2, pos=(2, 16))
        sizer.Add(self.txt, pos=(3, 3),span=(0,1),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name1, pos=(3, 5), span=(0,10), flag=wx.EXPAND)
        self.group_name1.Enable(False)
        self.select_animals1.Enable(False)

        self.txt = wx.StaticText(self, label='Group2:')
        font = self.txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.txt.SetFont(font)
        self.group_name2 = wx.TextCtrl(self)
        self.select_animals2 = wx.Button(self, label='Select animals')
        sizer.Add(self.select_animals2, pos=(4, 16), span=(0,9), flag=wx.TOP | wx.EXPAND, border=5)
        self.select_animals2.Bind(wx.EVT_BUTTON, self.select_group2)
        sizer.Add(self.txt, pos=(4, 3),span=(0,1),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name2, pos=(4, 5), span=(0,10), flag=wx.EXPAND)
        self.group_name2.Enable(False)
        self.select_animals2.Enable(False)

        self.txt = wx.StaticText(self, label='Group3:')
        font = self.txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.txt.SetFont(font)
        self.group_name3 = wx.TextCtrl(self)
        self.select_animals3 = wx.Button(self, label='Select animals')
        sizer.Add(self.select_animals3, pos=(5, 16), span=(1,9), flag=wx.TOP | wx.EXPAND, border=5)
        self.select_animals3.Bind(wx.EVT_BUTTON, self.select_group3)
        sizer.Add(self.txt, pos=(5, 3),span=(0,1),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name3, pos=(5, 5), span=(0,10), flag=wx.EXPAND)
        self.group_name3.Enable(False)
        self.select_animals3.Enable(False)

        self.txt = wx.StaticText(self, label='Group4:')
        font = self.txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.txt.SetFont(font)
        self.group_name4 = wx.TextCtrl(self)
        self.select_animals4 = wx.Button(self, label='Select animals')
        sizer.Add(self.select_animals4, pos=(6, 16), span=(1,9), flag=wx.TOP | wx.EXPAND, border=5)
        self.select_animals4.Bind(wx.EVT_BUTTON, self.select_group4)
        sizer.Add(self.txt, pos=(6, 3),span=(0,1),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name4, pos=(6, 5), span=(0,10), flag=wx.EXPAND)
        self.group_name4.Enable(False)
        self.select_animals4.Enable(False)

        self.choices.Bind(wx.EVT_CHOICE,self.check)



        sb = wx.StaticBox(self, label='Select number of steps used for analysis:')
        sb_sizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        self.n_step = wx.SpinCtrlDouble(self, value='', min=1, max=100, initial=10, inc=1)
        sb_sizer.Add(self.n_step)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(10, 3))

        sb = wx.StaticBox(self, label='Select statistical test:')
        sb_sizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        self.stat_choice = wx.Choice(self, choices=['Watson-Williams test', 'Modified Rayleigh test'])
        sb_sizer.Add(self.stat_choice)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(10,5))

        sb = wx.StaticBox(self, label='Select type of sampling:')
        sb_sizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        self.sampling_choice = wx.Choice(self, choices=['Random Sampling', 'Density based sampling', 'Tail sampling'])
        sb_sizer.Add(self.sampling_choice)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(10,6))





        self.SetSizer(sizer)
        sizer.Fit(self)

    def select_group1(self, event):

        cwd = os.getcwd()
        dlg = wx.FileDialog(
            self, "Select videos to add to the project", cwd, "", "*.*", wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            vids = dlg.GetPaths()
            self.new_vids = []
            for i in vids:
                if i in self.group1:
                    continue
                else:
                    self.new_vids.append(i)
            self.group1 = self.group1 + self.new_vids
            self.select_animals1.SetLabel("Total %s Animals in current group" % len(self.group1))

    def select_group2(self, event):

        cwd = os.getcwd()
        dlg = wx.FileDialog(
            self, "Select videos to add to the project", cwd, "", "*.*", wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            vids = dlg.GetPaths()
            self.new_vids = []
            for i in vids:
                if i in self.group2:
                    continue
                else:
                    self.new_vids.append(i)
            self.group2 = self.group2 + self.new_vids
            self.select_animals2.SetLabel("Total %s Animals in current group" % len(self.group2))

    def select_group3(self, event):

        cwd = os.getcwd()
        dlg = wx.FileDialog(
            self, "Select videos to add to the project", cwd, "", "*.*", wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            vids = dlg.GetPaths()
            self.new_vids = []
            for i in vids:
                if i in self.group3:
                    continue
                else:
                    self.new_vids.append(i)
            self.group3 = self.group3 + self.new_vids
            self.select_animals3.SetLabel("Total %s Animals in current group" % len(self.group3))

    def select_group4(self, event):

        cwd = os.getcwd()
        dlg = wx.FileDialog(
            self, "Select videos to add to the project", cwd, "", "*.*", wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            vids = dlg.GetPaths()
            self.new_vids = []
            for i in vids:
                if i in self.group4:
                    continue
                else:
                    self.new_vids.append(i)
            self.group4 = self.group4 + self.new_vids
            self.select_animals4.SetLabel("Total %s Animals in current group" % len(self.group4))



    def check(self,event):
        if self.choices.GetCurrentSelection() == 0:
            self.group_name1.Enable(True)
            self.select_animals1.Enable(True)
            self.group_name2.Enable(False)
            self.select_animals2.Enable(False)
            self.group_name3.Enable(False)
            self.select_animals3.Enable(False)
            self.group_name4.Enable(False)
            self.select_animals4.Enable(False)
        elif self.choices.GetCurrentSelection() == 1:
            self.group_name1.Enable(True)
            self.select_animals1.Enable(True)
            self.group_name2.Enable(True)
            self.select_animals2.Enable(True)
            self.group_name3.Enable(False)
            self.select_animals3.Enable(False)
            self.group_name4.Enable(False)
            self.select_animals4.Enable(False)
        elif self.choices.GetCurrentSelection() == 2:
            self.group_name1.Enable(True)
            self.select_animals1.Enable(True)
            self.group_name2.Enable(True)
            self.select_animals2.Enable(True)
            self.group_name3.Enable(True)
            self.select_animals3.Enable(True)
            self.group_name4.Enable(False)
            self.select_animals4.Enable(False)
        elif self.choices.GetCurrentSelection() == 3:
            self.group_name1.Enable(True)
            self.select_animals1.Enable(True)
            self.group_name2.Enable(True)
            self.select_animals2.Enable(True)
            self.group_name3.Enable(True)
            self.select_animals3.Enable(True)
            self.group_name4.Enable(True)
            self.select_animals4.Enable(True)







