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
from gait_analysis.coordination.tools import videoMetadata,processDict
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.accel import *
from gait_analysis.coordination.groupCoord import Group_profiler



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
        sizer.Add(border, pos=(4,1),span=(3,1),flag=wx.EXPAND)


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
        sizer.Add(self.txt1, pos=(2, 3),flag=wx.EXPAND|wx.ALIGN_CENTER)
        sizer.Add(self.txt2, pos=(2, 16))
        sizer.Add(self.txt, pos=(3, 2),span=(0,1),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name1, pos=(3, 3), span=(0,12), flag=wx.EXPAND)
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
        sizer.Add(self.txt, pos=(4, 2),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name2, pos=(4, 3), span=(0,12), flag=wx.EXPAND)
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
        sizer.Add(self.txt, pos=(5, 2),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name3, pos=(5, 3), span=(0,12), flag=wx.EXPAND)
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
        sizer.Add(self.txt, pos=(6, 2),flag=wx.ALIGN_RIGHT)
        sizer.Add(self.group_name4, pos=(6,3), span=(0,12), flag=wx.EXPAND)
        self.group_name4.Enable(False)
        self.select_animals4.Enable(False)

        self.choices.Bind(wx.EVT_CHOICE,self.check)

        sb1 = wx.StaticBox(self, label='Options:')
        sb_sizer1 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        hbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        sb2 = wx.StaticBox(self, label='Select number of steps used for analysis:')
        sb_sizer2 = wx.StaticBoxSizer(sb2, wx.HORIZONTAL)
        self.n_step = wx.SpinCtrlDouble(self, value='', min=1, max=150, initial=10, inc=5)
        sb_sizer2.Add(self.n_step,10,flag=wx.EXPAND,border=5)

        # sizer.Add(border, pos=(10, 2))



        stat_test = wx.StaticBox(self, label='Select statistical test:')
        stat_test_sizer = wx.StaticBoxSizer(stat_test, wx.HORIZONTAL)
        self.stat_choice = wx.Choice(self, choices=['Watson-Williams test', 'Modified Rayleigh test'])
        stat_test_sizer.Add(self.stat_choice,10,flag=wx.EXPAND,border=5)

        # sizer.Add(border, pos=(10,3))
        #
        sampling = wx.StaticBox(self, label='Select type of sampling:')
        sampling_sizer = wx.StaticBoxSizer(sampling, wx.HORIZONTAL)
        self.sampling_choice = wx.Choice(self, choices=['Random Sampling', 'Density based sampling', 'Tail sampling'])
        sampling_sizer.Add(self.sampling_choice,10,flag=wx.EXPAND,border=5)
        # sizer.Add(border, pos=(10,1))
        #
        phi_thr = wx.StaticBox(self, label='Select phi threshold:')
        phi_thr_sizer = wx.StaticBoxSizer(phi_thr, wx.HORIZONTAL)
        self.phi_thresh = wx.SpinCtrlDouble(self, value='', min=0.1, max=3.0, initial=0.5, inc=0.1)
        phi_thr_sizer.Add(self.phi_thresh,10,flag=wx.EXPAND,border=5)
        # sizer.Add(border, pos=(10, 4))
        #




        hbox1.Add(sampling_sizer,0,flag=wx.EXPAND,border=5)
        hbox1.Add(sb_sizer2,0,flag=wx.EXPAND,border=5)
        hbox1.Add(stat_test_sizer,0,flag=wx.EXPAND,border=5)
        hbox1.Add(phi_thr_sizer,0,flag=wx.EXPAND,border=5)


        stride_type = wx.StaticBox(self,label='Select stride type:')
        stride_type_sizer = wx.StaticBoxSizer(stride_type,wx.VERTICAL)
        self.check_list1 = wx.CheckListBox(self, choices=['Hindlimb("LH_RH")','Forelimb("LF_RF")',
                                                          'Homolateral left("LF_LH")'
                                                          ])
        # sizer.Add(self.check_list1, pos=(11, 3), flag=wx.ALIGN_RIGHT)
        self.check_list2 = wx.CheckListBox(self, choices=['Homolateral right("RH_RF")',
                                                          'Contra-lateral frontleft-hindright("LF_RH")',
                                                          'Contra-lateral frontright-hindleft("LH_RF")'
                                                          ])
        # sizer.Add(self.check_list2, pos=(11, 4), flag=wx.EXPAND)

        self.check_all = wx.CheckBox(self, label='Select all')
        self.check_all.Bind(wx.EVT_CHECKBOX, self.Select_all)
        # sizer.Add(self.check_all, pos=(11, 5))
        stride_type_sizer.Add(self.check_list1, 10, flag=wx.EXPAND, border=5)
        stride_type_sizer.Add(self.check_list2, 10, flag=wx.EXPAND, border=5)
        stride_type_sizer.Add(self.check_all, 10, flag=wx.ALIGN_RIGHT | wx.ALIGN_TOP, border=5)
        hbox2.Add(stride_type_sizer,0,border=5)

        sb_sizer1.Add(hbox1)
        sb_sizer1.Add(hbox2)
        sizer.Add(sb_sizer1,pos=(10,3),span=(0,12),flag=wx.EXPAND)

        test = wx.Button(self,label='Test')
        test.Bind(wx.EVT_BUTTON,self.test)
        sizer.Add(test,pos=(12,16),span=(0,9),flag=wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def test(self,event):
        groups = [self.group1,self.group2,self.group3,self.group4]
        names = [self.group_name1.GetValue(),self.group_name2.GetValue(),
                 self.group_name3.GetValue(),self.group_name4.GetValue()]
        if self.check_all.IsChecked() == True:
            combination = [i for i in range(6)]
        else:
            check1 = [i for i in self.check_list1.GetChecked()]
            check2 = [i + 3 for i in self.check_list2.GetChecked()]
            combination = check1 + check2
        Group_profiler(groups,names,combination,n_steps=int(self.n_step.GetValue()),phi_thr=self.phi_thresh.GetValue(),test=self.stat_choice.GetStringSelection())
        dlg = wx.MessageDialog(self,message='Group analysis finished!',style=wx.OK)
        dlg.ShowModal()

    def Select_all(self,event):
        if self.check_all.IsChecked() == True:
            for i in range(3):
                self.check_list1.Check(i,False)
                self.check_list2.Check(i,False)
            self.check_list1.Enable(False)
            self.check_list2.Enable(False)
        else:
            self.check_list1.Enable(True)
            self.check_list2.Enable(True)

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







