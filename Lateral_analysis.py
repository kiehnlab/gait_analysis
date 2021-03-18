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



class lateral_panel(wx.Panel):
    def __init__(self, parent, gui_size,proj_path):
        self.proj_path = proj_path
        self.parent = parent
        self.gui_size = gui_size
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))

        sizer = wx.GridBagSizer(10, 7)

        txt1 = wx.StaticText(self, label='Part1: Create stick plots and angles analysis.')
        font = txt1.GetFont()
        font.PointSize += 0.5
        font = font.Bold()
        txt1.SetFont(font)
        sizer.Add(txt1, pos=(0, 0), flag=wx.EXPAND)

        line = wx.StaticLine(self)
        sizer.Add(line, pos=(1, 0), span=(1, w), flag=wx.EXPAND | wx.BOTTOM, border=5)

        sb = wx.StaticBox(self, label='Select scaling for stick plots')
        self.boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.scaling_sticks = wx.SpinCtrlDouble(self, value='', min=1, max=10, initial=2, inc=1)
        hbox1.Add(self.scaling_sticks)

        self.boxsizer.Add(hbox1)
        sizer.Add(self.boxsizer, pos=(2, 0), flag=wx.EXPAND)

        self.run = wx.Button(self,label='RUN')
        sizer.Add(self.run,pos=(3,3))
        self.run.Bind(wx.EVT_BUTTON,self.lateral_pdf)


        self.SetSizer(sizer)
        sizer.Fit(self)

    def lateral_pdf(self,event):
        N = len(glob.glob(self.proj_path + '/*.avi'))
        df = pd.DataFrame(columns=df_cols, index=range(N))
        df[df_cols[1:]] = df[df_cols[1:]].apply(pd.to_numeric)
        df = lateral_profiler(self.proj_path, self.scaling_sticks.GetValue(), df)  # Measure joint angles, make stick figures
        print(df)
        df.to_csv(self.proj_path + '/statistics.csv', index=False, float_format='%.4f', na_rep='0')
