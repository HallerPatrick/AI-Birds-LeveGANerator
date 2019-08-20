import json
import os
import time
import sys

import click
from clint.textui import puts, colored, prompt, validators
from pyfiglet import Figlet



CHECKED_SYMBOL = '✓'
FAILED_SYMBOL  = 'x'

BOLD_START = '\033[1m'
BOLD_END = '\033[0m'

json_template = {
    "client_path": "None",
    "server_path": "None",
    "unity_path": "None",
    "autosizer_path": "None"
}

config_data = {}
config_file_path = ""



def print_header():
    f = Figlet(font='slant')
    puts(f.renderText('AI BIRDS CLI'))

def check_path(path):
    return os.path.isfile(path)

def print_check():
    global config_data
    global config_file_path

    client_checked = check_path(config_data["client_path"])
    server_checked = check_path(config_data["server_path"])
    unity_checked = check_path(config_data["unity_path"])
    autosizer_checked = check_path(config_data["autosizer_path"])

    if client_checked:
        client_path_string = colored.green(config_data["client_path"] + " " + CHECKED_SYMBOL)
    else:
        client_path_string = colored.red(config_data["client_path"] + " " + FAILED_SYMBOL)

    if server_checked:
        server_path_string = colored.green(config_data["server_path"] + " " + CHECKED_SYMBOL)
    else:
        server_path_string = colored.red(config_data["unity_path"] + " " + FAILED_SYMBOL)

    if unity_checked:
        unity_path_string = colored.green(config_data["unity_path"] + " " + CHECKED_SYMBOL)
    else:
        unity_path_string = colored.red(config_data["unity_path"] + " " + FAILED_SYMBOL)

    if autosizer_checked:
        autosizer_path_string = colored.green(config_data["autosizer_path"] + " " + CHECKED_SYMBOL)
    else:
        autosizer_path_string = colored.red(config_data["autosizer_path"] + " " + FAILED_SYMBOL)
    
    puts(BOLD_START + "(1) Client path (mandatory)" + BOLD_END + ": " + client_path_string)
    puts(BOLD_START + "(2) Server path (mandatory)" + BOLD_END + ": " + server_path_string)
    puts(BOLD_START + "(3) Unity Game path (mandatory)" + BOLD_END + ": " + unity_path_string)
    puts(BOLD_START + "(4) Autosizer path (mandatory)" + BOLD_END + ": " + autosizer_path_string)

    if client_checked and server_checked and unity_checked:
        puts(colored.green("ALL SET!"))
        val = prompt.query("Start automator? [(y)es/n(o)/s(et path)]")
        
        if val == "y":
            from automator import start_automator

            start_automator(config_data)
            return
        elif val == "n":
            sys.exit(1)
        elif not val == "s":
            return
        
    choice = prompt.query('Set path (1/2/3/4/q)?', default='q')

    if choice == "q":
        with open(config_file_path, "r+") as f:
            json.dump(config_data, f)
        sys.exit(1)
    elif choice == "1":
        path = prompt.query('Installation Path for client jar', validators=[validators.FileValidator()])
        config_data["client_path"] = path
    elif choice == "2":
        path = prompt.query('Installation Path for server jar', validators=[validators.FileValidator()])
        config_data["server_path"] = path
    elif choice == "3":
        path = prompt.query('Installation Path for unity game', validators=[validators.FileValidator()])
        config_data["unity_path"] = path
    elif choice == "4":
        path = prompt.query('Installation Path autosizer', validators=[validators.FileValidator()])
        config_data["autosizer_path"] = path

    
    with open(config_file_path, "r+") as f:
        json.dump(config_data, f)

    

    
@click.command()
@click.option("--config-file", default="cfg.json", help="Json config holding all config values for starting automator")
def main(config_file):

    global config_file_path

    config_file_path = config_file

    global config_data

    if not os.path.isfile(config_file):
        puts("Creating new configs")
        config_data = json_template
        with open(config_file, "w") as _:
            pass
    else:
        puts("Reading config from file")
        with open(config_file, "r+") as f:
            config_data = json.load(f)

    main_loop()
    

def main_loop():
    while True:
        os.system('clear')
        print_header()
        print_check()


if __name__ == "__main__":
    main()
