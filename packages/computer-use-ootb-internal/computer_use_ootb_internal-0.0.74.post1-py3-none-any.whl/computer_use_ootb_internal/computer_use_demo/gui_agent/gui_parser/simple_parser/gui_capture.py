import json
import os
import re
import datetime
import time
import platform
import subprocess
from typing import List, Tuple, Dict
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors
import pyautogui  # This is already in dependencies


class Rectangle:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def intersects(self, other: 'Rectangle') -> bool:
        return not (self.right < other.left or
                   self.left > other.right or
                   self.bottom < other.top or
                   self.top > other.bottom)

    def get_intersection(self, other: 'Rectangle') -> 'Rectangle':
        left = max(self.left, other.left)
        top = max(self.top, other.top)
        right = min(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        if left < right and top < bottom:
            return Rectangle(left, top, right, bottom)
        return None

    def area(self) -> int:
        return (self.right - self.left) * (self.bottom - self.top)

    def is_within_monitor(self, monitor: 'Rectangle') -> bool:
        return self.intersects(monitor)


class VisibilityChecker:
    def __init__(self, selected_screen: int = 0, cache_folder='.cache/'):
        self.window_regions: List[Tuple[Rectangle, str]] = []
        self.monitor = self.get_monitor(selected_screen)
        self.cache_folder = cache_folder

    def get_monitor(self, selected_screen: int = 0):
        screens = get_monitors()

        # Sort screens by x position to arrange from left to right
        sorted_screens = sorted(screens, key=lambda s: s.x)

        if selected_screen >= len(sorted_screens):
            selected_screen = 0
            
        monitor = sorted_screens[selected_screen]

        return Rectangle(monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height)

    def add_window(self, rect: List[int], window_title: str = "") -> int:
        """Add window and record its region"""
        rect_obj = Rectangle(*rect)
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if rect_obj.is_within_monitor(self.monitor):
            self.window_regions.append((rect_obj, window_title))

            log_str = f"[add_window] Window {window_title} - {rect_obj.left}, {rect_obj.top}, {rect_obj.right}, {rect_obj.bottom} is within monitor"
            save_path = os.path.join(self.cache_folder, f'gui_capture_add_window_{current_time}.log')
            with open(save_path, 'a') as f:
                f.write(log_str + '\n')

    def is_visible(self, rect: List[int], threshold: float = 0.0) -> bool:
        """
        Check if element is visible
        Args:
            rect: Element rectangle [left, top, right, bottom]
            threshold: Visibility threshold, default 0.0
        """
        
        element_rect = Rectangle(*rect)
        
        # Check if within monitor
        if not element_rect.is_within_monitor(self.monitor):
            return False

        element_area = element_rect.area()
        if element_area == 0:
            return False

        # Calculate covered area
        covered_area = 0
        for window_rect, window_title in self.window_regions:            
            intersection = element_rect.get_intersection(window_rect)
            if intersection:
                covered_area += intersection.area()

        # Calculate visibility ratio
        visible_area = element_area - covered_area
        visibility_ratio = visible_area / element_area

        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_str = f"[is_visible] Element {rect}: visible with ratio {visibility_ratio}"
        save_path = os.path.join(self.cache_folder, f'is_visible_gui_capture_log_{current_time}.log')
        with open(save_path, 'a') as f:
            f.write(log_str + '\n')
        
        return visibility_ratio >= threshold


# Platform-specific implementations
if platform.system() == "Windows":
    import uiautomation as auto
    import win32gui
    import win32con
    import win32api
    import pygetwindow as gw
    from pywinauto import Desktop, Application
    from pywinauto.application import WindowSpecification
    from pywinauto.findwindows import find_windows
    
    def get_window_z_order():
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    
    def get_control_properties(control, properties_list):
        prop_dict = {}
        for prop in properties_list:
            if prop == 'texts':
                continue

            if hasattr(control, prop):
                attr = getattr(control, prop)
                if callable(attr):
                    try:
                        value = attr()
                        if prop == 'rectangle':
                            value = [value.left, value.top, value.right, value.bottom]

                        prop_dict[prop] = value
                    except Exception:
                        continue
                else:
                    prop_dict[prop] = attr

        # Get texts property
        if prop_dict.get('friendly_class_name') in ['ComboBox']:
            prop_dict['texts'] = ['']
        else:
            try:
                attr = getattr(control, 'texts')
                value = attr()
                prop_dict['texts'] = value
            except:
                prop_dict['texts'] = ['']

        # Get value property
        # This is for file explorer, the texts do not contain the file name, but in value property
        if prop_dict.get('texts') in [['名称'], ['修改日期'], ['大小'], ['类型'], ['Name'], ['Modified'], ['Size'], ['Type']]:
            try:
                pattern = control.element_info.element.GetCurrentPropertyValue(30045)  # UIA_ValueValuePropertyId
                    
                if pattern:
                    prop_dict['value'] = pattern
                    if len(prop_dict['texts']) == 1:
                        prop_dict['texts'] = [prop_dict['value']]
                else:
                    prop_dict['value'] = ''
            except Exception:
                prop_dict['value'] = ''

        return prop_dict

elif platform.system() == "Darwin":  # macOS
    # No need to import macOS-specific modules, as we'll just return empty metadata
    
    def get_window_z_order():
        return []
    
    def get_control_properties(control, properties_list):
        return {'texts': ['']}
else:
    # Linux or other platforms
    def get_window_z_order():
        # Simplified approach for other platforms
        return []
    
    def get_control_properties(control, properties_list):
        # Return an empty dict for unsupported platforms
        return {'texts': ['']}


class GUICapture:
    def __init__(self, cache_folder='.cache/', selected_screen: int = 0):
        self.task_id = self.get_current_time()
        self.cache_folder = os.path.join(cache_folder, self.task_id)
        os.makedirs(self.cache_folder, exist_ok=True)
        self.current_step = 0
        self.history = []
        self.visibility_checker = VisibilityChecker(selected_screen, self.cache_folder)
        self.system = platform.system()
        
    def get_current_time(self):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def is_element_visible(self, element) -> bool:
        try:
            if self.system == "Windows":
                if not element.is_visible():
                    return False

                try:
                    rect = element.rectangle()
                    if rect.left < -32000 or rect.top < -32000 or rect.right > 32000 or rect.bottom > 32000:
                        return False
                    if rect.right <= rect.left or rect.bottom <= rect.top:
                        return False
                    
                    rect_list = [rect.left, rect.top, rect.right, rect.bottom]
                    return self.visibility_checker.is_visible(rect_list)
                except Exception as e:
                    return False
            
            elif self.system == "Darwin":  # macOS
                # Always return False for macOS since we're skipping this functionality
                return False
            
            else:
                # For other platforms, simplified approach
                return True
                
        except Exception as e:
            return False

    def get_gui_meta_data(self):
        control_properties_list = ['friendly_class_name', 'texts', 'rectangle', 'automation_id', "value"]
        
        if self.system == "Windows":
            def get_window_controls(window_element):
                try:
                    control_data = []
                    try:
                        children = window_element.children()
                    except Exception:
                        return []
                    
                    for child in children:
                        try:                        
                            if not self.is_element_visible(child):
                                continue
                            
                            control_data.append({
                                'properties': get_control_properties(child, control_properties_list),
                                'children': get_window_controls(child)
                            })
                        except Exception:
                            continue
                            
                    return control_data
                except Exception:
                    return []
                
            meta_data = {}
            desktop = Desktop(backend='uia')
            windows = desktop.windows()
            handle_to_window = {win.handle: win for win in windows if win.is_visible()}
            
            # Process taskbar
            try:
                taskbar = desktop.window(class_name='Shell_TrayWnd')
                meta_data['Taskbar'] = get_window_controls(taskbar)
                rect = taskbar.rectangle()
                self.visibility_checker.add_window(
                    [rect.left, rect.top, rect.right, rect.bottom],
                    "Taskbar"
                )
            except Exception:
                meta_data['Taskbar'] = []

            # Get Z-order sorted window handles
            z_ordered_handles = get_window_z_order()
            
            # Process all windows
            for handle in z_ordered_handles:
                if handle in handle_to_window:
                    window = handle_to_window[handle]
                    try:
                        window_title = window.window_text()
                        if window_title and window_title != "Taskbar":
                            meta_data[window_title] = get_window_controls(window)
                            rect = window.rectangle()
                            self.visibility_checker.add_window(
                                [rect.left, rect.top, rect.right, rect.bottom],
                                window_title
                            )
                    except Exception:
                        continue
            
            return meta_data
        
        elif self.system == "Darwin":  # macOS
            # Return empty metadata for macOS
            return {}
        
        else:  # Linux or other platforms
            return {}
            
    def capture_screenshot(self, save_path=None):
        if save_path:
            screenshot_path = save_path
        else:
            screenshot_path = os.path.join(self.cache_folder, f'screenshot-{self.current_step}.png')

        if self.system == "Windows":
            # Use uiautomation for Windows
            screenshot = auto.GetRootControl().ToBitmap()
            screenshot.ToFile(screenshot_path)
        else:
            # Use pyautogui for macOS and other platforms
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
        return screenshot_path
    
    def clean_meta_data(self, meta_data):
        if isinstance(meta_data, dict):
            cleaned = {}
            for key, value in meta_data.items():
                # Skip any key that is an empty string
                if key == "":
                    continue

                # Recursively clean the value
                cleaned_value = self.clean_meta_data(value)

                # If the cleaned value is an empty string, skip adding this key
                if isinstance(cleaned_value, str) and cleaned_value == "":
                    continue

                # For the "texts" key, if it's a list that is empty or contains only empty strings, drop this key
                if key == "texts" and isinstance(cleaned_value, list):
                    if not cleaned_value or all(isinstance(item, str) and item.strip() == "" for item in cleaned_value):
                        continue

                if key == "children" and isinstance(cleaned_value, list):
                    if not cleaned_value or all(isinstance(item, str) and item.strip() == "" for item in cleaned_value):
                        continue

                cleaned[key] = cleaned_value

            return cleaned

        elif isinstance(meta_data, list):
            # Process each item in the list recursively
            return [self.clean_meta_data(item) for item in meta_data]

        return meta_data

    def capture(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        meta_data = self.get_gui_meta_data()

        with open(os.path.join(self.cache_folder, f'uia_metadata_{current_time}_raw.log'), 'w') as f:
            json.dump(meta_data, f, indent=4)

        screenshot_path = self.capture_screenshot()

        meta_data = self.clean_meta_data(meta_data)
        with open(os.path.join(self.cache_folder, f'uia_metadata_{current_time}_cleaned.log'), 'w') as f:
            json.dump(meta_data, f, indent=4)

        return meta_data, screenshot_path


def get_screenshot(selected_screen: int = 0):
    gui = GUICapture(selected_screen=selected_screen)
    meta_data, screenshot_path = gui.capture()
    return meta_data, screenshot_path

def get_uia_data(selected_screen: int = 0):
    gui = GUICapture(selected_screen=selected_screen)
    uia_data, _ = gui.capture()
    return uia_data

if __name__ == '__main__':
    # Use main display
    gui = GUICapture()
    meta_data, screenshot_path = gui.capture()
    print(meta_data)
