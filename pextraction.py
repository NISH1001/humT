import os
from math import sin,pi

notePitches =   [   61.74,65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.83,110.00,116.54,123.47,130.81,
                    138.59,146.83,155.56,164.81,174.61,185.00,196.00,207.65,220.00,233.08,246.94,
                    261.63,277.18,293.66,311.13,329.63,349.23 ,369.99,392.00,415.30,440.00,466.16,493.88,
                    523.25,554.37,587.33,622.25, 659.25,698.46,739.99 ,783.99,830.61,880.00
                ]
    
def track_pitch(inputFilename): 
    #Load the Aubiopitch from command and save the data onto a file
    os.system("aubiopitch -i" + inputFilename+ " -r 44100 -l 0.8 > temp.txt")
    
    #Use the file to read the frequencies next
    file = open("temp.txt", "r")
    frequen = file.read().split()
    map(float, frequen)
    
    #delete the temp file beacuse it is not needed anymore
    os.system("rm temp.txt")
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
            #make sure temp(clusture) is big enough to be a valid clusture(size = 10) 
            if len(temp) > 10:
                #add the centre and lenth of clusture in the list
                pitches += [prev_pitch,len(temp)]
            #Update temp(new clusture) and prev_pitch accordingly
            temp = []
            prev_pitch = pitch
    
    #to use pitch slope method for comparision, to-do 
    #pitchSlope = []
    currPitch = []
    for p in range(0,len(pitches)-2,2):
        #converting the pitches value to the index of the notePitches
        #This is like mapping the frequencies to the musical notes
        currPitch += [min(range(len(notePitches)),key = lambda i: abs(notePitches[i]- pitches[p])), pitches[p+1]]
        
        #pitchSlope += [abs(currPitch - nextPitch)/pitchLen]
    print(currPitch)
    return currPitch

def main():
    pass

if __name__ == "__main__":
    main()
