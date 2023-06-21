PODCAST_INFO = [
    {
        "name": "Lex Fridman",
        "description": "麻省理工学院的人工智能专家Lex Fridman和知名科学家、企业家、作家等嘉宾进行深入对话,探讨人工智能、机器人、自动驾驶、生物技术等热门话题。",
        "metadata": {
            "podcast_url": "",
            "official_website": "",
            "youtube_url": "https://www.youtube.com/@lexfridman",
        }
    },{
        "name": "Huberman Lab",
        "description": "斯坦福大学的神经科学家Andrew Huberman帮助听众了解大脑如何影响身心健康、睡眠、情绪、创造力等。",
        "metadata": {
            "podcast_url": "",
            "official_website": "",
            "youtube_url": "https://www.youtube.com/@hubermanlab",
        }
    },{
        "name": "WorkLife",
        "description": "Adam Grant曾是沃顿商学院最年轻的教授,并已经连续7年成为沃顿商学院的最佳教授。也是《纽约时报》排名第一的畅销书作家。他的播客讲述了我们如何在工作中找到动力、创意和乐趣。",
        "metadata": {
            "podcast_url": "",
            "official_website": "https://adamgrant.net/podcasts/work-life/",
            "youtube_url": "",
        }
    },{
        "name": "Dare to Lead",
        "description": "Brené Brown是休斯顿大学的社会工作教授, 研究勇气、脆弱性和同理心。她曾在TED演讲中分享过自己对脆弱性的研究和体验,引起了全球观众的共鸣。",
        "metadata": {
            "podcast_url": "",
            "official_website": "https://brenebrown.com/podcast-show/dare-to-lead/",
            "youtube_url": "",
        }
    },{
        "name": "Unlocking Us",
        "description": "Brené Brown是休斯顿大学的社会工作教授, 研究勇气、脆弱性和同理心。她曾在TED演讲中分享过自己对脆弱性的研究和体验,引起了全球观众的共鸣。",
        "metadata": {
            "podcast_url": "",
            "official_website": "https://brenebrown.com/podcast-show/unlocking-us/",
            "youtube_url": "",
        }
    }          
    ]


def download_audio(url):
    pass

def download_video_txt(url):
    pass

def download_video_srt(url):
    pass

def download_transcript(url):
    pass

def trans_audio_to_text(audio):
    pass

def trans_srt_to_text(srt, text):
    from datetime import datetime
    # show notes时间戳
    timestamp_list = ['00:00:00','00:05:14', '00:09:29', '00:11:20', '00:12:27', '00:22:54', '00:26:36', '00:31:10', '00:32:54', '00:36:25', '00:37:54', '00:40:06','00:41:40']
    with open(srt, "r") as f:
        srt = f.read()
    # 分割时间戳和文本
    segments = srt.split("\n\n")
    # 分割文本并合并
    result = []
    for i in range(len(timestamp_list)):
        start = datetime.strptime(timestamp_list[i], '%H:%M:%S')
        if i < len(timestamp_list) - 1:
            end = datetime.strptime(timestamp_list[i+1], '%H:%M:%S')
        else:
            end = datetime.strptime("23:59:59", '%H:%M:%S')
        segment_text = timestamp_list[i]
        for j, segment in enumerate(segments):
            # 获取当前段落的时间戳
            tmp_str = segment.split("\n")
            if len(tmp_str) != 3:
                continue
            timestamp_str = tmp_str[1].split(" --> ")[0]
            timestamp_str = timestamp_str.replace(",", ".")
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')
            if start <= timestamp < end:
                # 如果在给定的时间戳范围内，则将当前段落添加到结果中
                segment_text += "," + segment.split("\n")[2]
            elif timestamp >= end:
                # 如果当前段落的时间戳大于等于给定的结束时间戳，则将其添加到结果中，并跳出循环
                result.append(segment_text)
                break
        if not result:
            # 如果结果为空，则将当前段落添加到结果中
            result.append(segment_text)
    # 将结果写入文件
    with open(text, "w") as f:
        for segment in result:
            f.write(segment + "\n")
    # 输出完成消息
    print("完成！已将结果写入output.txt文件中。")

def trans_english_to_chinese(text):
    pass

def trans_text_to_pdf(text):
    pass

def trans_text_to_epub(text):
    pass

def gernerate_summary(text ):
    pass


if __name__ == '__main__':
    pass