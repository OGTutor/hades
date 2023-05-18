import torch
import sounddevice as sd
import speech_recognition as sr
import time
from glob import glob

device = torch.device('cpu')
model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en',
                                       device=device)
(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils


def process_audio(_r, audio):
    try:
        print("Recognition...")

        # Save audio to file
        file_name = 'speech.wav'
        with open(file_name, 'wb') as f:
            f.write(audio.get_wav_data())

        # Process audio file
        test_files = glob(file_name)
        batches = split_into_batches(test_files, batch_size=10)
        input = prepare_model_input(read_batch(batches[0]),
                                    device=device)

        output = model(input)
        for example in output:
            print(decoder(example.cpu()))

    except sr.UnknownValueError:
        print("[log] Voice not recognized!")
    except Exception as e:
        print(f'[log] Error: {str(e)}')


# Start the recognition process
r = sr.Recognizer()
r.pause_threshold = 0.5
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

# Listen in the background and process audio
stop_listening = r.listen_in_background(m, process_audio)

# Keep the main thread running
while True:
    time.sleep(0.1)
