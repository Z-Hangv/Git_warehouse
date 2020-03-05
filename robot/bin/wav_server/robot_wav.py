import pyaudio
import wave
import time
import xbase

class PlayWav:
    wav_file_path = ""
    play_flag = False

    def play(self, wav_file_, with_kouxing_):
        wav_file_path = wav_file_
        wf = wave.open(wav_file_path, 'rb')
        p = pyaudio.PyAudio()
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        self.m_stream = stream
        self.m_p = p
        self.m_wf = wf
        self.play_flag = True
        stream.start_stream()

        # while stream.is_active():
        #     if self.stop_sig:
        #         break
        #     time.sleep(0.1)
        #
        # stream.stop_stream()
        # stream.close()
        # wf.close()
        # p.terminate()

    def close(self): #如果播放完毕,这关闭通道节省资源
        if self.play_flag is not True:
            return
        if self.m_stream.is_active() is not True:
            self.m_stream.stop_stream()
            self.m_stream.close()
            self.m_wf.close()
            self.m_p.terminate()

    def stop(self): #无论如何都停止播放,关闭通道
        if self.play_flag is not True:
            return
        self.m_stream.stop_stream()
        self.m_stream.close()
        self.m_wf.close()
        self.m_p.terminate()

if __name__ == '__main__':
    w = PlayWav()
    w.play(xbase.get_sound_file_path("1.wav"), False)
    time.sleep(3)
    # w.stop()
    # w1 = PlayWav()
    # w1.play(r"C:\mycode\projects\xrobot4\home\sound\welcome.wav")
    # time.sleep(3)

