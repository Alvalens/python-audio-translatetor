from deep_translator import GoogleTranslator
import assemblyai as aai
import pyaudio
import wave
import os
import time
from dotenv import load_dotenv

load_dotenv()

# assemblyai API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
transcriber = aai.Transcriber()

if not aai.settings.api_key:
    raise Exception("Please set your API key as an environment variable.")

# Inisialisasi PyAudio
p = pyaudio.PyAudio()

def record_audio(duration=5):  # Record for 5 seconds by default
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    print("Mulai merekam...")
    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    print("Selesai merekam")
    return frames


# tampilkan list kode bahasa
langs_dict = dict(GoogleTranslator().get_supported_languages(as_dict=True))
print("Kode bahasa yang tersedia: ")
for key, value in langs_dict.items():
    print(key, ': ', value)

# pilih bahasa yang akan diterjemahkan
lang = input("Masukkan kode bahasa tujuan diterjemahkan: ")
while lang not in langs_dict.values():
    print("Kode bahasa tidak ditemukan")
    lang = input("Masukkan kode bahasa tujuan diterjemahkan: ")
    if lang in langs_dict.values():
        break
    elif lang.lower() == 'x':
        exit()

# mulai merekam audio
conf = input("Ketik 'y' untuk mulai merekam: ")
frames = []
if conf.lower() == 'y':
    frames = record_audio()

# Menyimpan audio yang direkam sebagai file WAV
wf = wave.open("output.wav", "wb")
wf.setnchannels(2)  # Ubah jumlah saluran menjadi 2
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b"".join(frames))
wf.close()

# Melakukan transkripsi audio yang direkam
transcript = transcriber.transcribe("output.wav")
print(transcript.text)
text = transcript.text
if text == "" or text == None:
    text = "Tidak ada teks yang dikenali"
    
# Melakukan terjemahan teks yang diterjemahkan
translated_text = GoogleTranslator(
    source='auto', target=lang).translate(text)
print(translated_text)

# hapus file WAV
os.remove("output.wav")
