import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import webbrowser
import random


def main():
    print(f"{config.VA_NAME} (v{config.VA_VER}) started work ...")
    stt.va_listen(va_respond)


def va_respond(voice: str) -> None:
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("What?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str) -> str:
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str) -> dict:
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str) -> None:
    if cmd == 'help':
        handle_help()
    elif cmd == 'ctime':
        handle_current_time()
    elif cmd == 'joke':
        handle_joke()
    elif cmd == 'open_browser':
        handle_open_browser()


def handle_help() -> None:
    text = "Я умею: ...\n"
    text += "произносить время ...\n"
    text += "рассказывать анекдоты ...\n"
    text += "и открывать браузер"
    tts.va_speak(text)


def handle_current_time() -> None:
    now = datetime.datetime.now()
    text = f'Сейч+ас {num2words(now.hour, lang="ru")} "..." {num2words(now.minute, lang="ru")}'
    tts.va_speak(text)


def handle_joke() -> None:
    jokes = ['Как смеются программисты? ... ехе ехе ехе',
             'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
             'Программист это машина для преобразования кофе в код']
    tts.va_speak(random.choice(jokes))


def handle_open_browser() -> None:
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open("http://python.org")


if __name__ == '__main__':
    main()
