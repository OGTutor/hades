import vosk
import sounddevice as sd
import queue
import json

model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        raise RuntimeError(f'Audio callback error: {status}')
    q.put(bytes(indata))


def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback) as stream:

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                callback(text)
