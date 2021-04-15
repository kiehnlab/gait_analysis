# Welcome to KiehnLab Locomotion Analysis tool.
This tool is designed to analyse bottom and lateral videos. Analysis for bottom videos include speed, acceleration and cadence profiles. For lateral videos, we provide stick plots and angles analysis between different joints. The pose estimation is performed by DeepLabCut.

# MANUAL #

## Let's start with turning on the tool:

1. Start by loading the appropriate conda environment. You do this by typing in 'conda activate DLC-CPU'
2. Go into the directory in which "gait_analysis" tool is located.
3. Start up the tool by typing 'python -m gait_analysis'

<p align="center">
<img src = 'media/start_up.png' title='start'>
</p>

You will land on the main page of our tool. From here you can decide if you wish to start a new project, load an existing one or just perform a group analysis. 

<p align="center">
<img src = 'media/project_type.png' title='project'>
</p>

**IMPORTANT!!!**

In order to load a project, it must be structured (files names) in a way that our tool does it. This is imperative for the tool to work properly. The structure of a project directory looks like that: 

<p align="center">
<img src = 'media/project_structure.png' title='project_structure'>
</p>

Additionally, you can select which type of video you wish to analyse. The tool provides an option to either:
* only analyse bottom videos
* only analyse lateral videos
* analyse noth types of videos at the same time

<p align="center">
<img src = 'media/video_type.png' title='video'>
</p>


**IMPORTANT!!!**

The tool makes a distinction between bottom and lateral videos based on the names of the file. Therefore it is crucial to keep a partical nomenclature. The difference for the corresponding bottom and lateral videos lies in the 'SIDEVIEW' prefix in the name of file.
Example:
* Bottom video filename:           Cage1_0L0R_20cms_0degUP_4.avi
* Lateral video filename: SIDEVIEW_Cage1_0L0R_20cms_0degUP_4.avi


## STARTING A NEW PROJECT

The following demo shows the case where one selects to analyse combined videos. The same applies to all other options however this is the most general version.

If you decide to start a new project, the first thing to do is to specify where we want to create it. Simply press the 'Browse' button and select a directory in which new project should be created. Next you need to set the 'Project name' and 'Author name'. The full name of the project folder will comprise of the project name, author name and current date. 
Example:

<p align="center">
<img src = 'media/make_project.png' title='project_names'>
</p>

Such parameters will create a project named 'Kiehn_Lab-test-2021-04-14'. In case where you already a project withthat name, the program will ask you if you whish to overwrite already existing project. BE CAREFUL WITH THIS!

In the next step you need to upload the video which are to be analysed. It is important to upload correct videos under specific name, therefore under 'bottom videos' upload bottom videos and the same for lateral. If by any chance you upload wrong videos do not worry! Simply press a 'RESET VIDEOS' button which will reset all uploaded videos and you can repeat the process.

Finally, you have an optional choice do save labeled videos with overlayed markers on the analysed videos. This option serves only visualisation purpose, where you can make sure, that the model predicted correctly. 

<p align="center">
<img src = 'media/save_labeled.png' title=labeled_videos>
</p>

In order to start the analysis press the 'RUN' button. A window will pop up telling how long the analysis is taking. When it disapears, this means that the analysis is finished. Corresponding labels will be save in a directory called 'Labels'. 

**IMPORTANT!!!**

In case of loading an existing project, this step is ommited!!!


## SPEED, ACCELERATION AND CADENCE PROFILES

For the analysis of the bottom videos we provide 3 types of profiling:
*Speed profile - showing the belt speed, avg.speed and avg. instantenous speed with its error over the whole video
*Acceleration profile - showing instantenous acceleration and if existing, drag and recovery events over the whole video
*Cadence profile -  showing cadence and circular plots for selected limb coordination 

We provide multiple optional choices, that are up to the user. Firstly, one has an option to decide, which plots should be included in the final pdf. This choices are represented by the following windows:

<p align="center">
<img src = 'media/pdf_options.png' title='pdf_options'>
</p>


If you wish to include speed and acceleration profiles in your final pdf you simply must choose option 'Yes' in the corresponding box. This procedure is a bit different for the cadence profiles. You need to select which limb coordination you wish to include. In case of all of them being needed, simply mark 'Select all'. 

Additionally, you have an option to save all the important parameters from the analysis as a csv/Excel table. 

**TREADMILL PARAMETERS**

Regarding belt parameters, you have an option to specify these too. By defualt, we assume that the length of the treadmill is 20 cm however, if that is not the case, you can specify the length. Similar goes for the treadmill speed. By default, the tool assumes the speed from the name of the video file however, if the actuall speed was different, you can specify that too. If you wish to personalise both feature, simply check the corresponding checkbox and set the values in the following windows:

<p align="center">
<img src = 'media/treadmill_param.png' title='treadmill'>
</p>

**SPEED PROFILE PARAMETERS**

For the speed profile plot, you can specify the 'noise filter'. This parameter smoothes out the plot and removes big variations, allowing for a good looking plot. By default it is set to 10, which is the value that we propose.

**ACCELERATION PROFILES**

In this part of the analysis you have a choice on the selection of drag and recovery events. You need to choose a maximum time duration  (in seconds) for the program to select steps during which recover/drag event occured. This steps will later on be eliminated from the analysis. The will also be plot on the acceleration profile plot with blue line for  recovery event and red line for drag event. 


## STICK PLOTS AND ANGLES ANALYSIS


















