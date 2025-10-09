import time
import subprocess
import os
import shutil
from pathlib import Path
import psutil
import pyautogui
import pygetwindow as gw

class TNavigatorAutomator:
    def __init__(self):
        self.tnavigator_path = r"c:\Users\79224\Desktop\TZ\tNavigator 4.0.2.exe"
        self.data_file = r"c:\Users\79224\Desktop\TZ\Example4.DATA"
        self.results_dir = r"c:\Users\79224\Desktop\TZ\results"
        os.makedirs(self.results_dir, exist_ok=True)

    def activate_tnavigator_window(self):
        try:
            time.sleep(2)
            windows = gw.getWindowsWithTitle('tNavigator')
            if windows:
                window = windows[0]
                if window.isMinimized:
                    window.restore()
                window.activate()
                time.sleep(1)
                return True
            return False
        except:
            return False

    def activate_calculate_button_hotkey(self):
        if not self.activate_tnavigator_window():
            return False
        
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(5)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        return self.check_calculation_started()

    def check_calculation_started(self):
        time.sleep(3)
        data_dir = os.path.dirname(self.data_file)
        temp_files = list(Path(data_dir).glob("*.tmp"))
        return len(temp_files) > 0

    def wait_for_tnavigator_close(self, timeout=1800):
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            tnav_running = any(
                proc.info['name'] and 'tNavigator' in proc.info['name']
                for proc in psutil.process_iter(['name'])
            )
            
            if not tnav_running:
                return True
            
            if self.check_large_result_files():
                return True
            
            time.sleep(10)
        
        return False

    def check_large_result_files(self):
        data_dir = os.path.dirname(self.data_file)
        data_name = os.path.splitext(os.path.basename(self.data_file))[0]
        
        for file_path in Path(data_dir).glob(f"{data_name}*"):
            if file_path.is_file() and file_path.stat().st_size > 10000:
                return True
        return False

    def run(self):
        subprocess.Popen([self.tnavigator_path, self.data_file])
        time.sleep(20)
        
        if self.activate_calculate_button_hotkey():
            self.wait_for_tnavigator_close()
        
        self.export_results()

    def export_results(self):
        data_dir = os.path.dirname(self.data_file)
        data_name = os.path.splitext(os.path.basename(self.data_file))[0]
        
        for file_path in Path(data_dir).glob(f"{data_name}*"):
            if file_path.is_file():
                try:
                    shutil.copy2(file_path, os.path.join(self.results_dir, file_path.name))
                except:
                    pass

if __name__ == "__main__":
    automator = TNavigatorAutomator()
    automator.run()