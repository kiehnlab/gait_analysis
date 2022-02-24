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
from gait_analysis.Group_analysis import *

class loaded_S_C_profiler(wx.Panel):
    def __init__(self, parent, gui_size):
        # self.proj_path = proj_path
        self.parent = parent
        self.gui_size = gui_size
        self.pdf = []
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))

        # top_sizer = wx.BoxSizer(wx.VERTICAL)
        #
        # self.intro_txt = wx.StaticText(self,
        #                                label='Perform speed, acceleration and coordination analysis.')
        # top_sizer.Add(self.intro_txt, 0, wx.ALL, 5)

        sizer = wx.GridBagSizer(10,7)
        # sizer.Add(top_sizer,pos=(0,0))

        # line = wx.StaticLine(self)
        # sizer.Add(line, pos=(0, 0), span=(0, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt1 = wx.StaticText(self,label = 'Part1: Create speed profiles.')
        font = txt1.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt1.SetFont(font)
        sizer.Add(txt1,pos=(0,0),flag=wx.EXPAND)


        # self.save_np = wx.RadioBox(
        #     self,
        #     label='Want to save results as numpy table?',
        #     choices=['No','Yes'],
        #     majorDimension=1,
        #     style = wx.RA_SPECIFY_COLS,
        # )
        # sizer.Add(self.save_np,pos=(3,0),flag=wx.EXPAND)

        self.load_dir_txt = wx.StaticText(self,label='Select project folder:')
        sizer.Add(self.load_dir_txt,pos=(2,0),flag=wx.ALIGN_RIGHT)


        self.load_dir = wx.DirPickerCtrl(
            self,
            path='',
            style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST,
            message='Choose the working directory'
        )
        sizer.Add(self.load_dir, pos=(2, 1), span=wx.DefaultSpan, flag=wx.BOTTOM | wx.EXPAND, border=5)

        # self.proj_path = self.load_dir.GetPath()

        self.save_plot = wx.RadioBox(
            self,
            label='Want to save speed profile plot?',
            choices=['Yes','No'],
            majorDimension=1,
            style = wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_plot,pos=(3,1),span=wx.DefaultSpan,flag=wx.EXPAND)

        self.save_log = wx.RadioBox(
            self,
            label='Want to save results as csv(Excel) table?',
            choices=['Yes','No'],
            majorDimension=1,
            style = wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_log,pos=(3,2),flag=wx.EXPAND)

        sb = wx.StaticBox(self,label='Select noise filter parameter')
        self.boxsizer=wx.StaticBoxSizer(sb,wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.SpeedSmFactor = wx.SpinCtrlDouble(self, value='', min=1, max=20, initial=10, inc=1)
        hbox1.Add(self.SpeedSmFactor)

        self.boxsizer.Add(hbox1)
        sizer.Add(self.boxsizer,pos=(3,0))



        sb = wx.StaticBox(self,label='Specify treadmill length(cm): \n(If not, 20 cm assumed)')
        sb_sizer = wx.StaticBoxSizer(sb,wx.HORIZONTAL)
        border = wx.BoxSizer()

        self.tread_length = wx.SpinCtrlDouble(self, value='', min=0, max=30, initial=20, inc=0.01)
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
        self.tread_speed = wx.SpinCtrlDouble(self, value='', min=0, max=50, initial=20, inc=10)
        self.tread_speed.Enable(False)
        self.tread_speed_check.Bind(wx.EVT_CHECKBOX,self.Check_tread_speed)
        sb_sizer.Add(self.tread_speed_check)
        sb_sizer.Add(self.tread_speed)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(4,1))


        # self.run_speed = wx.Button(self,label='Run speed analysis!')
        # sizer.Add(self.run_speed,pos=(4,2),flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        # self.run_speed.Bind(wx.EVT_BUTTON,self.locomotion)


        line1 = wx.StaticLine(self)
        sizer.Add(line1, pos=(5, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt3 = wx.StaticText(self,label='Part2: Create acceleration plots with drag and recovery events')
        font = txt3.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt3.SetFont(font)
        sizer.Add(txt3,pos=(6,0))

        sb = wx.StaticBox(self,label='Specify duration for a drag/recovery event (s):')
        sb_sizer = wx.StaticBoxSizer(sb,wx.VERTICAL)
        border = wx.BoxSizer()

        self.tThresh = wx.SpinCtrlDouble(self, value='', min=0, max=1, initial=0.25, inc=0.05)
        sb_sizer.Add(self.tThresh,wx.EXPAND)
        border.Add(sb_sizer)
        sizer.Add(border, pos=(7,0))
        # tThresh_txt = wx.StaticText(self,label='Specify duration to count a drag/recovery event:')
        # sizer.Add(tThresh_txt,pos=(7,0),flag=wx.TOP)
        #
        #
        # self.tThresh = wx.SpinCtrlDouble(self,value='',min=0,max=1,initial=0.25,inc=0.05)
        # sizer.Add(self.tThresh,pos=(8,0),flag=wx.TOP)

        self.save_plot_acc = wx.RadioBox(
            self,
            label='Want to save acceleration profile plot?',
            choices=['Yes', 'No'],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS,
        )
        sizer.Add(self.save_plot_acc, pos=(7,1), span=wx.DefaultSpan, flag=wx.EXPAND)

        # self.accel = wx.Button(self,label='Run acceleration analysis')
        # sizer.Add(self.accel,pos=(7,2))
        # self.accel.Bind(wx.EVT_BUTTON,self.acceleration)

        line2 = wx.StaticLine(self)
        sizer.Add(line2, pos=(9, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        txt2 = wx.StaticText(self,label='Part3: Create cadence plots and circular plot.')
        font = txt2.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt2.SetFont(font)
        sizer.Add(txt2,pos=(10,0),flag=wx.TOP)

        self.check_list1 = wx.CheckListBox(self,choices=['Homolateral right("RH_RF")','Contra-lateral frontleft-hindright("LF_RH")','Hindlimb("LH_RH")'])
        self.check_list1.SetBackgroundColour(None)
        sizer.Add(self.check_list1,pos=(11,0),flag=wx.ALIGN_RIGHT)
        self.check_list2 = wx.CheckListBox(self, choices=['Homolateral left("LF_LH")','Contra-lateral frontright-hindleft("LH_RF")','Forelimb("LF_RF")'])
        sizer.Add(self.check_list2, pos=(11, 1),flag=wx.EXPAND)
        self.check_all = wx.CheckBox(self, label='Select all')
        self.check_all.Bind(wx.EVT_CHECKBOX,self.Select_all)
        sizer.Add(self.check_all, pos=(11, 2))

        # if len(self.check_list3.GetCheckedStrings()) == 0:
        # self.combination = self.check_list1.GetCheckedStrings() + self.check_list2.GetCheckedStrings()
        # else:
        #     self.combination = ['Homolateral right("RH_RF")','Contra-lateral frontleft-hindright("LF_RH")','Hindlimb("LH_RH")','Homolateral left("LF_LH")','Contra-lateral frontright-backleft("LH_RF")','Forelimb("LF_RF")']
        # self.select_opt_stride = wx.RadioBox(
        #     self,
        #     label='Select stride combination:',
        #     choices=['Homolateral right("RH_RF")','Contra-lateral frontleft-hindright("LF_RH")','Hindlimb("LH_RH")',
        #              'Homolateral left("LF_LH")','Contra-lateral frontright-backleft("LH_RF")','Forelimb("LF_RF")'],
        #     majorDimension=3,
        #     style=wx.RA_SPECIFY_COLS,
        # )
        # sizer.Add(self.select_opt_stride, pos=(11, 0), span=(0, 1))



        # sb1 = wx.StaticBox(self, label='Select stride combination')
        # sb_sizer1 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        # sb_sizer2 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        # border1 = wx.BoxSizer()
        # border2 = wx.BoxSizer()
        #
        # self.comb1 = wx.CheckBox(self, label='Homolateral right("RH_RF")')
        # self.comb2 = wx.CheckBox(self, label='Homolateral left("LF_LH")')
        # self.comb3 = wx.CheckBox(self, label='Contra-lateral frontleft-hindright("LF_RH")')
        # self.comb4 = wx.CheckBox(self, label='Contra-lateral frontright-backleft("LH_RF")')
        # self.comb5 = wx.CheckBox(self, label='Hindlimb("LH_RH")')
        # self.comb6 = wx.CheckBox(self, label='Forelimb("LF_RF")')
        #
        # sb_sizer1.Add(self.comb1)
        # sb_sizer1.Add(self.comb2)
        # sb_sizer2.Add(self.comb3)
        # sb_sizer2.Add(self.comb4)
        # border1.Add(sb_sizer1,pos=(0,1))
        # # border1.Add(sb_sizer2)
        # sizer.Add(border1, pos=(11, 0))


        # cadence_txt = wx.Button(self,label='Run coordination analysis')
        # sizer.Add(cadence_txt,pos=(11,3),flag=wx.ALIGN_RIGHT)
        # cadence_txt.Bind(wx.EVT_BUTTON,self.cadence)

        line3 = wx.StaticLine(self)
        sizer.Add(line3, pos=(12, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        self.create_pdf = wx.Button(self,label='Create final pdf')
        sizer.Add(self.create_pdf,pos=(13,3))
        self.create_pdf.Bind(wx.EVT_BUTTON,self.button_view)



        self.SetSizer(sizer)
        sizer.Fit(self)



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



    def button_view(self,event):
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

        N_bottom = len(glob.glob(self.load_dir.GetPath() + '/*.avi'))
        df = pd.DataFrame(columns=df_cols, index=range(N_bottom))
        df[df_cols[1:]] = df[df_cols[1:]].apply(pd.to_numeric)

        df = locomotionProfiler(data_path=self.load_dir.GetPath()+'/labels',
                tThr=self.tThresh.GetValue(),
                speedSmFactor=self.SpeedSmFactor.GetValue(),
                grid_number = n_grid,
                combination=self.combination,
                belt=belt_speed,
                df=df,
                saveFlag=True, 
                plotFlag=False, 
                log=True,
                plot_speed=save_speed,
                plot_acc = save_acc)
        dlg = wx.MessageDialog(self, message='Plots are created! Continue to group analysis!', style=wx.OK)
        dlg.ShowModal()
        page3 = Group_plotter(self.parent, self.gui_size)
        self.parent.AddPage(page3, 'Group analysis')
        self.parent.SetSelection(2)

    # def locomotion(self,event):
    #
    #     if self.load_dir.GetPath() == '':
    #         dlg = wx.MessageDialog(self,message='Select project folder!',style=wx.ICON_ERROR | wx.OK)
    #         dlg.ShowModal()
    #         return
    #
    #     plotFlag=False
    #     log=False
    #
    #
    #     if self.save_plot.GetStringSelection() == 'Yes':
    #         plotFlag=True
    #     if self.save_log.GetStringSelection() == 'Yes':
    #         log=True
    #     speed_plot = locomotionProfiler(data_path=self.load_dir.GetPath()+'/labels',tThr=self.tThresh.GetValue(),speedSmFactor=self.SpeedSmFactor.GetValue(),saveFlag=True, plotFlag=plotFlag, log=log)
    #     self.pdf.append(speed_plot)
    #     dlg = wx.MessageDialog(self, message='Speed profiles created', style=wx.OK)
    #     dlg.ShowModal()
    #
    # def cadence(self,event):
    #     if self.check_all.IsChecked() == True:
    #         self.combination = ['Homolateral right("RH_RF")', 'Contra-lateral frontleft-hindright("LF_RH")',
    #                             'Hindlimb("LH_RH")',
    #                             'Homolateral left("LF_LH")', 'Contra-lateral frontright-backleft("LH_RF")',
    #                             'Forelimb("LF_RF")']
    #     else:
    #         self.combination = self.check_list1.GetCheckedStrings() + self.check_list2.GetCheckedStrings()
    #     combinedPlot(data_path=self.load_dir.GetPath()+'/labels',combination_list=self.combination,saveFlag=False,paperPlot=True)
    #     dlg = wx.MessageDialog(self, message='Cadence and circular plots created!', style=wx.OK)
    #     dlg.ShowModal()
    #
    # def acceleration(self,event):
    #     accel_plotter(self.load_dir.GetPath(),self.tThresh.GetValue(),self.SpeedSmFactor.GetValue())
    #     dlg = wx.MessageDialog(self, message='Acceleration profiles created!', style=wx.OK)
    #     dlg.ShowModal()
