"""
Post-installation script for SpeedClick Pro
"""
import os
import sys
import site
import subprocess

def add_to_windows_path():
    """Add scripts directory to Windows PATH"""
    try:
        import winreg
        # Get script directory
        scripts_dir = os.path.join(site.USER_BASE, "Scripts")
        
        # Get current PATH
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           "Environment", 
                           0, 
                           winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            path, _ = winreg.QueryValueEx(key, "PATH")
        except WindowsError:
            path = ""
        
        # Add Scripts dir if it's not already in PATH
        if scripts_dir.lower() not in path.lower():
            if path:
                path = f"{path};{scripts_dir}"
            else:
                path = scripts_dir
            
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, path)
            winreg.CloseKey(key)
            print(f"Added {scripts_dir} to PATH")
            
            # Broadcast change notification
            try:
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x1A
                SMTO_ABORTIFHUNG = 0x0002
                result = ctypes.c_long()
                ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST, WM_SETTINGCHANGE, 0, 
                    "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
            except:
                pass
            
            return True
        else:
            print(f"{scripts_dir} already in PATH")
    except Exception as e:
        print(f"Error adding to PATH: {e}")
    return False

def main():
    """Main post-installation function"""
    if sys.platform.startswith('win'):
        add_to_windows_path()
        
if __name__ == "__main__":
    main()
