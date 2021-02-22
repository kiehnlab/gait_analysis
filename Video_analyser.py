import wx
import os
import datetime
import shutil
import warnings
import glob
warnings.filterwarnings("ignore")
import time
import argparse
import pdb
import pickle
os.environ['DLClight'] = 'True'
import threading
from Speed_coord import S_C_profiler

class analysis_Thread(threading.Thread):
    def __init__(self, threadID, name, filelist1, labeled_videos):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.config = './config.yaml'
        self.filelist1 = filelist1
        self.labeled_videos = labeled_videos
    def run(self):
        print ("Starting " + self.name)
        import deeplabcut
        deeplabcut.analyze_videos(self.config, self.filelist1, videotype='.avi')
        if self.labeled_videos == 'Yes':
            deeplabcut.create_labeled_video(self.config, self.filelist1, videotype='.avi')
            #     self.dest_labeled_videos = self.dest + '/labeled_videos'
            #     os.mkdir(self.dest_labeled_videos)
            #     labels = glob.glob(self.file_path + '*labeled.mp4')
            #     [shutil.move(f, self.dest_labeled_videos) for f in labels]
        print ("Exiting " + self.name)

class Video_analyser(wx.Panel):
    def __init__(self,parent,gui_size):
        self.parent = parent
        self.gui_size = gui_size
        h = self.gui_size[0]
        w = self.gui_size[1]
        self.filelist = []
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER,size=(w,h))

        top_sizer = wx.BoxSizer(wx.VERTICAL)


        self.intro_txt = wx.StaticText(self,label =' Step1 : Upload your video/videos and obtain h5 file with predicted coordinates.\n OPTIONAL : Obtain labeled videos')
        top_sizer.Add(self.intro_txt,0,wx.ALL,5)
        #sizer.Add(self.intro_txt, pos=(0,0),flag=wx.TOP | wx.LEFT |wx.EXPAND)

        sizer = wx.GridBagSizer(10, 15)

        sizer.Add(top_sizer,pos=(0,1))

        line = wx.StaticLine(self)
        sizer.Add(line,pos=(1,0),span=(1,w), flag=wx.EXPAND | wx.BOTTOM, border =5)

        self.save_dir_txt = wx.StaticText(self,label='Select where to create the project:')
        sizer.Add(self.save_dir_txt,pos=(2,0),flag =wx.BOTTOM | wx.EXPAND, border = 5)

        self.save_dir = wx.DirPickerCtrl(
            self,
            path='',
            style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST,
            message='Choose the working directory'
        )
        sizer.Add(self.save_dir, pos=(2, 1), span=wx.DefaultSpan, flag=wx.BOTTOM | wx.EXPAND, border=5)


        self.author_name_txt = wx.StaticText(self,label='Author name:')
        sizer.Add(self.author_name_txt,pos=(3,0),flag=wx.TOP | wx.EXPAND)

        self.author_name = wx.TextCtrl(self)
        sizer.Add(self.author_name,pos=(3,1),span=(1,5),flag=wx.BOTTOM | wx.EXPAND)

        self.project_name_txt = wx.StaticText(self,label='Project name:')
        sizer.Add(self.project_name_txt,pos=(4,0),flag=wx.TOP | wx.EXPAND)

        self.project_name = wx.TextCtrl(self)
        sizer.Add(self.project_name,pos=(4,1),span=(1,5),flag=wx.EXPAND)





        self.create_project = wx.Button(self,label='Create project!')
        #self.create_project.Enable(False)
        sizer.Add(self.create_project,pos=(5,5),flag=wx.BOTTOM, border =5)
        self.create_project.Bind(wx.EVT_BUTTON,self.create_new_project)


        self.videos = wx.StaticText(self,label='Please select videos:')
        sizer.Add(self.videos, pos=(7,0), flag = wx.TOP | wx.EXPAND, border = 5)

        self.sel_vids = wx.Button(self,label='Load Videos')
        sizer.Add(self.sel_vids, pos=(7,1),span=(1,5), flag =wx.TOP | wx.EXPAND, border=5)
        self.sel_vids.Bind(wx.EVT_BUTTON, self.select_videos)



        #self.save_dir.Bind(wx.EVT_BUTTON,self.select_save_dir)



        # self.check = wx.Button(self,label='Check path')
        # sizer.Add(self.check,pos=(10,0))
        # self.check.Bind(wx.EVT_BUTTON,self.check_dir_path)
        #self.check.Bind(wx.EVT_BUTTON, self.check_video_path)

        self.save_lab_videos = wx.RadioBox(self,
                                           label='Save labeled videos?',
                                           choices=['Yes','No'],
                                           majorDimension=1,
                                           style=wx.RA_SPECIFY_ROWS)

        # sb = wx.StaticBox(self, label="Optional Attributes")
        # self.boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        #
        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #
        # self.save_lab_videos = wx.CheckBox(self,label='Create labeled videos?')
        # hbox2.Add(self.save_lab_videos)
        # self.boxsizer.Add(hbox2)
        sizer.Add(self.save_lab_videos,pos=(10,1),flag=wx.EXPAND | wx.TOP | wx.LEFT, border=10)

        self.run = wx.Button(self,label='RUN')
        self.run.Enable(True)
        sizer.Add(self.run,pos=(11,5),flag= wx.TOP | wx.RIGHT)
        self.run.Bind(wx.EVT_BUTTON,self.run_script)

        self.reset = wx.Button(self,label='RESET VIDEOS')
        sizer.Add(self.reset,pos=(11,3),flag= wx.TOP)
        self.reset.Bind(wx.EVT_BUTTON,self.reset_video)

        self.SetSizer(sizer)
        sizer.Fit(self)


    def reset_video(self,event):
        self.filelist =[]
        self.sel_vids.SetLabel('Load Videos')

    def check_video_path(self,event):
        dlg = wx.MessageDialog(self,message='%s\n%s\n%s' %(self.filelist[0],self.filelist[1],self.filelist[2]),caption='Check of path', style=wx.OK)
        dlg.ShowModal()

    def check_dir_path(self,event):
        dlg = wx.MessageDialog(self,message=self.save_dir.GetPath(),caption='Check of path', style=wx.OK)
        dlg.ShowModal()

    def create_new_project(self,event):
        if self.save_dir.GetPath() == '' or self.project_name.GetValue() == '' or self.author_name.GetValue() == '':
            dlg = wx.MessageDialog(self,message='Make sure to choose directory and insert yours and projects names!!',style=wx.ICON_ERROR | wx.OK)
            dlg.ShowModal()
            return

        self.dest = self.save_dir.GetPath()+'/'+self.author_name.GetValue()+'-'+self.project_name.GetValue()+'-'+datetime.datetime.now().strftime('%Y-%m-%d')

        if os.path.exists(self.dest):
            dlg = wx.MessageDialog(self,message='Project already exists! Do you want overwrite it?',style=wx.ICON_QUESTION | wx.YES_NO)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                shutil.rmtree(self.dest)
            else:
                return
        os.mkdir(self.dest)
        dlg = wx.MessageDialog(self,message='Project created',style=wx.OK)
        dlg.ShowModal()
        self.run.Enable(True)

    def select_videos(self, event):

        cwd = os.getcwd()
        dlg = wx.FileDialog(
            self, "Select videos to add to the project", cwd, "", "*.*", wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            vids = dlg.GetPaths()
            self.new_vids = []
            for i in vids:
                if i in self.filelist:
                    continue
                else:
                    self.new_vids.append(i)
            self.filelist = self.filelist + self.new_vids
            self.sel_vids.SetLabel("Total %s Videos selected" % len(self.filelist))

    def run_script(self,event):
        if len(self.filelist) == 0:
            dlg = wx.MessageDialog(self,message='Upload videos!',style=wx.ICON_ERROR | wx.OK)
            dlg.ShowModal()
            return

        t1 = analysis_Thread(1, "Video analysis",self.filelist,self.save_lab_videos.GetStringSelection())
        t1.start()
        dlg = wx.ProgressDialog('', 'Please wait..',
                                style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_CAN_ABORT | wx.STAY_ON_TOP)
        while t1.isAlive():
            wx.MilliSleep(300)
            dlg.Pulse("Analysing videos:")
            wx.GetApp().Yield()
        del dlg
        t1.join()
        # dlg = wx.MessageDialog(self, message='The video analysis will start now!', style=wx.OK | wx.CANCEL)
        # if dlg.ShowModal() == wx.ID_CANCEL:
        #     return
        # if dlg.ShowModal() == wx.ID_OK:
        #     dlg.Destroy
        # dlg = wx.ProgressDialog('Lets see','Information',parent=self)
        # import deeplabcut
        # deeplabcut.analyze_videos(config,self.filelist, videotype='.avi')
        # dlg.Destroy()

        self.file_path = '/'.join(self.filelist[0].split('/')[:-1]) + '/'
        if self.save_lab_videos.GetStringSelection() == 'Yes':
        #     deeplabcut.create_labeled_video(config,self.filelist,videotype='.avi')
            self.dest_labeled_videos = self.dest + '/labeled_videos'
            os.mkdir(self.dest_labeled_videos)
            labels = glob.glob(self.file_path + '*labeled.mp4')
            [shutil.move(f, self.dest_labeled_videos) for f in labels]
        self.dest_labels = self.dest+'/labels'
        os.mkdir(self.dest_labels)
        labels = glob.glob(self.file_path + '*.h5')
        [shutil.move(f, self.dest_labels) for f in labels]
        labels = glob.glob(self.file_path + '*.pickle')
        [shutil.move(f, self.dest_labels) for f in labels]
        #
        [shutil.copy(f, self.dest) for f in self.filelist]
        #
        page3 = S_C_profiler(self.parent,self.gui_size,self.dest_labels)
        self.parent.AddPage(page3,'Speed and Coordination')
        self.parent.SetSelection(2)

    def get_vid_dir(self,vid_path):
        a = vid_path.split('/')
        b = '/'.join(a[-1])
        b = b+'/'
        return b









































