import tkinter as tk 
from tkinter import *
from pytube import YouTube 
from tkinter import messagebox, filedialog
import glob
import os
import pathlib
import moviepy.editor as mp 
  
  
# Defining CreateWidgets() function 
# to create necessary tkinter widgets
def Browse(): 
    # Presenting user with a pop-up for 
    # directory selection. initialdir  
    # argument is optional Retrieving the 
    # user-input destination directory and 
    # storing it in downloadDirectory 
    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH") 
   
    # Displaying the directory in the directory 
    # textbox 
    download_Path.set(download_Directory) 
  
# Defining Download() to download the video 
def Download(): 
    global root
    global video_Link
    global download_Path
    global starttime
    global endtime
    global var
    global selected_resolution
    global resolution_type
    print(str(starttime.get()),str(endtime.get()),video_Link.get(),download_Path.get())
    starttime= sum(int(x) * 60 ** i for i, x in enumerate(reversed((str(starttime.get())).split(':'))))
    endtime= sum(int(x) * 60 ** i for i, x in enumerate(reversed((str(endtime.get())).split(':'))))
    print(starttime,endtime,str(var.get()),var.get())
    if(str(var.get())=="EDIT"):
        print("edit")
        mp4files = (YouTube(video_Link.get()).streams.filter(adaptive=True).order_by('resolution').desc())
        print(mp4files)
        mp4files[0].download()
        downloaded_video=glob.glob("*.mp4")
        downloaded_video.sort(key=os.path.getmtime,reverse=True)
        input_video_path = downloaded_video[0]
        with mp.VideoFileClip(input_video_path) as video:
            new = video.subclip(starttime,endtime)
            new.write_videofile(download_Path.get()+"/clip.mp4", audio_codec='aac')
            messagebox.showinfo("SUCCESSFULLY","DOWNLOADED AND SAVED IN\n"+download_Path.get()+"/clip.mp4")
        try:
            file_to_rem = pathlib.Path(download_video[0])
            file_to_rem.unlink()
        except Exception as e:
            pass
    elif(str(var.get())=="STATUS"):
        print("status")
        selected_resolution_index=resolution_type.index(selected_resolution.get())
        print(selected_resolution_index)
        selected_video=(YouTube(video_Link.get())).streams.filter(adaptive=True,res=str(resolution_type[selected_resolution_index]))
        selected_video[0].download()
        YouTube(video_Link.get()).streams.filter(only_audio=True).first().download(filename="audio")
        print(3)
        download_video=glob.glob("*")
        print(4)
        download_video.sort(key=os.path.getmtime,reverse=True)
        print(5)
        print(download_video)
        with mp.AudioFileClip(download_video[0]) as az:
            print(6)
            new=az.subclip(starttime,endtime)
            new.write_audiofile('my.mp3')
            print("audio")
        with mp.VideoFileClip(download_video[1]) as vid:
            q = vid.subclip(starttime, endtime)
            q.write_videofile('y.mp4',fps=60)
            print("video")
        download_video1=glob.glob("*")
        download_video1.sort(key=os.path.getmtime,reverse=True)
        print(download_video1)
        audi=mp.AudioFileClip(download_video1[1])
        vidi=mp.VideoFileClip(download_video1[0])
        finalclip=vidi.set_audio(audi)
        finalclip.write_videofile(str(download_Path.get())+'\clipping.mp4')
        messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" 
                        + download_Path.get()+'\clipping.mp4')
        try:
            file_to_rem = pathlib.Path(download_video[0])
            file_to_rem.unlink()
            file_to_rem = pathlib.Path(download_video[1])
            file_to_rem.unlink()
            file_to_rem = pathlib.Path(download_video1[1])
            file_to_rem.unlink()
            file_to_rem = pathlib.Path(download_video1[0])
            file_to_rem.unlink()
        except Exception as e:
            pass        
    elif(str(var.get())=="AUDIO"):
        print("audio")
        mp3files = (YouTube(video_Link.get())).streams.filter(only_audio=True).all()
        mp3files[0].download() 
        download_audio=glob.glob("*")
        download_audio.sort(key=os.path.getmtime,reverse=True)
        output_audio_path="clip.mp3"
        with mp.AudioFileClip(download_audio[0]) as video:
            new = video.subclip(starttime, endtime)
            new.write_audiofile(download_Path.get()+"/"+output_audio_path)
            messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + str(download_path.get())+"/"+output_audio_path)
        try:
            file_to_rem = pathlib.Path(download_audio[0])
            file_to_rem.unlink()
            
        except Exception as e:
            pass          
def sel():
    global selected_resolution
    global video_Link
    selection = "You selected the option " + str(var.get())
    if(str(var.get())=="EDIT"):
        label.config(text=selection)
        Download_B = Button(root, text="Download",  command=Download,  width=20, bg="#05E8E0") 
        Download_B.grid(row=7, column=1, pady=3, padx=3)
    elif(str(var.get())=="AUDIO"):
        label.config(text=selection)
        Download_B = Button(root, text="Download",  command=Download,  width=20, bg="#05E8E0") 
        Download_B.grid(row=7, column=1, pady=3, padx=3)
    elif(str(var.get())=="STATUS"):
        mp4files = (YouTube(video_Link.get()).streams.filter(adaptive=True))
        for i in mp4files:
            if(i.resolution not in resolution_type):
                resolution_type.append(i.resolution)
        resolution_type.remove(None)
        for i in range(0,len(resolution_type)):
            button=Radiobutton(root, text =resolution_type[i], variable = selected_resolution,value =resolution_type[i],command=sel,tristatevalue=0)
            button.grid(row=5+i,column=2,pady=0,padx=0)
        selection+=" and you selected the resolution"+" "+str(selected_resolution.get())
        label.config(text=selection) 
        Download_B = Button(root, text="Download",  command=Download,  width=20, bg="#05E8E0") 
        Download_B.grid(row=7+len(resolution_type), column=1, pady=3, padx=3)        
    
root = tk.Tk()
root.geometry("1000x1200") 
root.resizable(False, False) 
root.title("YouTube_Video_Downloader") 
video_Link = StringVar() 
download_Path = StringVar()
starttime=StringVar()
endtime=StringVar()
var=StringVar()
selected_resolution=StringVar()
resolution_type=[]
link_label = Label(root,  text="YouTube link  :", bg="#E8D579") 
link_label.grid(row=0, column=0, pady=5,padx=5)   
root.linkText = Entry(root, width=85, textvariable=video_Link) 
root.linkText.grid(row=0,  column=1, pady=5, padx=5, columnspan = 2)    
destination_label = Label(root,  text="Destination    :", bg="#E8D579") 
destination_label.grid(row=1, column=0, pady=5, padx=5) 
root.destinationText = Entry(root, width=50, textvariable=download_Path) 
root.destinationText.grid(row=1,  column=1, pady=5, padx=5) 
browse_B = Button(root,  text="Browse", command=Browse, width=10, bg="#05E8E0") 
browse_B.grid(row=1, column=2, pady=1, padx=1)
start_label=Label(root,text="start time    :",bg="#E8D579")
start_label.grid(row=2,column=0,pady=10,padx=5)
root.startText=Entry(root,width=50,textvariable=starttime)
root.startText.grid(row=2,column=1,pady=10,padx=5)
start_inst=Label(root,text="(starting time must be HH:MM:SS format)")
start_inst.grid(row=2,column=2,pady=10,padx=5)
end_label=Label(root,text="end time    :",bg="#E8D579")
end_label.grid(row=3,column=0,pady=10,padx=5)
root.endText=Entry(root,width=50,textvariable=endtime)
root.endText.grid(row=3,column=1,pady=10,padx=5)
end_inst=Label(root,text="(ending time must be HH:MM:SS format)")
end_inst.grid(row=3,column=2,pady=10,padx=5)
format_label=Label(root,text="Format    :",bg="#E8D579")
format_label.grid(row=4,column=0,pady=10,padx=5)
l=["EDIT","STATUS","AUDIO"]
for i in range(0,len(l)):
    button=Radiobutton(root, text =l[i], variable = var, 
                value =l[i],command=sel,tristatevalue=0)
    button.grid(row=4,column=i+1,pady=5,padx=5)
label = Label(root)
label.grid(row=6+len(resolution_type),column=1,pady=3,padx=3)
root.mainloop()
