# -*- coding: UTF-8 -*-

import os
import json
import sys
import cv2
import requests
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
COVERR_API_KEY = os.environ.get("COVERR_API_KEY")
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance

  
class VideoRestClient(SingletonClass):
    def _get(self, url, params):
        full_url = self.base_url + url
        response = requests.get(url=full_url,params=params,headers=self.headers,verify=False,timeout=self.timeout)
        if response.status_code != 200:
            print("Pexels response error: {}".format(response.status_code))
            return
        response_data = json.loads(response.text)
        return response_data


class PexelsRestClient(VideoRestClient):
    def __init__(self) -> None:
        self.timeout = 30
        self.base_url = "https://api.pexels.com"
        self.headers = {
            "Authorization": PEXELS_API_KEY
        }
    
    def get_video_url(self, video):
        video_files = video.get("video_files")
        if not video_files:
            return
        for video_file in video_files:
            if video_file.get("width") == 1920 and video_file.get("height") == 1080:
                return video_file.get("link")
    # https://www.pexels.com/zh-cn/api/documentation/#videos-search
    def search_videos(self, query_string="yellow flowers"):
        url = "/videos/search"
        params = {
            "query": query_string,
            "per_page": 2
        }
        collections = self._get(url, params)
        if not collections:
            return
        media = collections.get("videos")
        if not media:
            return
        videos = []
        for item in media:
            videos.append(self.get_video_url(item))
        return videos


class CoverrRestClient(VideoRestClient):
    def __init__(self) -> None:
        self.timeout = 30
        self.base_url = "https://api.coverr.co"
        self.headers = {
            "Authorization": "Bearer {}".format(COVERR_API_KEY)
        }
    # https://api.coverr.co/docs/videos/#search-videos
    def search_videos(self, query_string="yellow flowers"):
        url = "/videos"
        params = {
            "query": query_string,
            "page_size": 20
        }
        collections = self._get(url, params)
        if not collections:
            return
        print(collections)
        

class PixabayRestClient(VideoRestClient):
    def __init__(self) -> None:
        self.timeout = 30
        self.base_url = "https://pixabay.com/api/"
        self.api_key = PEXELS_API_KEY
        self.headers = None

    # https://pixabay.com/api/docs/#api_key
    def search_videos(self, query_string="yellow+flowers"):
        url = "videos"
        params = {
            "q": query_string,
            "key": self.api_key,
            "per_page": 20,
            "video_type": "film"
        }
        collections = self._get(url, params)
        if not collections:
            return
        print(collections)


class CommonGernerateVideo(object):
    def __init__(self, video_name, video_formt="mp4v" ,fps=0.5) -> None:
        self.video_name = video_name
        self.fps = fps
        self.video_size = (1920, 1080)
        self.video_path = "./videos/"
        self.audio_path = "./audios/"
        self.video_tmp = "./video/{}.mp4".format(video_name+"_tmp")
        self.pexels_client = PexelsRestClient()
        self.video_formt = cv2.VideoWriter_fourcc(*video_formt)


    def download_file(self, url, filename):
        # Set up the request headers with a user agent to avoid server blocking
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        # Send a request to get the file size
        response = requests.head(url, headers=headers)
        file_size = int(response.headers.get("Content-Length", 0))
        # Create a progress bar to track the download progress
        progress_bar = tqdm(total=file_size, unit="iB", unit_scale=True)
        # Set up a stream to download the file in chunks
        chunk_size = 1024
        stream = requests.get(url, headers=headers, stream=True)
        # Write the file to disk in chunks
        with open(filename, "wb") as file:
            for chunk in stream.iter_content(chunk_size=chunk_size):
                # Update the progress bar
                progress_bar.update(len(chunk))
                # Write the downloaded chunk to the file
                file.write(chunk)
        # Close the progress bar
        progress_bar.close()

    def get_video(self, video_url, item):
        video_name = "{}_{}.mp4".format(self.video_name, item)
        save_path = self.video_path + video_name
        # TODO
        return save_path
        self.download_file(video_url, save_path)
        return save_path
    
    def composite_video(self):
        videos = self.pexels_client.search_videos()
        if not videos:
            print("get video faild: {}".format(videos))
            return False

        try:
            if os.path.exists(self.video_tmp):
                return True
            video_list = []
            for i in tqdm(range(0, len(videos))):
                video_path = self.get_video(videos[i], i)
                clip = VideoFileClip(video_path)
                video_list.append(clip)

            # 将视频片段连接在一起
            final_clip = concatenate_videoclips(video_list)
            # 将最终视频保存到本地
            final_clip.write_videofile(self.video_tmp)
        except Exception as e:
            print("composite video failed!!!")
            print(e)
            return False
        return True

    def generate_video(self, audio_name):
        video = VideoFileClip(self.video_tmp)
        audio = AudioFileClip(self.audio_path+audio_name)
        if video.duration > audio.duration:
            video = video.subclip(0, int(audio.duration))
        else:
            audio = audio.subclip(0, int(video.duration))

        videos = video.set_audio(audio)
        videos.write_videofile(self.video_name+".mp4", audio_codec='aac')


def init_path():
    for path in ["./video", "./videos", "./audios"]:
        if not os.path.exists(path):
            os.mkdir(path)


def generate_video():
    video_name = "smile"
    audio_name = "test.mp3"
    video = CommonGernerateVideo(video_name)

    print("图片正在整和成视频，请稍后片刻")
    if not video.composite_video():
        sys.exit(-1)

    print("正在给视频加入音频")
    if not video.generate_video(audio_name):
        sys.exit(-1)


if __name__ == "__main__":
    init_path()
    generate_video()