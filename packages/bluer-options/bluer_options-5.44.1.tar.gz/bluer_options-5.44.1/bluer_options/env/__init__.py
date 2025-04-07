from typing import Union
import os

from bluer_options.env.functions import load_config, load_env, get_env


ABCUL = " \\\n\t"


abcli_log_filename = os.getenv(
    "abcli_log_filename",
    "",
)


CYAN = "\033[36m"
GREEN = "\033[32m"
LIGHTBLUE = "\033[96m"
NC = "\033[0m"
RED = "\033[31m"

EOP = "\033[33m"

HOST_NAME: Union[None, str] = None

abcli_hostname = get_env("abcli_hostname")

BLUER_AI_WIFI_SSID = get_env("BLUER_AI_WIFI_SSID")
