import yt_dlp,uuid,os

import sys
sys.path.append(os.getcwd())

from utils.audio_transcribe import get_transcript

def read_multimedia(url:str,audio_only:bool=True)->str:
    """
    Tool: Audio/Video reader to read audio/video files

        Name : read_multimedia

        Description:
            This tool is used to read audio/video files like (mp3,mp4,MOV etc) of different format.
            The result return is of type string

        Args:
            url:str = The url/filename of the video file.
            audio_only:bool = Set as True if only Audio file is required for the task, else Set as False

        Usage:
            Call this tool if you want to get the content of a audio/video file from a URL.

        Output:

            result:str = The transcriptions of the media file.
    """

    if url.startswith("http"):
        filename = str(uuid.uuid4())
        #__get_metadata__(url)
        if audio_only:
            __download_audio__(url,filename)
        else:
            __download_video__(url,filename)
    else:
        filename = url

    # Get the text
    transcript_text = get_transcript(filename)
    #print(transcript_text)
    return transcript_text

def __download_video__(url:str,filename:str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'tools/video_ops/temp/{filename}',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Video downloaded with yt-dlp!")

def __download_audio__(url:str,filename:str):
    ######### COVERT TO MP3 (Requires ffmpeg installed.) #######################
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'tools/video_ops/temp/{filename}',
    }
    ##############################################################################
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def __get_metadata__(url:str):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        print(info_dict.keys())  # Show available metadata fields


if __name__ == "__main__":
    read_multimedia("99c9cc74-fdc8-46c6-8f8d-3ce2d3bfeea3.mp3")