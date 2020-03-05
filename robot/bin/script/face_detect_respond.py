import script.base_script as body

def run(param_):
    body.stop_all_action()
    body.play_block("welcome.wav")
    return

    # for i in range(10):
    #     body.sleep(1)
    #     res = protocol.get_face_data()
    #     m = eval(res)
    #     x = m["x"]
    #     y = m["y"]
    #     w = m["w"]
    #     h = m["h"]
    #     find = m["find"]
    #     if find == 0:
    #         continue
    #     time_ago = m["time_ago"]
    #     # if time_ago < 10 and w > 40:
    #     if  w > 40:
    #         xbias =int(( x + w/2 -320) * -100 /4000)
    #         ybias = int((y + h / 2 - 240) * 100 / 1000)
    #         print("bias")
    #         print(xbias)
    #         print(ybias)
    #         if abs(xbias) > 3:
    #             body.neck.left_right_relative(xbias, 20)
    #         if abs(ybias) > 5:
    #             body.neck.up_down_relative(ybias, 20)
    #
    # return


if __name__ == '__main__':
    run("")
