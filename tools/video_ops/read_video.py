import yt_dlp

def read_video(url:str)->str:
    __get_metadata__(url)
    #__download_video__(url)
    __download_audio__(url)

def __download_video__(url:str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'tools/video_ops/temp/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Video downloaded with yt-dlp!")

def __download_audio__(url:str):
    ######### COVERT TO MP3 (Requires ffmpeg installed.) #######################
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'tools/video_ops/temp/%(title)s.%(ext)s',
    }
    ##############################################################################
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def __get_metadata__(url:str):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        print(info_dict.keys())  # Show available metadata fields


read_video("https://www.youtube.com/watch?v=WS3ywmABNm4")