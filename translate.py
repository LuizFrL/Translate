import os, playsound, clipboard, time, win10toast as win
from typing import TypeVar, Dict
from googletrans import Translator
from googletrans.models import Detected, Translated
from gtts import gTTS
from system_hotkey import SystemHotkey


def play_sound(text: str, lang: str = 'en') -> None:
    tts: gTTS = gTTS(text=text, lang=lang)
    sound_name: str = 'speak_sound.mp3'
    if os.path.isfile(sound_name):
        os.remove(sound_name)
    tts.save(sound_name)
    playsound.playsound(sound_name)
    os.remove(sound_name)


def pt_actions(text: str) -> None:
    trans: Translator = Translator()
    translated_object: Translated = trans.translate(text, 'en')
    play_sound(translated_object.text)
    clipboard.copy(translated_object.text)


def en_actions(text: str) -> None:
    trans: Translator = Translator()
    translated_object: Translated = trans.translate(text, dest='pt')
    play_sound(translated_object.text, 'pt')
    play_sound(text)


def get_error_message(error: str) -> str:
    errors: Dict[str, str] = {
        '[Errno 11001] getaddrinfo failed': 'Problem was detected, could not connect to API.',
    }

    return errors.get(error) if errors.get(error) else error


def notify(message: str) -> None:
    notifier: win.ToastNotifier = win.ToastNotifier()
    icon_path: str = 'icone.ico'
    if message:
        notifier.show_toast('Translate', message, icon_path=icon_path, duration=10)
    else:
        notifier.show_toast('Translate', f'We unable identify the error, please contact the developer.',
                            duration=10, icon_path=icon_path)


def main(a):
    try:
        TEXT: str = clipboard.paste()
        trans: Translator = Translator()
        souce_text: Detected = trans.detect(TEXT)
        if actions.get(souce_text.lang):
            actions.get(souce_text.lang)(TEXT)
    except Exception as error:
        notify(get_error_message(str(error)))


T = TypeVar('T')
actions: Dict[str, T] = {
    'pt': pt_actions,
    'en': en_actions
}


hotkeys: tuple = ('alt', 'shift', 'q')
hk = SystemHotkey()
hk.register(hotkeys, callback=main)


while True:
    time.sleep(1000000)
