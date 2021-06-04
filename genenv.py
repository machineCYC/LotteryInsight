import os
from configparser import ConfigParser


# def get_config_from_environment(env_content):
#     # get config from env
#     env_content += "MYSQL_HOST={}\n".format(os.environ.get("MYSQL_HOST", ""))
#     env_content += "MYSQL_USER={}\n".format(os.environ.get("MYSQL_USER", ""))
#     env_content += "MYSQL_PASSWORD={}\n".format(os.environ.get("MYSQL_PASSWORD", ""))
#     return env_content

local_config = ConfigParser()
local_config.read("config.ini")

status = os.environ.get("VERSION", "")
section = local_config[status] if status else local_config["DEFAULT"]

env_content = ""
for sec in section:
    env_content += "{}={}\n".format(sec.upper(), section[sec])

# env_content = get_config_from_environment(env_content)

with open(".env", "w", encoding="utf8") as env:
    env.write(env_content)
