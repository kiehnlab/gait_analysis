import wx
#from Video_analyser import *
#from coordination.constants import *
#from coordination.profiler import *
#from coordination.plotter import *
#from Accel_plotter import *

from gait_analysis.Video_analyser import *
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.profiler import *
from gait_analysis.coordination.plotter import *
from gait_analysis.Accel_plotter import *

class S_C_profiler(wx.Panel):
    def __init__(self, parent, gui_size,proj_path):
        self.proj_path = proj_path
        self.parent = parent
        self.gui_size = gui_size
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))

        top_sizer = wx.BoxSizer(wx.VERTICAL)

        self.intro_txt = wx.StaticText(self,
                                       label=' Step2 : Perform speed, acceleration and coordination analysis.')
        font = self.intro_txt.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        self.intro_txt.SetFont(font)
        top_sizer.Add(self.intro_txt, 0, wx.ALL, 5)

        sizer = wx.GridBagSizer(10,7)
        sizer.Add(top_sizer,pos=(0,0))

        line = wx.StaticLine(self)
        sizer.Add(line, pos=(1, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt1 = wx.StaticText(self,label = 'Part1: Create speed profiles.')
        font = txt1.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt1.SetFont(font)
        sizer.Add(txt1,pos=(2,0),flag=wx.EXPAND)


        # self.save_np = wx.RadioBox(
        #     self,
        #     label='Want to save results as numpy table?',
        #     choices=['No','Yes'],
        #     majorDimension=1,
        #     style = wx.RA_SPECIFY_COLS,
        # )
        # sizer.Add(self.save_np,pos=(3,0),flag=wx.EXPAND)

        self.save_plot = wx.RadioBox(
            self,
            label='Want to save speed profile plot?',
            choices=['Yes','No'],
            majorDimension=1,
            style = wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_plot,pos=(3,1),flag=wx.EXPAND)

        self.save_log = wx.RadioBox(
            self,
            label='Want to save results as csv(Excel) table?',
            choices=['Yes','No'],
            majorDimension=1,
            style = wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_log,pos=(3,2),flag=wx.EXPAND)

        sb = wx.StaticBox(self, label='Select noise filter parameter')
        self.boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.SpeedSmFactor = wx.SpinCtrlDouble(self, value='', min=1, max=20, initial=10, inc=1)
        hbox1.Add(self.SpeedSmFactor)

        self.boxsizer.Add(hbox1)
        sizer.Add(self.boxsizer, pos=(3, 0), flag=wx.EXPAND)

        sb = wx.StaticBox(self,label='Specify treadmill length(cm): \n(If not, 20 cm assumed)')
        sb_sizer = wx.StaticBoxSizer(sb,wx.HORIZONTAL)
        border = wx.BoxSizer()

        self.tread_length = wx.SpinCtrlDouble(self, value='', min=10, max=30, initial=20, inc=1)
        self.tread_length.Enable(False)
        self.tread_length_check = wx.CheckBox(self,label='')
        self.tread_length_check.Bind(wx.EVT_CHECKBOX,self.Check_tread_length)
        sb_sizer.Add(self.tread_length_check)
        sb_sizer.Add(self.tread_length)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(4,0),flag=wx.EXPAND | wx.ALIGN_RIGHT)

        sb = wx.StaticBox(self,label='Specify treadmill speed (cm/s): (If not,assumed from\n the title of the video)')
        sb_sizer = wx.StaticBoxSizer(sb,wx.HORIZONTAL)
        border = wx.BoxSizer()

        self.tread_speed_check = wx.CheckBox(self,label='')
        self.tread_speed = wx.SpinCtrlDouble(self, value='', min=10, max=100, initial=20, inc=5)
        self.tread_speed.Enable(False)
        self.tread_speed_check.Bind(wx.EVT_CHECKBOX,self.Check_tread_speed)
        sb_sizer.Add(self.tread_speed_check)
        sb_sizer.Add(self.tread_speed)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(4,1))


        # self.check = wx.Button(self,label='Run speed analysis!')
        # sizer.Add(self.check,pos=(4,2),flag=wx.ALIGN_RIGHT)
        # self.check.Bind(wx.EVT_BUTTON,self.locomotion)


        line1 = wx.StaticLine(self)
        sizer.Add(line1, pos=(6, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt3 = wx.StaticText(self, label='Part2: Create acceleration plots with drag and recovery events')
        font = txt3.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt3.SetFont(font)
        sizer.Add(txt3, pos=(7, 0))

        # tThresh_txt = wx.StaticText(self, label='Specify duration to count a drag/recovery event.')
        # sizer.Add(tThresh_txt, pos=(8, 0), flag=wx.TOP)

        sb = wx.StaticBox(self,label='Specify duration for a drag/recovery event:')
        sb_sizer = wx.StaticBoxSizer(sb,wx.VERTICAL)
        border = wx.BoxSizer()

        self.tThresh = wx.SpinCtrlDouble(self, value='', min=0, max=1, initial=0.25, inc=0.05)
        sb_sizer.Add(self.tThresh,wx.EXPAND)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(8, 0), flag=wx.EXPAND)

        self.save_plot_acc = wx.RadioBox(
            self,
            label='Want to save acceleration profile plot?',
            choices=['Yes', 'No'],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_plot_acc, pos=(8,1), span=wx.DefaultSpan, flag=wx.EXPAND)

        # self.accel = wx.Button(self, label='Run acceleration analysis')
        # sizer.Add(self.accel, pos=(8, 2), flag=wx.ALIGN_RIGHT)
        # self.accel.Bind(wx.EVT_BUTTON,self.acceleration)

        line2 = wx.StaticLine(self)
        sizer.Add(line2, pos=(9, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt2 = wx.StaticText(self, label='Part3: Create cadence plots and circular plot.')
        font = txt2.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt2.SetFont(font)
        sizer.Add(txt2, pos=(10, 0), flag=wx.TOP)

        # self.select_opt_stride = wx.RadioBox(
        #     self,
        #     label='Select stride combination:',
        #     choices=['Homolateral right("RH_RF")','Contra-lateral frontleft-hindright("LF_RH")','Hindlimb("LH_RH")',
        #              'Homolateral left("LF_LH")','Contra-lateral frontright-hindleft("LH_RF")','Forelimb("LF_RF")'],
        #     majorDimension=3,
        #     style=wx.RA_SPECIFY_COLS,
        # )
        # sizer.Add(self.select_opt_stride,pos=(13,0),span=(0,1))
        sb1 = wx.StaticBox(self,label='Select stride combination')
        sb_sizer1 = wx.StaticBoxSizer(sb1,wx.VERTICAL)
        border1 = wx.BoxSizer(wx.HORIZONTAL)

        self.check_list1 = wx.CheckListBox(self, choices=['Homolateral right("RH_RF")',
                                                          'Contra-lateral frontleft-hindright("LF_RH")',
                                                          'Hindlimb("LH_RH")'])
        sizer.Add(self.check_list1, pos=(11, 0), flag=wx.ALIGN_RIGHT)
        self.check_list2 = wx.CheckListBox(self, choices=['Homolateral left("LF_LH")',
                                                          'Contra-lateral frontright-hindleft("LH_RF")',
                                                          'Forelimb("LF_RF")'])
        sizer.Add(self.check_list2, pos=(11, 1), flag=wx.EXPAND)

        self.check_all = wx.CheckBox(self, label='Select all')
        self.check_all.Bind(wx.EVT_CHECKBOX, self.Select_all)
        sizer.Add(self.check_all, pos=(11, 2))




        # cadence_txt = wx.Button(self,label='Run coordination analysis')
        # sizer.Add(cadence_txt,pos=(11,2),flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        # cadence_txt.Bind(wx.EVT_BUTTON,self.cadence)

        run_button = wx.Button(self,label='Run')
        sizer.Add(run_button,pos=(12,2),flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        run_button.Bind(wx.EVT_BUTTON,self.buttom_view)


        self.SetSizer(sizer)
        sizer.Fit(self)


    def buttom_view(self,event):
        n_grid = 0
        save_speed = False
        save_acc = False

        if self.save_plot.GetStringSelection() == 'Yes':
            n_grid += 1
            save_speed = True
        if self.save_plot_acc.GetStringSelection() == 'Yes':
            n_grid += 1
            save_acc = True
        if self.check_all.IsChecked() == True:
            self.combination = ['Homolateral right("RH_RF")', 'Contra-lateral frontleft-hindright("LF_RH")',
                                'Hindlimb("LH_RH")',
                                'Homolateral left("LF_LH")', 'Contra-lateral frontright-backleft("LH_RF")',
                                'Forelimb("LF_RF")']
        else:
            self.combination = self.check_list1.GetCheckedStrings() + self.check_list2.GetCheckedStrings()

        if self.tread_speed_check.IsChecked() == True:
            belt_speed = self.tread_speed.GetValue()
        else:
            belt_speed = -1

        n_grid = n_grid + len(self.combination)
        locomotionProfiler(data_path=self.proj_path, tThr=self.tThresh.GetValue(),
                           speedSmFactor=self.SpeedSmFactor.GetValue(), grid_number=n_grid,
                           combination=self.combination,belt = belt_speed, saveFlag=True, plotFlag=False, log=True, plot_speed=save_speed,
                           plot_acc=save_acc)
    def Check_tread_speed(self,event):
        if self.tread_speed_check.IsChecked() == True:
            self.tread_speed.Enable(True)
        else:
            self.tread_speed.Enable(False)

    def Check_tread_length(self,event):
        if self.tread_length_check.IsChecked() == True:
            self.tread_length.Enable(True)
        else:
            self.tread_length.Enable(False)
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


    # def locomotion(self,event):
    #     plotFlag=False
    #     log=False
    #
    #     if self.save_plot.GetStringSelection() == 'Yes':
    #         plotFlag=True
    #     if self.save_log.GetStringSelection() == 'Yes':
    #         log=True
    #
    #     locomotionProfiler(data_path=self.proj_path,tThr=self.tThresh.GetValue(),speedSmFactor=self.SpeedSmFactor.GetValue(),saveFlag=True, plotFlag=plotFlag, log=log)
    #     dlg = wx.MessageDialog(self,message='Speed profiles created',style=wx.OK)
    #     dlg.ShowModal()
    #
    # def cadence(self,event):
    #     self.combination = self.check_list1.GetCheckedStrings() + self.check_list2.GetCheckedStrings()
    #     combinedPlot(data_path=self.proj_path,combination_list=self.combination,saveFlag=False,paperPlot=True)
    #     dlg = wx.MessageDialog(self, message='Cadence and circular plots created!', style=wx.OK)
    #     dlg.ShowModal()
    #
    # def acceleration(self,event):
    #     accel_plotter('/'.join(self.proj_path.split('/')[:-1]),self.tThresh.GetValue(),self.SpeedSmFactor.GetValue())
    #     dlg = wx.MessageDialog(self, message='Acceleration profiles created!', style=wx.OK)
    #     dlg.ShowModal()
