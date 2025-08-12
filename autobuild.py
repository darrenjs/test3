import watchdog.observers
import watchdog.events
import time
import subprocess
import sys

# TODO: change this to point to your source dir
src_dir = "../src"

class colors:
    '''Colors class: reset all colors with colors.reset two subclasses fg for
    foreground and bg for background.  use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green also, the generic bold, disable,
    underline, reverse, strikethrough, and invisible work with the main class
    i.e. colors.bold

    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


def run_command_old():
    return_code = subprocess.call("make -j", shell=True)  #OLD
    if return_code == 0:
        sys.stdout.write(colors.fg.lightgreen)
        sys.stdout.write(colors.bold)
        print ("=== AUTOBUILD -- SUCCESS ===")
        sys.stdout.write(colors.reset)
    else:
        sys.stdout.write(colors.fg.red)
        sys.stdout.write(colors.bold)
        print ("=== AUTOBUILD -- FAILED ===")
        sys.stdout.write(colors.reset)


def run_command():

    autolog = "autobuild.log"
    with open(autolog, "w") as f:
        f.write("-*- mode: compilation; -*-\n");

    subprocess.call("echo build starting at $(date) 2>&1| tee --append autobuild.log", shell=True)
    cmd ="set -o pipefail; nice make -j $(nproc) 2>&1| tee --append autobuild.log"
    return_code = subprocess.call(["bash", "-c", cmd])
    if return_code == 0:
        sys.stdout.write(colors.fg.lightgreen)
        sys.stdout.write(colors.bold)
        print ("=== AUTOBUILD -- SUCCESS ===")
        sys.stdout.write(colors.reset)
    else:
        sys.stdout.write(colors.fg.red)
        sys.stdout.write(colors.bold)
        print ("=== AUTOBUILD -- FAILED ===")
        sys.stdout.write(colors.reset)



def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    run_command()


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
    run_command()


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
    run_command()


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    run_command()


def main():
    patterns = None
    ignore_patterns = ["*/.idea/*", "*/.git/*", "*/.git", ".#*"]
    ignore_directories = True
    case_sensitive = True
    my_event_handler = watchdog.events.PatternMatchingEventHandler(
        patterns=patterns,
        ignore_patterns=ignore_patterns,
        ignore_directories=ignore_directories,
        case_sensitive=case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = src_dir
    go_recursively = True
    my_observer = watchdog.observers.Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()



if __name__ == "__main__":
    main()




# autobuild ()
# {
#     fgbold=`tput bold`;
#     fgred=`tput setaf 1`;
#     fggreen=`tput setaf 2`;
#     treset=`tput sgr0`;
#     lastmake="0000-00-00 00:00:00";
#     while :; do
#         highmodstat=`find .  -regextype posix-egrep  \( \( -iregex '.*\.c[cp]*' -o -name \*h \) -a -type f \) -exec stat --format "%y%n" '{}' \; | sort | tail -1`;
#         highmodstamp=`echo $highmodstat  | cut -b 1-19`;
#         if [ "${highmodstamp}" \> "${lastmake}" ]; then
#             echo $highmodstat;
#             make -j 4;
#             errcode=$?;
#             lastmake="${highmodstamp}";
#             echo;
#             if [ $errcode -eq 0 ]; then
#                 echo ${fgbold}${fggreen}"     "=== AUTOBUILD -- SUCCESS ===${treset};
#             else
#                 echo ${fgbold}${fgred}"     "=== AUTOBUILD -- FAILED ===${treset};
#             fi;
#             echo;
#         fi;
#         usleep 750000;
#     done
# }
