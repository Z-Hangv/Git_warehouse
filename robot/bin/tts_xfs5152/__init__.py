# -*- coding: utf-8 -*-
import time
import serial

class Tts:
    def init(self, com_):
        try:
            self.serial_handle = serial.Serial(com_, 9600)
            return True
        except Exception as e:
            print(e)
            return False

    def synthesis(self, text_, voice_feature_=1, can_break_=True):
        # print("systhesis: %s " % text_)
        data_ = self.Judge_state(can_break_)  # 判断语音合成状态 如果为不打断模式 当处于合成状态 退出
        if data_:
            print("正在合成语音中")
            return
        if voice_feature_ == 1:
            my_text = "[m3]" # 女声
        elif voice_feature_ == 2:
            my_text = "[m51]" # 男声
        elif voice_feature_ == 3:
            my_text = "[m53]" # 女声 成熟
        elif voice_feature_ == 4:
            my_text = "[m52]"  # 男声 成熟
        elif voice_feature_ == 5:
            my_text = "[m54]" # 唐老鸭
        else:
            my_text = "[m3]" # 女声

        my_text = my_text + text_
        encoding_flag = "01"
        if "GBK" == "GBK":   # 如果需要修改编码, 需要修改2个地方
            my_text = my_text.encode("GBK")
            encoding_flag = "01"


        my_len = len(my_text) + 2
        if my_len >= 4000:
            print("文本长度不能超过4000")
            return

        # send_data_list = [0xFD, 0x00, 0x01, 0x01, 0x01]  # 命令头 1、帧头 2和3、高字节 低字节（数据长度） 4、命令字（0x01-合成）5、文本编码格式
        send_data =bytes.fromhex("FD")
        len_byte = my_len.to_bytes(length=2, byteorder='big', signed=True)
        send_data = send_data + len_byte
        send_data = send_data + bytes.fromhex("01")
        send_data = send_data + bytes.fromhex(encoding_flag)
        send_data = send_data + my_text

        print(send_data)
        print(len(send_data))
        print("start loop")
        for i in range(len(send_data)):
            res = self.serial_handle.write(send_data[i:i+1])
            # if res <= 0:
            #     print("发送数据时时出现错误")
            #     break
            time.sleep(0.001)

    def Judge_state(self,break_): #break_ true为打断 false为不打断
        if break_ == False :
            self.serial_handle.write([0xFD,0x00,0x01,0x21])
            time.sleep(0.1)
            state = self.serial_handle.read(1)
            #state.hex()
            if state.hex() == "4e": #4E 在合成中 4F未合成
                return True
            else:
                return False
        return False

if __name__ == '__main__':
    tts = Tts()
    tts.init("com8")
    tts.synthesis("你好啊, 今天天气不错", 1, True)
    time.sleep(1)
    tts.synthesis("你好啊, 今天天气不错",1,  True)
