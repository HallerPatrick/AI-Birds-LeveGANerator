import subprocess
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

#import xml_generator.__main__ as gan_main
#import automator.prepare_samples.main as prepare_samples



def start_automator(config_data):

    # Start the xml generator
    #gan_main.main()

    # Move all levels to unity resource folder

    ##### POWERSHELL SCRIPT #####

    if sys.platform == "win":
        pwsh = "powershell"
    else:
        pwsh = "pwsh"

    subprocess.run([
        pwsh,
        "automator.ps1",
        config_data["unity_path"],
        config_data["autosizer_path"],
        config_data["client_path"],
        config_data["server_path"]
    ])

    #prepare_samples()
