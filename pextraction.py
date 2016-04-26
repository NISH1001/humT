import os
from math import sin,pi

#Things used to make the wav file --start
#I proudly copied these things from the internet 
#and don't know shit about them

def littleEndian(n, bytes):
    li=[]
    for i in range(0, bytes):
        li.append(chr(n % 0x100))
        n = n // 0x100
    return ''.join(li)


def sineWave(freq, length, sampleRate=44100):
    C = 2 * pi * freq / sampleRate 
    return ''.join([chr(0x80+int(0x7F*sin(i*C))) for i in range(0,int(sampleRate*length//1000))])

#Things used to make wav file --end


#Load the Aubiopitch from command and save the data onto a file
os.system("aubiopitch -i test3.mp3 -r 44100 -l 0.8 > result.txt")

#Use the file to read the frequencies next
file = open("result.txt", "r")
frequen = file.read().split()
map(float, frequen)

#Pitch obtained in the form of [Time,Frequency]. Ignore time for now
frequency = []
for i in range(0, len(frequen),2):
    if float(frequen[i+1]) < 100: continue
    frequency.append(float(frequen[i+1]))


#Pitches is the list of pitches after averaging
pitches = []

#temp to hold the current clusture
temp = [frequency[0]]

#prev_pitch is the centre of the clusture
prev_pitch = 0

for pitch in frequency:
    #pitch is compared with the prev_pitch or centre and a minimum deviation of 15hz 
    #15hz is just trail stuff. Need to see if anything good comes with differed values
    if abs(pitch -prev_pitch) < 15:
        #add the pitch in the clusture
        temp += [pitch]
        #Update the prev_pitch/centre
        prev_pitch = sum(temp)/float(len(temp))
    else:
        #make sure temp(clusture) is not empty 
        if len(temp) > 0:
            #add the centre and lenth of clusture in the list
            pitches += [prev_pitch,len(temp)]
        #Update temp(new clusture) and prev_pitch accordingly
        temp = []
        prev_pitch = pitch


#wave is the value to write on the wav file
wave = ""

#take pitches only from the [pitches,lenth] tuple
for p in range(0,len(pitches),2):
    #if the length is not enough... probably a anamoly
    if pitches[p+1] < 10 : continue
    
    #print the pitches and their duration for viewing purpose
    print(pitches[p],pitches[p+1])
    #sineWave will make a sineWave with the given frequency of the given lenght
    wave = wave + sineWave(pitches[p],pitches[p+1]*10)

f = open("output.wav", 'wb')
length=len(wave)
f.write('RIFF%sWAVE'%littleEndian(length + 36, 4))
f.write('fmt \x10\x00\x00\x00\x01\x00\x01\x00%s%s\x01\x00\x08\x00'%(littleEndian(44100, 4),littleEndian(44100, 4)))
f.write('data%s'%littleEndian(length, 4))
f.write(wave)
f.close()

