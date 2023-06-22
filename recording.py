import os
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from datetime import datetime
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.microphone_sound = []
    
    def record_audio(self):
        def callback(indata, frames, time, status):
            if status:
                print("Recording error:", status)
            self.microphone_sound.append(indata.copy())

        with sd.InputStream(samplerate=self.sample_rate, channels=2, callback=callback):
            print("Recording started. Press Enter to stop recording...")
            input()
            print("Recording stopped.")

    def save_audio(self, output_filename):
        if not self.microphone_sound:
            print("No audio recorded.")
            return

        microphone_sound = np.concatenate(self.microphone_sound)
        recordings_dir = "recordings"
        os.makedirs(recordings_dir, exist_ok=True)

        microphone_sound_filename = os.path.join(recordings_dir, output_filename + "_microphone_sound.wav")
        sf.write(
            microphone_sound_filename,
            microphone_sound,
            samplerate=self.sample_rate,
            subtype='PCM_24'
        )

        microphone_sound_audio = AudioSegment.from_file(microphone_sound_filename)
        output_path = os.path.join(recordings_dir, output_filename + ".wav")
        
        current_datetime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        current_datetime = str(current_datetime)
        microphone_sound_audio.export(f'{output_path}_{current_datetime}' + ".wav", format="wav")

        # Delete temporary audio files
        os.remove(microphone_sound_filename)


if __name__ == "__main__":
    output_filename = "meeting_recording"

    recorder = AudioRecorder()
    recorder.record_audio()
    recorder.save_audio(output_filename)
