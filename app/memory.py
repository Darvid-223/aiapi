chat_log = []

def save_message(role, content) -> None: 
    chat_log.append({"role": role, "content": content})

def get_full_log():
    return chat_log
