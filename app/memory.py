ledning_log = []
verksamhet_log = []

def save_message(user_type, role, content) -> None:
    if user_type == "ledning":
        ledning_log.append({"role": role, "content": content})
    elif user_type == "verksamhet":
        verksamhet_log.append({"role": role, "content": content})

def get_full_log(user_type):
    if user_type == "ledning":
        return ledning_log
    elif user_type == "verksamhet":
        return verksamhet_log
    return []

def reset_log(user_type: str):
    global ledning_log, verksamhet_log
    if user_type == "ledning":
        ledning_log = []
    elif user_type == "verksamhet":
        verksamhet_log = []
