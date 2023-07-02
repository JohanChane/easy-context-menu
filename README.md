# Easy Context Menu

Language: [English](./README.md) | [中文](./README_CN.md)

## Platform

-   Windows

## Purpose/Background

I often like to use portable software that doesn't require installation. However, some software doesn't provide a built-in feature to manage the right-click context menu. It can be inconvenient to manually edit the registry files (.reg) to modify the context menu, especially when there are many repetitive fields. Therefore, I developed this tool to make it easier to manage the context menu.

## Usage

Installation & Execution:

```sh
git clone https://github.com/JohanChane/easy-context-menu.git --depth 1
cd easy-context-menu
Run EasyContextMenu.bat
```

Related Files:

-   confs: Contains the configurations for the software right-click context menu

Format of the configuration file:

For example: Vim.ini

```ini
[main]
program_path = D:\PortableProgramFiles\Vim\vim90\gvim.exe
menu_icon_path = D:\PortableProgramFiles\Vim\vim90\gvim.exe
; The name of the menu
menu_name = Edit with Vim
; The internal name used in the registry (should be unique)
sub_key_name = EditWithVim

; Menu for files
[menu_on_file]
; `%` is an escape character in ini configuration files, so `%%` represents `%`.
param = -p --remote-tab-silent "%%1"
; Indicates whether the menu should be shown when Shift + right-click is used
;is_extended = True

; Menu for directories
;[menu_on_dir]
;is_extended = True

; Menu for directory background (enabled by leaving param empty)
[menu_on_dir_bg]
;is_extended = True
```

Options:

-   add: Add the context menu
-   del: Remove the context menu