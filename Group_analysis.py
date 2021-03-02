import wx
from Video_analyser import *
from coordination.constants import *
from coordination.profiler import *
from coordination.plotter import *
from Accel_plotter import *
from coordination.plotter import *
from coordination.coord import iqrMean, heurCircular
import warnings
warnings.filterwarnings("ignore")
from coordination.tools import videoMetadata
from coordination.constants import *
from coordination.accel import *

class Group_plotter(wx.Panel):
    def __init__(self, parent, gui_size):
        self.parent = parent
        self.gui_size = gui_size
        h = self.gui_size[0]
        w = self.gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))
        sizer = wx.GridBagSizer(10, 7)



        self.SetSizer(sizer)
        sizer.Fit(self)