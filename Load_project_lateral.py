import wx
#from Video_analyser import *
#from coordination.constants import *
#from coordination.profiler import *
#from coordination.plotter import *
#from Accel_plotter import *
#from coordination.lateral import *
#from coordination.sticks import *

from gait_analysis.Video_analyser import *
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.profiler import *
from gait_analysis.coordination.plotter import *
from gait_analysis.Accel_plotter import *
from gait_analysis.coordination.lateral import *
from gait_analysis.coordination.sticks import *
import pdb

class loaded_lateral_profiler(wx.Panel):
    def __init__(self, parent, gui_size):
        # self.proj_path = proj_path
        self.parent = parent
        self.gui_size = gui_size
        self.pdf = []
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))

        sizer = wx.GridBagSizer(10, 7)

        txt1 = wx.StaticText(self,label = 'Part1: Create stick plots and angles analysis.')
        font = txt1.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt1.SetFont(font)
        sizer.Add(txt1,pos=(0,0),flag=wx.EXPAND)

        line = wx.StaticLine(self)
        sizer.Add(line,pos=(1,0),span=(1,w), flag=wx.EXPAND | wx.BOTTOM, border =5)

        self.load_dir_txt = wx.StaticText(self, label='Select project folder:')
        sizer.Add(self.load_dir_txt, pos=(4,5), flag=wx.ALIGN_RIGHT)

        self.load_dir = wx.DirPickerCtrl(
            self,
            path='',
            style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST,
            message='Choose the working directory'
        )
        sizer.Add(self.load_dir, pos=(4,6), flag=wx.BOTTOM | wx.EXPAND, border=5)

        sb = wx.StaticBox(self, label='Options:')
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        scal_sb = wx.StaticBox(self,label='Select scaling for stick plots')
        scal_sb_sizer = wx.StaticBoxSizer(scal_sb,wx.HORIZONTAL)
        self.scaling_sticks = wx.SpinCtrlDouble(self, value='', min=1, max=10, initial=2, inc=1)
        scal_sb_sizer.Add(self.scaling_sticks,0,flag=wx.ALIGN_LEFT,border=5)
        # hbox1.Add(self.scaling_sticks)

        temp_sb = wx.StaticBox(self,label='Perform temporal synchronization?')
        temp_sb_sizer = wx.StaticBoxSizer(temp_sb,wx.VERTICAL)
        self.temp_synch = wx.RadioBox(self,choices=['Yes','No'])
        temp_sb_sizer.Add(self.temp_synch,0,flag=wx.ALIGN_CENTER,border=5)
        # sizer.Add(self.temp_synch,pos=(4,1),flag=wx.EXPAND)
        # self.boxsizer.Add(hbox1)

        hbox1.Add(scal_sb_sizer,0,flag=wx.EXPAND,border=5)
        hbox1.Add(temp_sb_sizer,10,flag=wx.EXPAND,border=5)
        boxsizer.Add(hbox1)
        sizer.Add(boxsizer, pos=(5, 6), flag=wx.EXPAND)




        self.run = wx.Button(self,label='Create pdf!')
        sizer.Add(self.run,pos=(6,7))
        self.run.Bind(wx.EVT_BUTTON,self.lateral_pdf)



        self.SetSizer(sizer)
        sizer.Fit(self)


    def lateral_pdf(self,event):
        N = len(glob.glob(self.load_dir.GetPath() + '/*.avi'))
        df = pd.DataFrame(columns=df_cols, index=range(N))
        df[df_cols[1:]] = df[df_cols[1:]].apply(pd.to_numeric)
        #pdb.set_trace()
        df = lateral_profiler(self.load_dir.GetPath(), 2, df)  # Measure joint angles, make stick figures
        df.to_csv(self.load_dir.GetPath() + '/statistics.csv', index=False, float_format='%.4f', na_rep='0')
        dlg = wx.MessageDialog(self,message='Plots created!',style=wx.OK)
        dlg.ShowModal()
