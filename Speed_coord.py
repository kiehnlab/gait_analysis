import wx


class S_C_profiler(wx.Panel):
    def __init__(self, parent, gui_size):
        h = gui_size[0]
        w = gui_size[1]
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER, size=(w, h))
        sizer = wx.GridBagSizer(10,7)



        self.SetSizer(sizer)
        sizer.Fit(self)