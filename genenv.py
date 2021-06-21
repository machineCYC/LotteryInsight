import os


def get_config_from_environment(env_content):
    # get config from env
    env_content += "MYSQL_HOST={}\n".format(os.environ.get("MYSQL_HOST", ""))
    env_content += "MYSQL_USER={}\n".format(os.environ.get("MYSQL_USER", ""))
    env_content += "MYSQL_PASSWORD={}\n".format(os.environ.get("MYSQL_PASSWORD", ""))
    env_content += "MYSQL_PORT={}\n".format(os.environ.get("MYSQL_PORT", ""))
    return env_content


env_content = ""
env_content = get_config_from_environment(env_content)

with open(".env", "w", encoding="utf8") as env:
    env.write(env_content)
