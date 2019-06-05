import subprocess
import log

class Tools:
    def __init__(self):
        self.log = log.Log()
        pass
    # 提取视频中的音轨
    def separateAudio(self, source, destination):
        try:
            error = subprocess.call(
                'ffmpeg -i ' + source + ' -f mp3 -vn ' + destination, shell=True)
        except:
            self.log.info(error)

    # 将音频文件转为标准的PCM文件
    def mp32pcm(self, source, destination):
        try:
            error = subprocess.call(['ffmpeg', '-y', '-i', source,
                                     '-acodec', 'pcm_s16le',
                                     '-f', 's16le',
                                     '-ac', '1',
                                     '-ar', '16000', destination])
        except:
            self.log.info(error)