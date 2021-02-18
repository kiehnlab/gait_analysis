import wx
import os
import datetime
from Welcome import Welcome
from Video_analyser import Video_analyser
from Speed_coord import S_C_profiler



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
        self.gui_size = (screenWidth * 0.6, screenHeight * 0.55)
        wx.Frame.__init__(
            self,
            None,
            wx.ID_ANY,
            "Kiehn_App",
            pos=wx.DefaultPosition,
            size=wx.Size(self.gui_size),
            style=wx.RESIZE_BORDER | wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )
        self.SetIcon(wx.Icon('mice.jpg'))
        self.SetSizeHints(
            wx.Size(self.gui_size)
        )
        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel)

        tab1 = Welcome(self.nb,self.gui_size)
        self.nb.AddPage(tab1,'Welcome')

        # tab2 = Video_analyser(self.nb,self.gui_size)
        # self.nb.AddPage(tab2,'Video Analyser')
        #
        # tab3 = S_C_profiler(self.nb,self.gui_size,'/home/janek/Downloads')
        # self.nb.AddPage(tab3,'Speed')

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer)


app = wx.App()
frame = MainFrame().Show()
app.MainLoop()

# def launch_KiehnApp():
#     app = wx.App()
#     frame = MainFrame().Show()
#     app.MainLoop()