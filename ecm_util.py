import configparser
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

    def add_the_context_menu(self, menu_type):
        sub_key = self.__get_sub_key(menu_type)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, self.__menu_name)
            if self.__menu_icon_path:
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, self.__menu_icon_path)

        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key + '\\command') as key:
            menu_command = r"{}".format(self.__pragram_path)
            if self.__menu_info[menu_type]["param"]:
                menu_command += r" {}".format(self.__menu_info[menu_type]["param"])

            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_command)
            
        if self.__menu_info[menu_type]["is_extended"]:
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, sub_key) as key:
                winreg.SetValueEx(key, "Extended", 0, winreg.REG_SZ, "")

    def del_the_context_menu(self, menu_type):
        sub_key = self.__get_sub_key(menu_type)
        self.__delete_registry_tree(winreg.HKEY_CLASSES_ROOT, sub_key)

    @staticmethod
    def __delete_registry_tree(root, sub_key):
        try:
            hkey = winreg.OpenKey(root, sub_key, access=winreg.KEY_ALL_ACCESS)
        except OSError:
            # subkey does not exist
            return
        while True:
            try:
                subsubkey = winreg.EnumKey(hkey, 0)
            except OSError:
                # no more subkeys
                break
            EasyContextMenu.__delete_registry_tree(hkey, subsubkey)
        winreg.CloseKey(hkey)
        winreg.DeleteKey(root, sub_key)

    def __get_sub_key(self, menu_type):
        if menu_type == MenuType.ON_FILE:
            sub_key = "*\\shell\\" + self.__sub_key_name
        elif menu_type == MenuType.ON_DIR:
            sub_key = "Directory\\shell\\" + self.__sub_key_name
        elif menu_type == MenuType.ON_DIR_BG:
            sub_key = "Directory\\Background\\shell\\" + self.__sub_key_name
        else:
            sub_key = None
            
        return sub_key
    def __get_enable_menu(self):
        return [k for k, v in self.__menu_info.items() if v["enable"]]