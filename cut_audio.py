import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


class CutAudio:
    def __init__(self, audio_path, mp3_path):
        self.audio_path = audio_path
        self.mp3_path = mp3_path
        self.cut_time_list = []

    def cut(self):        
        pass

    def getMp3Path(self):
        return self.mp3_path

    def getCutTimeList(self):
        return self.cut_time_list

# 静态切割
class SilenceCut(CutAudio):
    def __init__(self, audio_path, mp3_path):
        super().__init__(audio_path, mp3_path)
        print('silence cut')
        
    def cut(self):
        # 静音切割        
        song = AudioSegment.from_mp3(self.audio_path)        
        chunks = split_on_silence(song,
                                  # must be silent for at least 2 seconds or 2000 ms
                                  min_silence_len=50,
                                  # consider it silent if quieter than -16 dBFS
                                  # Adjust this per requirement
                                  silence_thresh=-10
                                  )
        
        # Process each mp3 per requirements
        count = 0
        for i, chunk in enumerate(chunks):
            # Create 0.5 seconds silence mp3
            silence_chunk = AudioSegment.silent(duration=500)
            # Add 0.5 sec silence to beginning and end of audio mp3
            audio_chunk = silence_chunk + chunk + silence_chunk
            # Normalize each audio mp3
            normalized_chunk = self.match_target_amplitude(audio_chunk, -20.0)
            # Export audio mp3 with new bitrate
            mp3_keep_path = self.mp3_path + os.sep + '{0}.mp3'.format(i)
            normalized_chunk.export(
                mp3_keep_path, bitrate='192k', format="mp3")
            
            # 统计时长
            audio = AudioSegment.from_mp3(mp3_keep_path)  # 打开mp3文件
            sound_len = round(audio.duration_seconds)
            from_time = self.second2time(count)
            to_time = self.second2time(count + sound_len)
            self.cut_time_list.append(from_time, to_time)
            count += sound_len

    def second2time(self, seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return self.changeFormat(hour) + ':' + self.changeFormat(minute) + ':' + self.changeFormat(second)

    def changeFormat(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)

    def match_target_amplitude(self, chunk, target_dBFS):
        ''' Normalize given audio mp3 '''
        change_in_dBFS = target_dBFS - chunk.dBFS
        return chunk.apply_gain(change_in_dBFS)

    def getCutTimeList(self):
        return self.cut_time_list

# 线性切割
class LinearCut(CutAudio):
    def __init__(self, audio_path, mp3_path):
        super().__init__(audio_path, mp3_path)
        print('linear cut')

    def cut(self):
        # 线性切割
        linear_trunk = AudioSegment.from_mp3(self.audio_path)  # 打开mp3文件
        sound_time = round(linear_trunk.duration_seconds)
        sound_len = sound_time // 30
        for i in range(sound_len):
            linear_trunk[i * 30000: (i + 1) * 30000].export(
                self.mp3_path + os.sep + '{0}.mp3'.format(i), bitrate='192k', format="mp3")

            from_time = self.second2time(i * 30)
            to_time = self.second2time((i + 1) * 30)

            self.cut_time_list.append((from_time, to_time))

            print(str(round(i * 30 / sound_time * 100)) + '%')
            # 切割前17.5秒并覆盖保存

    def second2time(self, seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return self.changeFormat(hour) + ':' + self.changeFormat(minute) + ':' + self.changeFormat(second)

    def changeFormat(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)

    def getCutTimeList(self):
        return self.cut_time_list

class CutFactory:
    def getCutProduct(self, audio_path, mp3_path, cut_way):
        if cut_way == 'slience':
            return SlienceCut(audio_path, mp3_path)
        if cut_way == 'linear':
            return LinearCut(audio_path, mp3_path)

#
# if __name__ == '__main__':
#     factory = CutFactory()
#     cut_product = factory.getCutProduct('../resource/audio/test_a.mp3', '../resource/audio/mp3', 'linear')
#     cut_product.cut()
#     print(cut_product.getCutTimeList())