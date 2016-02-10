import numpy, scipy, librosa, IPython.display
import scipy.io.wavfile as wav

array = ['C4', 'C#4', 'D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4']
x, fs = librosa.load('test2.mp3',44100)
print('loading successful')

IPython.display.Audio(x,rate=fs)

def get_onset_times(x,fs):
    # onset frames
    onset_f = librosa.onset.onset_detect(x,fs)
    return librosa.frames_to_time(onset_f, fs)

def estimate_pitch(segment, fs, fmin=50.0, fmax= 5000.0):
    C = librosa.feature.chroma_stft(segment, fs)
    i = C.argmax(axis=0)
    #This returns what appears most in the list which we multiply
    counts = numpy.bincount(i) 
    mostused = numpy.argmax(counts) 
    note = array[mostused]
    midi = librosa.note_to_midi(note)
    return librosa.midi_to_hz(midi)
    
def generate_sine(f0, fs, n_duration):
    n = numpy.arange(n_duration)
    return 0.2*numpy.sin(2*numpy.pi*f0*n/float(fs))

def transcribe_pitch(signal_in, fs):
    signal_out = numpy.zeros(len(signal_in))
    onsets = get_onset_times(signal_in, fs)

    for i in range(len(onsets)-1):
        n0 = int(onsets[i]*fs)
        n1 = int(onsets[i+1]*fs)
        
        pitch = estimate_pitch(signal_in[n0:n1],fs,fmin=60,fmax=4000)
        print(pitch)
        signal_out[n0:n1] = generate_sine(pitch,fs,n1-n0)

    return signal_out

signal_out = transcribe_pitch(x,fs)
#IPython.display.Audio(signal_out,rate=fs)

wav.write('output.wav',fs, signal_out)
