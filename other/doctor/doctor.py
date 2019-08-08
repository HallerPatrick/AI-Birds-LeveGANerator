# -*- coding: UTF-8 -*-

import importlib
import os
import subprocess
import sys

DOCTOR_REQUIREMENTS = "other/doctor/requirements_doctor.txt"

CHECKED_SYMBOL = '✓'
WARNING_SYMBOL = '!'
FAILED_SYMBOL  = 'x'

BOLD_START = '\033[1m'
BOLD_END = '\033[0m'


REQUIRED_PY = (3, 7)
REQUIREMENTS = "other/doctor/requirments/requirements.txt"

# Nome packges have other names when getting imported 
PACKAGE_NAMES = {
    "Keras": "keras",
    "opencv-python": "cv2",
    "Pillow": "PIL"
}

def install(package):
    """
    Function that installed python packages to executing python pip package
    silently if not already installed


    """
    try:
        stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        importlib.import_module(package)
        sys.stderr = stderr
    except ImportError:
        try:
            subprocess.check_output([sys.executable, "-m", "pip", "install", package])
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    print("This Script should should only be run with a python3 interpreter as the project uses python3.")
    print("WARNING: This script is eventually installing packages on the currently used python interpreter")
    ans = input("Still continue? [y/N]")
    if ans != "y":
        sys.exit(1)
    
    with open(DOCTOR_REQUIREMENTS, "r") as f:
        reqs = f.readlines()

    for req in reqs:
        install(req)

    run_doctor()


def run_doctor():
    import distutils.spawn
    import importlib
    import platform
    import subprocess

    from clint.textui import (
        colored,
        prompt,
        puts,
        indent,
        validators
    )
    from halo import Halo
    from pyfiglet import Figlet

    def install_swipl(platform_os):
        if platform_os == "Darwin":
            try:
                stderr = sys.stderr
                sys.stderr = open(os.devnull, 'w')
                subprocess.check_output(["brew", "install" , "swi-prolog"])
                sys.stderr = stderr
                return True
            except subprocess.CalledProcessError:
                return False
        
        if platform_os == "Windows":
            try:
                stderr = sys.stderr
                sys.stderr = open(os.devnull, 'w')
                subprocess.check_output(["choco", "install" , "swi-prolog"])
                sys.stderr = stderr
                return True
            except subprocess.CalledProcessError:
                return False

        if platform_os == "Linux":
            try:
                stderr = sys.stderr
                sys.stderr = open(os.devnull, 'w')
                subprocess.check_output(["apt-get", "install" , "swi-prolog"])
                sys.stderr = stderr
                return True
            except subprocess.CalledProcessError:
                return False
        

    HEADER = Figlet(font='slant').renderText('Doctor')

    #def find_all_python_interpreters():
    #    py = distutils.spawn.find_executable("python")
    #    py3 = distutils.spawn.find_executable("python3")
    #    return [py, py3]

   
    puts(HEADER)
    puts()

    #puts("Following Python interpreters are found")
    #interpreter_paths = find_all_python_interpreters()
    #options = [
    #    *[{"selector": no, "prompt": path, "return": path} for no, path in enumerate(interpreter_paths)],
    #    {"selector": len(interpreter_paths)+1, "prompt": "Select other interpreter", "return": "other"}
    #]

    #interpreter = prompt.options("Which python interpreter to use?", options)

    #if interpreter == "other":
    #    puts(colored.red("Please choose a python 3.7!"))
    #    interpreter = prompt.query('Installation Path of interpreter', validators=[validators.FileValidator()])

    platform_os = platform.system()

    puts("Running script from: {}".format(platform_os))

    if platform_os in ["Darwin", "Linux"]:
        with indent(4):
            puts(colored.yellow("Parts of this project will probably not run on this OS, please try to execute on Windows"))

    puts()
    puts(colored.blue(BOLD_START + "Python Interpreter" + BOLD_END))
    puts()
    # Check if python 3.7 is installed
    #if sys.version_info < REQUIRED_PY:
    #    puts(colored.yellow("Doctor executed with python version < 3.7"))
    #    answer = prompt.yn("Do you still want to run doctor? (Packages will then be installed on current running interpreter", default="n")
    #    
    #    if answer:
    #        sys.exit(1)

    # Check for site-packages

    puts("Checking Python site-packages...")
    all_installed = True 
    with open(REQUIREMENTS) as f:
        requirements = f.readlines()
    requirements_name = [req.strip().split("==")[0] for req in requirements if not req.startswith("#")]
    not_installed_packges = []
    
    for req in requirements_name:
        if req in PACKAGE_NAMES:
            req = PACKAGE_NAMES[req]
        try:
            # Import everything silently
            stderr = sys.stderr
            sys.stderr = open(os.devnull, 'w')
            importlib.import_module(req)
            sys.stderr = stderr
            with indent(4):
                puts(colored.green("[{}] ".format(CHECKED_SYMBOL) + "{} already installed".format(req)))
        except ImportError as e:
            all_installed = False 
            not_installed_packges.append(req)
            with indent(4):
                puts(colored.red("[{}] ".format(FAILED_SYMBOL) + "{} not installed".format(req)))

    if not all_installed:
        install_answer = prompt.yn("Installing all missing modules?", default="n")

        if not install_answer:
            for req in not_installed_packges:
                spinner = Halo(text="Installing package {}...".format(req), spinner='dots')
                spinner.start()
                succesfull = install(req)
                spinner.stop()
                
                if succesfull:
                    puts(colored.green("Installation of {} succesfully".format(req)))
                else:
                    puts(colored.red("Installation failed. Try it manually"))



    # Maybe Cuda


    # Client/Server

    puts()
    puts(colored.blue(BOLD_START + "Java" + BOLD_END))
    puts()
    # Check if java in path
    java_path = distutils.spawn.find_executable("java")

    if java_path:
        puts(colored.green("[{}] ".format(CHECKED_SYMBOL)) + "Java path found at: {}".format(java_path))
    else:
        puts(colored.red("[{}]".format(FAILED_SYMBOL)) + "Java in path not found")

    puts()
    puts(colored.blue(BOLD_START + "Swipl" + BOLD_END))
    puts()
    # Check if swipl insalled
    swiple_path = distutils.spawn.find_executable("swipl")

    if swiple_path:
        puts(colored.green("[{}] ".format(CHECKED_SYMBOL)) + "Swipl path found at: {}".format(swiple_path))
    else:
        puts(colored.red("[{}]".format(FAILED_SYMBOL)) + "Swipl in path not found")

        brew = distutils.spawn.find_executable("brew")

        if brew:
            puts()
            ans = prompt.yn("Should swipl be installed with package manager?", default="n")
            if not ans:
                spinner = Halo(text="Installing swipl...")
                spinner.start()
                successfully = install_swipl(platform_os)
                spinner.stop()
                if successfully:
                    puts(colored.green("[{}] Successfully installed swipl".format(CHECKED_SYMBOL)))
                else:
                    puts(colored.red("[] Could not install swipl".format(FAILED_SYMBOL)))
            else:
                puts()
                puts("If swipl is not installed please use a package manager or manually install it")
                puts("E.g")
                with indent(2):
                    puts("Windows: (Chocolatey)")
                    with indent(4):
                        puts("choco intall swi-prolog")
                    puts()
                    puts("Mac: (Homebrew)")
                    with indent(4):
                        puts("brew intall swi-prolog")
                    puts()
                    puts("Linux: (apt-get)")
                    with indent(4):
                        puts("apt-get intall swi-prolog")

    # Automator

        

if __name__ == "__main__":
    main()
