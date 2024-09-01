from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import os

def download_video(url, save_path, file_name=None, progress_bar=None):
    try:
        video = YouTube(url)

        # Get the highest resolution stream
        streams = video.streams.filter(progressive=True, file_extension='mp4')
        highest_res_vid = streams.get_highest_resolution()

        def on_progress(stream, chunk, bytes_remaining):
            if progress_bar:
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                percentage = bytes_downloaded / total_size * 100
                progress_bar['value'] = percentage
                root.update_idletasks()

        video.register_on_progress_callback(on_progress)

        # If a file name is provided, save the file with that name
        if file_name:
            save_path = os.path.join(save_path, f"{file_name}.mp4")
            highest_res_vid.download(filename=save_path)
        else:
            highest_res_vid.download(output_path=save_path)

        print('Video downloaded successfully.')
        messagebox.showinfo("Success", f"Video downloaded successfully to {save_path}")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Download Failed", f"Failed to download video: {e}")

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f'Selected folder: {folder}')
    return folder

def validate_url(url):
    try:
        YouTube(url)
        return True
    except Exception as e:
        print(f"Invalid URL: {e}")
        messagebox.showerror("Invalid URL", "The provided URL is not valid. Please enter a valid YouTube video URL.")
        return False

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Loop to allow downloading multiple videos
    while True:
        video_url = simpledialog.askstring("YouTube URL", "Please enter the YouTube video URL:")
        
        # Validate the URL
        if video_url and validate_url(video_url):
            save_dir = open_file_dialog()

            if save_dir:
                file_name = simpledialog.askstring("File Name", "Enter a name for the downloaded video (optional):")

                # Create a new top-level window for the progress bar
                progress_window = tk.Toplevel(root)
                progress_window.title("Downloading...")
                tk.Label(progress_window, text="Download in progress...").pack(pady=10)

                # Create the progress bar
                progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
                progress_bar.pack(pady=10)

                # Start downloading the video
                print('Video download in progress...')
                download_video(video_url, save_dir, file_name, progress_bar)

                # Close the progress window once the download is complete
                progress_window.destroy()
            else:
                print('Invalid save location.')
                messagebox.showerror("Invalid Directory", "No valid directory selected.")
        
        # Ask the user if they want to download another video
        another = messagebox.askyesno("Download Another?", "Would you like to download another video?")
        if not another:
            break

    print("Exiting program.")
    messagebox.showinfo("Goodbye", "Thank you for using the YouTube Downloader!")
