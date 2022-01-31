from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx

def def_browser_check(reg_path):
    reg_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'

    with OpenKey(HKEY_CURRENT_USER, reg_path) as key:
        if "Chrome" in QueryValueEx(key, 'ProgId')[0]:
            print("Yes")

