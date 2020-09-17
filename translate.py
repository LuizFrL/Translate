import os, playsound, sys, clipboard
from googletrans import Translator
from googletrans.models import Detected, Translated
from gtts import gTTS


def play_sound(text: str, lang: str = 'en') -> None:
    tts: gTTS = gTTS(text=text, lang=lang)
    sound_name: str = 'speak_sound.mp3'
    tts.save(sound_name)
    playsound.playsound(sound_name)
    os.remove(sound_name)

def pt_actions(text: str) -> None:
    translated_object: Translated = trans.translate(text)
    play_sound(translated_object.text)
    clipboard.copy(translated_object.text)


def en_actions(text: str) -> None:
    translated_object: Translated = trans.translate(text, dest='pt')
    play_sound(translated_object.text, 'pt')
    play_sound(text)


actions = {
    'pt': pt_actions,
    'en': en_actions
}


TEXT: str = ' '.join(string for string in sys.argv[1:]).strip()

trans: Translator = Translator()
souce_text: Detected = trans.detect(TEXT)

if actions.get(souce_text.lang):
    actions.get(souce_text.lang)(TEXT)
