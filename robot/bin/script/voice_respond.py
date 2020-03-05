import script.base_script as body

def run(param_):
    body.stop_all_action()
    flag = param_[0:2]
    question_id = param_[2:]
    if flag == "a8":
        print("不可识别的声音")
        return
    if flag == "a7":
        print("收到唤醒词")
        body.play_block("en.wav")
        return
    if flag == "a6":
        if question_id== "113":
            print("明月几时有")
            body.play_block("song.wav")
        elif question_id== "115":
            print("我欲乘风归去")
            body.play_block("song.wav")
        elif question_id== "116":
            print("起舞弄清影")
            body.play_block("song.wav")
        elif question_id== "117":
            print("转朱阁")
            body.play_block("song.wav")
        elif question_id== "118":
            print("不应有恨")
            body.play_block("song.wav")
        elif question_id== "119":
            print("人有悲欢离合")
            body.play_block("song.wav")
        else:
            print("我不知道答案")
            body.play_block("bye.wav")
    return


if __name__ == '__main__':
    run("")
