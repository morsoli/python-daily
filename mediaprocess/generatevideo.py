# -*- coding: UTF-8 -*-

import os
import json
import sys
import cv2
import requests
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_KEY = os.environ.get("PEXELS_API_KEY")

class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class PexelsRestClient(SingletonClass):
    def __init__(self) -> None:
        self.timeout = 30
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {
            "Authorization": API_KEY
        }
    
    def _get(self, url, params):
        full_url = self.base_url + url
        response = requests.get(url=full_url,params=params,headers=self.headers,verify=False,timeout=self.timeout)
        if response.status_code != 200:
            print("Pexels response error: {}".format(response.status_code))
            return
        response_data = json.loads(response.text)
        return response_data

    def get_collections_photos(self, collection_id):
        url = "/collections/{}".format(collection_id)
        params = {
            "type": "photos",
            "per_page": 80
        }
        collections = self._get(url, params)
        if not collections:
            return
        media = collections.get("media")
        if not media:
            return
        photos = []
        for item in media:
            photos.append(item.get("src").get("original"))
        return photos


class CommonGernerateVideo(object):
    def __init__(self, video_name, video_formt="mp4v" ,fps=0.5) -> None:
        self.video_name = video_name
        self.fps = fps
        self.video_size = (6720, 6720)
        self.image_path = "./images/"
        self.audio_path = "./audios/"
        self.video_tmp = "./videos/{}.mp4".format(video_name+"_tmp")
        self.pexels_client = PexelsRestClient()
        self.video_formt = cv2.VideoWriter_fourcc(*video_formt)

    def download_file(self, url, name):
        try: 
            if os.path.exists(name):
                return
            data = requests.get(url).content
            with open(name, "wb") as f:
                f.write(data)
                f.close()
        except Exception as e:
            print("download file failed!!!")
            print(e)

    def get_image(self, image_url, item):
        image_name = "{}_{}.jpg".format(self.video_name, item)
        save_path = self.image_path + "/" + image_name
        self.download_file(image_url, save_path)
        return save_path
    
    def composite_video(self, collection_id):
        images = self.pexels_client.get_collections_photos(collection_id)
        if not images:
            print("get image faild: {}".format(images))
            return False

        try:
            if os.path.exists(self.video_tmp):
                return True
            video_writer = cv2.VideoWriter(self.video_tmp, self.video_formt, self.fps, self.video_size)
            for i in tqdm(range(0, len(images))):
                image_path = self.get_image(images[i], i)
                frame = cv2.imread(image_path)
                resize_frame = cv2.resize(frame, self.video_size)
                video_writer.write(resize_frame)
            video_writer.release()
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
    for path in ["./images", "./videos", "./audios"]:
        if not os.path.exists(path):
            os.mkdir(path)


def generate_video():
    # https://www.pexels.com/zh-cn/collections/feeling-happy-hzn4cx4/
    pexels_collections_id = "x2gadw0"
    video_name = "smile"

    # https://www.fiftysounds.com/music/the-best-time.zip
    audio_name = "The Best Time.mp3"
    video = CommonGernerateVideo(video_name)

    print("图片正在整和成视频，请稍后片刻")
    if not video.composite_video(pexels_collections_id):
        sys.exit(-1)

    print("正在给视频加入音频")
    if not video.generate_video(audio_name):
        sys.exit(-1)


if __name__ == "__main__":
    init_path()
    generate_video()