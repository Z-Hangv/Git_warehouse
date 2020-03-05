import xbase
import script.base_script as body
import script_server.server

def run(param_):
    m ={}
    m["action"] = "set_mood"
    m["mood_seed"] = param_
    body.stop_all_action()
    script_server.server.client_send( str(m))


if __name__ == '__main__':
    run("")