import wx
import os
import datetime
#from Welcome import Welcome
#from Video_analyser import Video_analyser
#from Speed_coord import S_C_profiler
#from Load_project import loaded_S_C_profiler
import gait_analysis
from gait_analysis.Welcome import Welcome
from gait_analysis.Video_analyser import Video_analyser
from gait_analysis.Speed_coord import S_C_profiler
from gait_analysis.Load_project import loaded_S_C_profiler
from gait_analysis.Group_analysis import Group_plotter



class MainFrame(wx.Frame):
    def __init__(self):
        displays = (
            wx.Display(i) for i in range(wx.Display.GetCount())
        )  # Gets the number of displays
        screenSizes = [
            display.GetGeometry().GetSize() for display in displays
        ]  # Gets the size of each display
        index = 0  # For display 1.
        screenWidth = screenSizes[index][0]
        screenHeight = screenSizes[index][1]
        self.gui_size = (screenWidth * 0.8, screenHeight * 0.75)
        wx.Frame.__init__(
            self,
            None,
            wx.ID_ANY,
            "Gait Analysis App",
            pos=wx.DefaultPosition,
            size=wx.Size(self.gui_size),
            style=wx.RESIZE_BORDER | wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )
        self.SetIcon(wx.Icon(gait_analysis.__path__[0] + '/mice.jpg'))
        self.SetSizeHints(
            wx.Size(self.gui_size)
        )
        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel)

        tab1 = Welcome(self.nb,self.gui_size)
        self.nb.AddPage(tab1,'Welcome')

        # tab2 = Group_plotter(self.nb,self.gui_size)
        # self.nb.AddPage(tab2,'Trutu')

        # tab2 = Video_analyser(self.nb,self.gui_size)
        # self.nb.AddPage(tab2,'Video Analyser')

        # tab3 = S_C_profiler(self.nb,self.gui_size,'/home/janek/Downloads')
        # self.nb.AddPage(tab3,'Speed')
        #
        # tab4 = loaded_S_C_profiler(self.nb,self.gui_size)
        # self.nb.AddPage(tab4,'load')

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer)


# app = wx.App()
# frame = MainFrame().Show()
# app.MainLoop()

def launch_app():
    app = wx.App()
    frame = MainFrame().Show()
    app.MainLoop()
