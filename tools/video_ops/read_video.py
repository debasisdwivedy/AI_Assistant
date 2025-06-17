import yt_dlp

def read_video(url:str)->str:
    """
    Tool: Audio/Video reader to read audio/video files

        Name : read_video

        Description:
            This tool is used to read audio/video files like (mp3,mp4,MOV etc) of different format.
            The result return is of type string

        Args:
            url:str = The url of the video file.

        Usage:
            Call this tool if you want to get the content of a audio/video file from a URL.

        Output:

            result:str = The result from the function call
    """
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


# read_video("https://www.youtube.com/watch?v=WS3ywmABNm4")