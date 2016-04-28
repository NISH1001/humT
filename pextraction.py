import os
from math import sin,pi

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
    
    return pitches

def main():
    pass

if __name__ == "__main__":
    main()
