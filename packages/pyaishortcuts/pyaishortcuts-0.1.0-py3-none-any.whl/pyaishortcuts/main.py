import json
from .ai_processor import AIProcessor
import pyperclip
import time
import FreeSimpleGUI as sg
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

class ShortcutHandler:
    def __init__(self, config):
        self.config = config
        self.ai_processor = AIProcessor(config)

    def show_notification(self, message):
        """显示通知消息"""
        sg.popup_auto_close(message,
                title="Notification",
                button_type=sg.POPUP_BUTTONS_OK,
                background_color="#f0f0f0",
                text_color="#000000",
                font=('Arial', 12),
                keep_on_top=True,
                location=(400, 400))  # 通知出现在屏幕顶部

    def process_selected_text(self, shortcut_name):
        selected_text = pyperclip.paste()
        if selected_text:
            result = self.ai_processor.process_text(selected_text, shortcut_name)
            if result:
                pyperclip.copy(result)
                self.show_notification("Text processed and copied to clipboard!")
            else:
                self.show_notification("Failed to process text.")
        else:
            self.show_notification("No text selected.")



    def create_popup(self):
        logger.debug("Key event pressed!")
        # 获取键盘事件的详细信息
        key_info = {
            'key': self.config['key_binding']['shortcut'],
            'event_type': 'keydown',
            'timestamp': time.time()
        }
        logger.info(f"Keyboard event details: {key_info}")
        
        shortcuts = self.config['shortcuts']
        options = [(name, shortcuts[name]['name']) for name in shortcuts]
        default_option = next((name for name in shortcuts if shortcuts[name].get('default', False)), options[0][0])
        
        # 创建弹出窗口布局
        layout = [
            [sg.Text("Select a prompt:", font=('Arial', 14))],
            [sg.Combo([option[1] for option in options], 
                     key="prompt", 
                     default_value=next(option[1] for option in options if option[0] == default_option),
                     font=('Arial', 12))],
            [sg.Button("OK", font=('Arial', 12))]
        ]
        
        # 设置窗口位置在顶部
        window = sg.Window("Prompt Selection",
                          layout,
                          location=(500, 500),  # 窗口出现在屏幕顶部
                          font=('Arial', 12),
                          finalize=True)
        
        # 自动选择默认选项并处理
        window['prompt'].update(window['prompt'].get())
        event, values = window.read(timeout=3000)  # 等待3秒
        
        # 获取当前选择的选项
        selected_name = next(option[0] for option in options if option[1] == values['prompt'])
        self.process_selected_text(selected_name)
        
        window.close()


    def run(self):
        import keyboard
        keyboard.add_hotkey(self.config['key_binding']['shortcut'], self.create_popup)
        while True:
            time.sleep(1)

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = json.load(open(config_path))
    handler = ShortcutHandler(config)
    handler.run()

if __name__ == "__main__":
    main()

