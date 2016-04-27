#!/usr/bin/env python3

import pyaudio
import wave

class Recorder:
    def __init__(self, fmt=pyaudio.paInt16,
            channels=2, rate=44100, chunk=1024,
            ):
        self.audio = pyaudio.PyAudio()
        self.fmt = fmt
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
    
    def start(self, time=5):
        print("record : start")
        stream = self.audio.open(format=self.fmt,
                    channels = self.channels,
                    rate = self.rate,
                    input = True,
                    frames_per_buffer = self.chunk
                    )
        frames = []
        for i in range(0, int(self.rate / self.chunk * time)):
            data = stream.read(self.chunk)
            frames.append(data)
        print("record : stopped")
        stream.stop_stream()
        stream.close()
        return frames

    def write_wav(self, frames, filename="shit.wav"):
        wavefile = wave.open(filename, 'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.fmt))
        wavefile.setframerate(self.rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

def main():
    recorder = Recorder()
    frames = recorder.start(5)
    recorder.write_wav(frames, "shit.wav")

if __name__ == "__main__":
    main()

