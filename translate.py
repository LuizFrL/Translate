import os, playsound, clipboard, pyautogui
import time
from typing import TypeVar, Dict
from googletrans import Translator
from googletrans.models import Detected, Translated
from gtts import gTTS
from system_hotkey import SystemHotkey



def play_sound(text: str, lang: str = 'en') -> None:
    tts: gTTS = gTTS(text=text, lang=lang)
    sound_name: str = 'speak_sound.mp3'
    tts.save(sound_name)
    playsound.playsound(sound_name)
    os.remove(sound_name)


def pt_actions(text: str) -> None:
    trans: Translator = Translator()
    translated_object: Translated = trans.translate(text)
    play_sound(translated_object.text)
    clipboard.copy(translated_object.text)


def en_actions(text: str) -> None:
    trans: Translator = Translator()
    translated_object: Translated = trans.translate(text, dest='pt')
    play_sound(translated_object.text, 'pt')
    play_sound(text)


T = TypeVar('T')
actions: Dict[str, T] = {
    'pt': pt_actions,
    'en': en_actions
}


# TEXT: str = ' '.join(string for string in sys.argv[1:]).strip()

def main(a):
    pyautogui.hotkey('ctrl', 'c')
    TEXT: str = clipboard.paste()

    trans: Translator = Translator()
    souce_text: Detected = trans.detect(TEXT)

    if actions.get(souce_text.lang):
        actions.get(souce_text.lang)(TEXT)



hk = SystemHotkey()
hk.register(('alt', 'shift', 't'), callback=main)

while True:
    time.sleep(1000000)
