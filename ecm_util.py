import os, subprocess, configparser, tempfile
from enum import Enum
import winreg

class MenuType(Enum):
    ON_FILE = 0
    ON_DIR = 1
    ON_DIR_BG = 2

def str_menu_type(menu_type):
    menu_type_str = ""
    if menu_type == MenuType.ON_FILE:
        menu_type_str = "TheMenuOnFile"
    elif menu_type == MenuType.ON_DIR:
        menu_type_str = "TheMenuOnDir"
    elif menu_type == MenuType.ON_DIR_BG:
        menu_type_str = "TheMenuOnDirBg"
    return menu_type_str

class EasyContextMenu():
    def __init__(self, cfg_path):
        self.__cfg_path = cfg_path
        config = configparser.ConfigParser()
        config.read(cfg_path)
        self.__pragram_path = config.get("main", "program_path", fallback=None)
        self.__menu_icon_path = config.get("main", "menu_icon_path", fallback=None)
        self.__menu_name = config.get("main", "menu_name", fallback=None)
        self.__sub_key_name = config.get("main", "sub_key_name", fallback=None)

        self.__menu_info = {MenuType.ON_FILE: {}, MenuType.ON_DIR: {}, MenuType.ON_DIR_BG: {}}
        self.__menu_info[MenuType.ON_FILE]["enable"] = config.has_section("menu_on_file")
        self.__menu_info[MenuType.ON_DIR]["enable"] = config.has_section("menu_on_dir")
        self.__menu_info[MenuType.ON_DIR_BG]["enable"] = config.has_section("menu_on_dir_bg")
        self.__menu_info[MenuType.ON_FILE]["is_extended"] = config.getboolean("menu_on_file", "is_extended", fallback=None)
        self.__menu_info[MenuType.ON_DIR]["is_extended"] = config.getboolean("menu_on_dir", "is_extended", fallback=None)
        self.__menu_info[MenuType.ON_DIR_BG]["is_extended"] = config.getboolean("menu_on_dir_bg", "is_extended", fallback=None)
        self.__menu_info[MenuType.ON_FILE]["param"] = config.get("menu_on_file", "param", fallback=None)
        self.__menu_info[MenuType.ON_DIR]["param"] = config.get("menu_on_dir", "param", fallback=None)
        self.__menu_info[MenuType.ON_DIR_BG]["param"] = config.get("menu_on_dir_bg", "param", fallback=None)

    def add_context_menus(self):
        menus = []
        for m in self.__get_enable_menu():
            self.add_the_context_menu(m)
            menus.append(m)
        return menus
            
    def del_context_menus(self):
        menus = []
        for m in self.__get_enable_menu():
            self.del_the_context_menu(m)
            menus.append(m)
        return menus
    
    def query_context_menu_registrys(self):
        for m in self.__get_enable_menu():
            self.__query_registry(f'HKEY_CLASSES_ROOT\\{self.__get_sub_key_path(m)}')

    def export_context_menu_registrys(self, out_dir):
        cfg_name = os.path.basename(self.__cfg_path).split(".")[0]
        out_reg_path = os.path.join(out_dir, cfg_name + ".reg")
        out_reg_dir = os.path.dirname(out_reg_path)
        if not os.path.exists(out_reg_dir):
            os.makedirs(out_reg_dir, exist_ok=True)

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_path = temp_file.name
        temp_file.close()
        with open(out_reg_path, "w") as f:
            for m in self.__get_enable_menu():
                self.__export_registry(f'HKEY_CLASSES_ROOT\\{self.__get_sub_key_path(m)}', temp_file_path, True)
                with open(temp_file_path, "r", encoding="utf-16") as tf:
                    f.write(tf.read())
        os.remove(temp_file_path)
        print(f'Export to the file: {out_reg_path}')
        
    def add_the_context_menu(self, menu_type):
        sub_key_path = self.__get_sub_key_path(menu_type)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, self.__menu_name)
            if self.__menu_icon_path:
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, self.__menu_icon_path)

        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key_path + '\\command') as key:
            menu_command = r"{}".format(self.__pragram_path)
            if self.__menu_info[menu_type]["param"]:
                menu_command += r" {}".format(self.__menu_info[menu_type]["param"])

            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_command)
            
        if self.__menu_info[menu_type]["is_extended"]:
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key_path) as key:
                winreg.SetValueEx(key, "Extended", 0, winreg.REG_SZ, "")

    def del_the_context_menu(self, menu_type):
        sub_key_path = self.__get_sub_key_path(menu_type)
        self.__delete_registry_tree(winreg.HKEY_CLASSES_ROOT, sub_key_path)
    
    def __get_sub_key_path(self, menu_type):
        if menu_type == MenuType.ON_FILE:
            sub_key_path = "*\\shell\\" + self.__sub_key_name
        elif menu_type == MenuType.ON_DIR:
            sub_key_path = "Directory\\shell\\" + self.__sub_key_name
        elif menu_type == MenuType.ON_DIR_BG:
            sub_key_path = "Directory\\Background\\shell\\" + self.__sub_key_name
        else:
            sub_key_path = None
            
        return sub_key_path
    def __get_enable_menu(self):
        return [k for k, v in self.__menu_info.items() if v["enable"]]
    
    @staticmethod
    def __delete_registry_tree(root_key, sub_key):
        try:
            # del subkey in subkey
            with winreg.OpenKey(root_key, sub_key, access=winreg.KEY_ALL_ACCESS) as hkey:
                while True:
                    try:
                        subsubkey = winreg.EnumKey(hkey, 0)
                    except OSError:
                        # no more subkeys
                        break
                    EasyContextMenu.__delete_registry_tree(hkey, subsubkey)

            # del subkey
            winreg.DeleteKey(root_key, sub_key)
        except OSError:
            # subkey does not exist
            return

    @staticmethod
    def __query_registry(reg_path):
        try:
            subprocess.run(['reg', 'query', reg_path, "/s"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    @staticmethod
    def __export_registry(reg_path, output_file_path, force=False):
        command = ['reg', 'export', reg_path, output_file_path]
        if force:
            command.append("/y")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout