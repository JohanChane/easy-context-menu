# Easy Context Menu

## 平台

-   Windows

## 目的/背景

我平时喜欢用免安装的软件, 但是软件有时不提供管理右键菜单的功能。如果用注册文件维护右键菜单是比较麻烦的, 因为有很多重复的字段, 所以修改起来并不方便, 所以开发了这个工具。

## 使用

安装 & 运行:

```sh
git clone https://github.com/JohanChane/easy-context-menu.git --depth 1
cd easy-context-menu
运行 EasyContextMenu.bat
```

相关文件:

-   confs: 用于放置软件右键菜单的配置

配置文件的格式:

For example: Vim.ini

```ini
[main]
program_path = D:\PortableProgramFiles\Vim\vim90\gvim.exe
menu_icon_path = D:\PortableProgramFiles\Vim\vim90\gvim.exe
; 菜单的名称
menu_name = Edit with Vim
; 注册表内部使用的名称 (不重复即可)
sub_key_name = EditWithVim

; 作用于文件的菜单
[menu_on_file]
; `%` 在 ini 配置文件是用于转义的字符, 所以 `%%` 表示是 `%`。
param = -p --remote-tab-silent "%%1"
; 表示是否需要按 shift + 右键弹出菜单
;is_extended = True

; 作用于目录的菜单
;[menu_on_dir]
;is_extended = True

; 作用于目录背景的菜单 (表示启用, param 为空。)
[menu_on_dir_bg]
;is_extended = True
```

Options:

-   add: 添加右键菜单
-   del: 删除右键菜单
-   query: 查询右键菜单的注册表
-   export: 导出右键菜单的注册表到 out 目录