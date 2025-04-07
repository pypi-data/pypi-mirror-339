from fellow.utils.format_message import format_ai_message


def log_message(config, name, color, content, formatter=format_ai_message):
    if config.get("log"):
        with open(config["log"], "a", encoding="utf-8") as f:
            f.write(formatter(name=name, color=color, content=content))

def clear_log(config):
    if config.get("log"):
        with open(config["log"], "w", encoding="utf-8") as f:
            f.write("")