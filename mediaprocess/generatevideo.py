# -*- coding: UTF-8 -*-

import os
import json
import sys
import cv2
import requests
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip, concatenate_audioclips
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
                res = requests.get(video_file.get("link"), allow_redirects=True, timeout=self.timeout)
                if res.status_code == 200:    
                    return res.url
                
    # https://www.pexels.com/zh-cn/api/documentation/#videos-search
    def search_videos(self, query_string):
        url = "/videos/search"
        params = {
            "query": query_string,
            "per_page": 20,
            "page": 2
        }
        collections = self._get(url, params)
        if not collections:
            return
        media = collections.get("videos")
        if not media:
            return
        videos = []
        for item in media:
            original_url = self.get_video_url(item)
            print(original_url)
            videos.append(original_url)
        return videos


class CoverrRestClient(VideoRestClient):
    def __init__(self) -> None:
        self.timeout = 30
        self.base_url = "https://api.coverr.co"
        self.headers = {
            "Authorization": "Bearer {}".format(COVERR_API_KEY)
        }
    # https://api.coverr.co/docs/videos/#search-videos
    def search_videos(self, query_string):
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
    def search_videos(self, query_string):
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
    def __init__(self, video_name, videos_client, video_formt="mp4v" ,fps=0.5) -> None:
        self.video_name = video_name
        self.fps = fps
        self.video_size = (1920, 1080)
        self.video_path = "./videos/"
        self.audio_path = "./audios/"
        self.audio_tmp = "./audio/{}.mp3".format(video_name+"_tmp")
        self.video_tmp = "./video/{}.mp4".format(video_name+"_tmp")
        self.videos_client = videos_client
        self.video_formt = cv2.VideoWriter_fourcc(*video_formt)


    @staticmethod
    def download_file(url, filename):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.head(url, headers=headers)
        file_size = int(response.headers.get("Content-Length", 0))
        progress_bar = tqdm(total=file_size, unit="iB", unit_scale=True)
        chunk_size = 1024
        stream = requests.get(url, headers=headers, stream=True)
        with open(filename, "wb") as file:
            for chunk in stream.iter_content(chunk_size=chunk_size):
                progress_bar.update(len(chunk))
                file.write(chunk)
        progress_bar.close()
    
    def get_video(self):
        videos = self.videos_client.search_videos(self.video_name)
        if not videos:
            return False
        try:
            if os.path.exists(self.video_tmp):
                return True
            for i in tqdm(range(len(videos))):
                if not videos[i]:
                    continue
                video_name = "{}_{}.mp4".format(self.video_name, i)
                save_path = self.video_path + video_name
                self.download_file(videos[i], save_path)
        except Exception as e:
            print(e)
            return False
        return True
    
    def concatenate_audio(self):
        audio_files = []
        for filename in os.listdir(self.audio_path):
            audio_file= os.path.join(self.audio_path, filename)
            if not audio_file.endswith('.mp3'):
                continue
            # 加载每个音频文件并创建AudioFileClip对象
            print(audio_file)
            audio_files.append(AudioFileClip(audio_file))
        # 使用concatenate_audioclips函数拼接音频文件
        concatenated_clip = concatenate_audioclips(audio_files)
        # 将结果写入新的音频文件
        concatenated_clip.write_audiofile(self.audio_tmp)
        return True
    
    def concatenate_video(self):
        video_files = []
        for filename in os.listdir(self.video_path):
            video_file= os.path.join(self.video_path, filename)
            if not video_file.endswith('.mp4'):
                continue
            # 加载每个视频文件并创建VideoFileClip对象
            video_files.append(VideoFileClip(video_file))
        # 使用concatenate_videoclips函数拼接音频文件
        concatenated_clip = concatenate_videoclips(video_files)
        # 将结果写入新的视频文件
        concatenated_clip.write_videofile(self.video_tmp)
        return True

    def generate_video(self):
        video = VideoFileClip(self.video_tmp)
        audio = AudioFileClip(self.audio_tmp)
        if video.duration > audio.duration:
            video = video.subclip(0, int(audio.duration))
        else:
            audio = audio.subclip(0, int(video.duration))

        videos = video.set_audio(audio)
        videos.write_videofile(self.video_name+".mp4", audio_codec='aac')
        return True
        

def init_path():
    for path in ["./video", "./videos", "./audios", "./audio"]:
        if not os.path.exists(path):
            os.mkdir(path)

def release_resource():
    for path in ["./video", "./videos", "./audio"]:
        if os.path.exists(path):
            os.remove(path)
                
def generate_video():
    video_client = PexelsRestClient()
    video = CommonGernerateVideo(video_name="mountain lake", videos_client=video_client)
    video.get_video()

    print("正在合成视频中。。。")
    if not video.concatenate_video():
        sys.exit(-1)
        
    print("正在合成音频中。。。")
    if not video.concatenate_audio():
        sys.exit(-1)
        
    print("剪辑视频中。。。")
    if not video.generate_video():
        sys.exit(-1)


if __name__ == "__main__":
    init_path()
    generate_video()
    release_resource()