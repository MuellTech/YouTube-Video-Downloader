from pytube import YouTube
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
  try:
    video = YouTube(url)
    streams = video.streams.filter(progressive=True, file_extension ='mp4')
    highest_rev_vid = streams.get_highest_resolution(ouput_path = save_path)
    highest_rev_vid.download(output_path = save_path)
    print('video downloaded successfully')
  except Exception as e:
    print(e)

def open_file_dialog():
  folder = filedialog.askdirectory()
  if folder:
    print(f'Selected folder: {folder}')

  return folder

if __name__ == '__main__':
  root = tk.Tk()
  root.withdraw()

  video_url = input('Please enter the video url: ')
  save_dir = open_file_dialog()

  if save_dir:
    print('Video download in progress....')
    download_video(video_url, save_dir)
  else:
    print('Invalid save location')