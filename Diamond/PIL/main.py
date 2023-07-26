from multiprocessing import Process, Queue
import numpy as np
import time
from PIL import Image, ImageDraw
from random import choice
import pickle

def NextCoord(queue: Queue, Points, L, M, DLR, URR, W, H, R, Pickle=None):
    Diff = np.array([W, H]) / (URR - DLR)
    Possibility = list(range(L))
    Second = choice(Possibility[1:])
    Lasts = np.array([0, Second])
    coords = (Points[Lasts[0]] + Points[Lasts[1]])/2
    
    Same = np.ndarray((L, L-3))
    
    for i in range(L):
        I = list(range(L))
        I.remove(i); I.remove((i+1)%L); I.remove((i-1+L)%L)
        Same[i] = I
    
    # Same = [2, 3, 0, 1]
    
    for i in range(M//1000):
        for j in range(1000):
            current = ((coords - DLR) * Diff)
            current = [*(current-R), *(current+R)]
            #queue.put(current)
            Pickle.put(coords)
            
            if Lasts[0] == Lasts[1]:
                Second = int(np.random.choice(Same[Lasts[0]]))
            else:
                Second = choice(Possibility)
            
            coords = (coords + Points[Second])/2
            
            if j%2:
                Lasts[1] = Second
            else:
                Lasts[0] = Second
        while Pickle.qsize() > 500:
            print(i*100000/M)
            time.sleep(0.1)
  
    print(int(time.time()), ' - fin First')

    
    
if __name__ == "__main__":
    Gif = 0
    
    S = 2048
    Width, Height = [S] * 2
    
    im = Image.new('RGB', (Width, Height), (0,0,0))
    draw = ImageDraw.Draw(im)
    
    Nbr = int(2e7)
    DownLeftReal, UpRightReal = np.array([0, 0]), np.array([1, 1])
        
    radius = S//1024 - 1
    radius = 3.5
    radius = np.array([radius, radius])
    
    NbrPoints = 4
    Points = np.ndarray((NbrPoints, 2))
    Points[0] = np.array([0.5, 0.75])
    Origin = np.array([0.5, 0.5])
    Theta = -2*np.pi/NbrPoints
    Coeffs = np.matrix([[np.cos(Theta), -np.sin(Theta)], [np.sin(Theta), np.cos(Theta)]])
    
    for i in range(1, NbrPoints):
        Points[i] = np.dot(Coeffs, Points[i-1]-Origin)+Origin
    
    
    
    
    for i in Points:
        i = ((i - DownLeftReal) / (UpRightReal - DownLeftReal) * np.array([Width, Height]))
        draw.ellipse((*(i-radius), *(i+radius)), fill="white")
    
    test = np.array([0, 0])
    RealCoord = Queue()
    PickleQueue = Queue()
    CalculateCoords = Process(target=NextCoord, args=(RealCoord, Points, NbrPoints, Nbr, DownLeftReal, UpRightReal, Width, Height, radius, PickleQueue))
    print((U:=int(time.time())), ' - deb All')
    CalculateCoords.start()
    
    
    with open('Data.pickle', 'wb') as T:
        for i in range(Nbr):
            #current = RealCoord.get()
            #draw.ellipse(current, fill="blue")
            pickle.dump(PickleQueue.get(), T)
            if not i%100 and Gif:
                im.save(f'Gif/{i//100}.png', 'PNG', quality=100)
    print(int(time.time()), ' - fin Creation')
    im.save(f'Images/{f"{NbrPoints}/" if NbrPoints<=6 else f"6+/{NbrPoints}"}{Nbr} - {Width}*{Height} - {time.time():.0f}.png', 'PNG', quality=100)
    im.close()
    CalculateCoords.kill()
    print(int(time.time()), ' - fin All')
    