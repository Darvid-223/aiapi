from datetime import datetime


def log_conversation(prompt: str, response: str, log_file: str = "conversation_log.txt"):
    """
    Logs the user's prompt and the assistant's response to a file.

    Args:
        prompt (str): The user's input.
        response (str): The assistant's response.
        log_file (str): The file where the conversation will be logged.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\nUser: {prompt}\nAssistant: {response}\n{'-'*40}\n"
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)