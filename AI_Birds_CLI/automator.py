import subprocess
import os
import sys
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

#import xml_generator.__main__ as gan_main
from AI_Birds_CLI import prepare_samples


def start_automator(config_data):

    cuda_envs = config_data["cuda"]

    os.environ["PATH"] += os.pathsep + cuda_envs

    # Start the xml generator
    #gan_main.main(config_data["parameters_file"], config_data["root"])

    # Move all levels to unity resource folder

    ##### POWERSHELL SCRIPT #####


    if sys.platform == "win32":
        pwsh = "powershell"
    else:
        pwsh = "pwsh"

    command = [
        pwsh,
        "-File ",
        os.getcwd() + "/automator.ps1",
        '{}'.format(config_data["unity_path"]),
        '{}'.format(config_data["autosizer_path"]),
        '{}'.format(config_data["client_path"]),
        '{}'.format(config_data["server_path"])
    ]

    
    subprocess.run(command)

    time.sleep(5)

    prepare_samples.main(config_data["root"], config_data["parameters_file"])
