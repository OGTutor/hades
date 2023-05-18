import torch
import sounddevice as sd
import time

language = 'ru'
speaker_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'
put_accent = True
put_yo = True
device = torch.device('cpu')
text = "Wazzup dude!"

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=speaker_id)
model.to(device)


def va_speak(what: str):
    audio = model.apply_tts(text=what+"...",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    with sd.OutputStream(samplerate=sample_rate, channels=1) as stream:
        stream.write(audio)
        time.sleep((len(audio) / sample_rate) + 0.5)
