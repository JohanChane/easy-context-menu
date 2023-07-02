import os, sys
from ecm_util import EasyContextMenu
from ecm_util import str_menu_type

SCRIPT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CFG_DIR = os.path.join(SCRIPT_PATH, "confs")

def select(options):
    print("Please select an option:")
    for i, item in enumerate(options):
        print(i, item)

    try:
        choice = int(input("Enter your choice (num): "))
    except ValueError:
        choice = len(options)
    if choice < 0:
        choice = len(options)

    return choice

def get_file_names(dir):
    file_nams = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    file_nams.sort()
    return file_nams
    
def main():
    options = ["add", "del", "restart", "exit"]
    while True:
        print()
        choice = select(options)
        if choice >= len(options):
            print("Invalid selection, please try again")
            continue
        choiced_option = options[choice]
        if choiced_option == "add":
            cfg_names = get_file_names(CFG_DIR)
            index = select(cfg_names)
            if index >= len(cfg_names):
                print("backward")
                continue
            cfg_path = os.path.join(CFG_DIR, cfg_names[index])
            easy_context_menu = EasyContextMenu(cfg_path)
            added_menus = easy_context_menu.add_context_menus()
            print("Added menus:")
            [print(f'-   {str_menu_type(i)}') for i in added_menus]

        if choiced_option == "del":
            cfg_names = get_file_names(CFG_DIR)
            index = select(cfg_names)
            if index >= len(cfg_names):
                print("backward")
                continue
            cfg_path = os.path.join(CFG_DIR, cfg_names[index])
            easy_context_menu = EasyContextMenu(cfg_path)
            deled_menus = easy_context_menu.del_context_menus()
            print("Deled menus:")
            [print(f'-   {str_menu_type(i)}') for i in deled_menus]

        elif choiced_option == "restart":
            exec = sys.executable
            os.execl(exec, exec, * sys.argv)
        elif choiced_option == "exit":
            break;
        else:
            sys.stderr.write("Not match the option")
            
if __name__ == "__main__":
    main()