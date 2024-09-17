import os
import sys
from termcolor import cprint, colored
import time
import subprocess
import readline
from help_command import *

def vi_cmd(args):
    try:
        result = subprocess.Popen(["vi"])
    except Exception as e:
        print(f"Exception.{e}")
def ping_cmd(args):
    try:
        result = subprocess.run(["ping",args[1]])
        print(result.stdout.strip())
    except IndexError as I:
        print(I)
    except KeyboardInterrupt:
        main()
def locate_cmd(args):
    try:
        result = subprocess.run(["locate",args[1]])
    except IndexError:
        print(f"help: locate [argument]")
    except KeyboardInterrupt:
        main()

def top_cmd(args):
    try:
        result = subprocess.run(["top"])
        print(result)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        main()
def du_cmd(args):
    try:
        if len(args) == 1:
            result = subprocess.run(["du"])
        elif len(args) == 2:
            if args[1] == "-h":
                result_h = subprocess.run(["du","-h"])
        else:
            print(f"help: du [argument]")

    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        main()

def remove_file(del_file,args):
    try:
        if len(args) == 2:
            os.remove(del_file)
    except FileNotFoundError:
        print(f"{del_file}: No such file or directory")
    except IsADirectoryError:
        print("Cannot delete directory")

def remove_directory(directory):
    try:
        os.rmdir(directory)
    except FileNotFoundError:
        print(f"{directory}: No such file or directory")

def create_directory(create_dir):
    try:
        os.makedirs(create_dir)
    except IndexError:
        print("help: mkdir [argument]")
    except OSError:
        print("cannot create directory")

def cat_command(show_file):
    files = show_file
    try:
        # loop durch die datei
        for i in files:
            # öffnen und lesen der datei
            with open(i, "r") as file:
                # zeige den inhalt
                cprint(file.read(), "white")
    except FileNotFoundError:
        print(f"{i}: No such file or directory")
    except PermissionError:
        print(f"{i}: Permission denied")
    except OSError:
        print(f"{i}: Invalid argument")

def run_python_file(python_file):
    liste = ["python3"] + python_file
    os.execvp("python3", liste)

def get_user_id(args):
    if len(args) < 2:
        user_id = os.getuid()
        print(user_id)

def show_history():
    history_length = readline.get_current_history_length()  # history length
    line_number = 0
    for i in range(1, history_length + 1):
        line_number += 1
        print(line_number, readline.get_history_item(i))
def list_files(args):
    if len(args) > 1 and args[1] == "-al":
            result = subprocess.run(["ls", "-al"], capture_output=True, text=True, check=True)
            print(result.stdout.strip())
    elif len(args) == 1:
            nummer = 0
            nummer_farbe = "yellow"
            datei_farbe = "white"
            dir_farbe = "blue"

            for i in os.listdir():
                nummer += 1
                if os.path.isdir(i):
                    print(colored(f"{nummer}", nummer_farbe), colored(i, dir_farbe))
                else:
                    print(colored(f"{nummer}", nummer_farbe), colored(i, datei_farbe))

            if nummer == 0:
                print("")

    elif len(args) > 1 and args[1] == "-a" or args[1] == "-all":
                result = subprocess.run(["ls", "-a"], capture_output=True, text=True, check=True)
                print(result.stdout.strip())
    elif len(args) > 1 and args[1] == "-r":
        ls_reverse = subprocess.run(["ls", "-r"], capture_output=True, text=True, check=True)
        print(ls_reverse.stdout.strip())
    elif len(args) > 1 and args[1] == "-t" or args[1] == "--time":
            sort_time = subprocess.run(["ls","-t"],capture_output=True,text=True,check=True)
            print(sort_time.stdout.strip())
    elif len(args) > 1 and args[1] == "-d" or args[1] == "--directory":
        ls_d = subprocess.run(["ls","-d"],capture_output=True,text=True,check=True)
        print(ls_d.stdout.strip())
    else:
        print(f"Invalid option for ls: {' '.join(args[1:])}")

def mv_cmd(args):
    try:
        result = subprocess.run(["mv",args[1],args[2]],capture_output=True,text=True,check=True)
        print(result.stdout.strip())
    except IndexError:
        print("help: mv [argument] [argument]")
def cp_cmd(args):
    try:
        result = subprocess.run(["cp",args[1],args[2]])
    except IndexError:
        print("help: cp [argument] [argument]")
def touch_cmd(args):
    try:
        result = subprocess.run(["touch",args[1]],capture_output=True,text=True,check=True)
        print(result.stdout.strip())
    except IndexError:
        print("help: touch [argument]")

def main():
    while True:
        path = os.getcwd()
        shell_symbol = "$"
        print(colored(path, "yellow"))
        sys.stdout.write(f"{shell_symbol} ")
        sys.stdout.flush()
        try:
            command = input()
        except KeyboardInterrupt:
            print("Stopped")
            sys.exit(0)
        args = command.split()
        try:
            cmd = args[0]
        except IndexError:
            continue

        if cmd == "echo":
            if len(args) > 1:
                print(" ".join(args[1:]))
            else:
                print("help: echo [type something ...]")

        elif cmd == "pwd":
            if len(args) == 1:
                pwd = os.getcwd()
                print(pwd)
            else:
                print("help: pwd")
        elif cmd == "type":
            if len(args) == 2:
                for arg in args[1:]:
                    if args[1] in ["type", "echo", "exit"]:
                        print(f"{arg} is a shell builtin")
                    else:
                        print(f"{arg}: not found")
            else:
                print("help: type [argument]")

        elif cmd == "exit":
            sys.exit(0)
        elif cmd == "cd":
            if len(args) > 1:
                path = args[1]
                if path == "~":
                    path = os.path.expanduser("~")
                try:
                    if len(args) > 1:
                        os.chdir(path)
                except FileNotFoundError:
                    print(f"{path}: No such file or directory")
                except NotADirectoryError:
                    print(f"{path}: Not a directory")
                except PermissionError:
                    print(f"{path}: permission denied")

        elif cmd == "file":
            try:
                result = subprocess.run(["file"] + args[1:], capture_output=True, text=True, check=True)
                print(result.stdout.strip())
            except Exception:
                print("help: file [argument] ")

        elif cmd == "ls":
            list_files(args)
        
        elif cmd == "cat":
            if len(args) > 1:
                cat_command(args[1:])
                if args[2] == "-n":
                    result = subprocess.run(["cat"] + args[:1],capture_output=True,text=True,check=True)
                    print(result)
        elif cmd == "clear":
            os.system("clear")
        elif cmd == "rmdir":
            if len(args) > 1:
                remove_directory(args[1])
        elif cmd == "rm":
            remove_file(args[1],args)
            try:
                if args[1] == "-r":
                    result = subprocess.run(["rm","-r"] + args[2:],capture_output=True,text=True,check=True)
                    print(result.stdout.strip())
            except subprocess.CalledProcessError:
                print(f"{args[2]}: No such file or directory")

        elif cmd == "mkdir":
            if len(args) > 1:
                if args[-1] == "-v":
                    print(f"{cmd}: created directory '{args[1]}'")
                    create_directory(args[1])
                else:
                    create_directory(args[1])


        elif cmd == "python3":
            # works but you get kicked out of the shell
            run_python_file(args[1:])
            time.sleep(1)

        elif cmd == "whoami":
            username = os.environ.get('USER') or os.environ.get('USERNAME')
            if username == "root":
                print(colored(username,"red"))

        elif cmd == "id":
            get_user_id(args)
        elif cmd == "history":
            show_history()
        elif cmd == "grep":
            try:
                FILE_DATA = args[2:]
                TEXT = args[1]
                command = ["grep", TEXT] + FILE_DATA
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                print(result.stdout.strip())
            except IndexError:
                print("help: grep [pattern] [file...]")
        elif cmd == "mv":
            mv_cmd(args)
        elif cmd == "cp":
            cp_cmd(args)
        elif cmd == "help":
            print(HELP)
        elif cmd == "touch":
            touch_cmd(args)
        elif cmd == "vi":
            vi_cmd(args)
        elif cmd == "ping":
            ping_cmd(args)
        elif cmd == "top":
            top_cmd(args)
        elif cmd == "locate":
            locate_cmd(args)
        elif cmd == "du":
            du_cmd(args)
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl + c
        print("Stopped")
    except OSError:
        print("No such device or adress.")

