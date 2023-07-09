from queue import Queue
import speech_recognition as sr
import pygetwindow as gw
import pyautogui
import threading
import argparse
import logging
import time

logging.getLogger().setLevel(logging.INFO)

class VoiceRecognizer(threading.Thread):
    WORDS = ['print', 'scan', 'scam', 'skin', 'plane', 'green', 'flynn', 'step', 'stem', 'yeah', 'ten', 'stan']

    def __init__(self, recognizer, queue, window_offset, window_title):
        threading.Thread.__init__(self, daemon=True)
        self.recognizer = recognizer
        self.queue = queue
        self.window_offset = window_offset
        self.window_title = window_title
        self.next_print = 0

    def recognize_command(self, recognizer, audio):
        try:
            logging.info('Recognizing...')
            command = recognizer.recognize_vosk(audio,  language='en-US').lower()
            logging.info(f'Command: {command}')
            return command
        except sr.UnknownValueError:
            logging.info("Could not understand audio")
        except sr.RequestError as e:
            logging.info(f"Error: {e}")

    def click_button(self):
        try:
            windows = gw.getWindowsWithTitle(self.window_title)

            if not windows:
                return False

            window = windows[0]
            window.activate()

            x, y = self.window_offset
            button_position = window.left + x, window.top + y
            
            for _ in range(3):
                pyautogui.click(button_position)
                time.sleep(0.2)
        except gw.PyGetWindowException as e:
            # Ignore correct Windows errors
            if '0' in str(e):
                return

            raise e

    def is_scan_command(self, command):
        if not command:
            return False
    
        for word in self.WORDS:
            if word in command:
                return True
        
        return False

    def work(self, audio):
        command = self.recognize_command(self.recognizer, audio)

        if not self.is_scan_command(command):
            return

        logging.info("Scanning...")

        if self.next_print > time.time():
            logging.info('Skipping due to next print')
            return

        self.next_print = time.time() + 6.0
        self.click_button()

    def run(self):
        while True:
            added_time, item = self.queue.get()

            if time.time() - added_time > 5.0:
                logging.info('Skipping old audio...')
            else:
                self.work(item)

            self.queue.task_done()

def main(window_offset, window_title):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    queue = Queue()

    voice_recognizer = VoiceRecognizer(recognizer, queue, window_offset, window_title)
    voice_recognizer.start()

    with microphone as source:
        logging.info('Adjusting for ambient noise...')
        recognizer.adjust_for_ambient_noise(source)

        while True:
            logging.info('Listening for command...')
            audio = recognizer.listen(source, phrase_time_limit=2)
            queue.put((time.time(), audio))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Voice Recognition Script')
    parser.add_argument('--x', type=int, help='X offset for button click', default=40)
    parser.add_argument('--y', type=int, help='Y offset for button click', default=70)
    parser.add_argument('--window-title', type=str, help='Window title of scanner', default='Not Another PDF Scanner 2')
    args = parser.parse_args()

    main(window_offset=(args.x, args.y), window_title=args.window_title)
