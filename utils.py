from music21 import converter, instrument, note, chord,midi,stream
import numpy as np
from collections import Counter
import operator
import os

#transform in a 2D array in 3D of shape (n,TIMESTEPS,2)
#last shape=2 because each point is a note + time
def get_x(input,TIMESTEPS):
    x = np.zeros((input.shape[0] - TIMESTEPS, TIMESTEPS, input.shape[1]))
    y = np.array([])
    for i in range(0, len(input) - TIMESTEPS):
        x[i] = input[i:i + TIMESTEPS]
    return x

def gabriel():
    print "lala"

#read a midi_file and transform it in an array (n,2)
#where 2 is because each point is a note + time
def create_dataset(midi_file_name):
    data = converter.parse(midi_file_name)
    a=instrument.partitionByInstrument(data)
    a=a.flat.notesAndRests
    note_list=[]
    offset_list=[]
    prev=0
    for i in a:
        if isinstance(i, note.Note):
            note_list.append([str(i.pitch)])
            offset_list.append(i.offset-prev)
            prev=i.offset
        elif isinstance(i, chord.Chord):
            for pitch in i:
                note_list.append([str(pitch.pitch)])
                offset_list.append(i.offset-prev)
                prev=i.offset
    return note_list,offset_list

# transform a 2D array of notes (ex:A,B,D) in a numbers sequence
#unique is a dictionnary which link each note to a number
#you can print it below if you want
def create_dataset_number(dataset):
    unique=list(set(list(dataset[:,0])))
    unique=sorted(unique)
    for i in range(len(unique)):
        unique[i]=[unique[i],i]
    unique=dict(unique)
    
    for i in range(dataset.shape[0]):
        dataset[i,0]=unique[dataset[i,0]]
    dataset=dataset.astype('float64')
    return dataset,unique

#predict music
def generate_music(model,x):
    notes=model.predict(x)
    return notes
        
# transform an array of number to a midi file
# save a midi file named test_output.mid
def array_to_midi(x,dic,name='test_output'):
    notes=[]
    offset=0
    for i in range(len(x)):
        try:
            new_note = note.Note(dic.keys()[dic.values().index(int(x[i][0]))])
            new_note.storedInstrument = instrument.AltoSaxophone()
            print x[i]
            offset+=x[i][1]
            new_note.offset=(offset)
            notes.append(new_note)
        except:
            print('oui')
    midi_stream = stream.Stream(notes)
    midi_stream.write('midi', fp=name+'.mid')

# fct to add several midi files to the dataset    
def concat_dataset(list_midi):
    notes=[]
    offset=[]
    for i in list_midi:
        n,o=create_dataset(i)
        notes=notes+n
        offset=offset+o
    return np.array(notes),np.array(offset)