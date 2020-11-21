from queue import Queue
import threading, time, glob, pickle
from music21 import converter, instrument, note, chord, stream

global notes,q,threads,all_tasks

num_threads=10

notes = []
threads={}

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        worker(self.name)
        print ("Exiting " + self.name)
    
def parse(file):
    try:
        midi = converter.parse(file)
        notes_to_parse = None
        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    except Exception as e:
        print(e)
        


def worker(thread):
    while not q.empty():
        threads[thread]=True
        file=q.get()
        print("Parsing %s by %s | %d tasks finished"  % (file,thread,all_tasks-q.qsize()))
        parse(file)
    threads[thread]=False
        
            
 

q = Queue()

# Change with your MID file location
for file in glob.glob("~/midis/*.mid"):
    q.put(file)
  
all_tasks=q.qsize()

# Starting Threads    
for i in range(1,num_threads+1):
    myThread(i, "Thread-"+str(i), i).start()
    

# Checking if All tasks completed
while any(threads.values()):
    time.sleep(10)


# Change location to save final notes
with open('data/final_notes3', 'wb') as filepath:
    pickle.dump(notes, filepath)
    
print("All Completed!")
