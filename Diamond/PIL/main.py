from multiprocessing import Process, Queue
import numpy as np
import time
from PIL import Image, ImageDraw
from random import choice

def NextCoord(queue: Queue, Points, M, DLR, URR, W, H, R):
    Diff = np.array([W, H]) / (URR - DLR)
    Possibility = [0, 1, 2, 3]
    Second = choice(Possibility[1:])
    Lasts = np.array([0, Second])
    coords = (Points[Lasts[0]] + Points[Lasts[1]])/2
    
    Same = [2, 3, 0, 1]
    
    for i in range(M//1000):
        for j in range(1000):
            current = ((coords - DLR) * Diff)
            current = [*(current-R), *(current+R)]
            queue.put(current)
            
            if Lasts[0] == Lasts[1]:
                Second = Same[Lasts[0]]
            else:
                Second = choice(Possibility)
            
            coords = (coords + Points[Second])/2
            
            if j%2:
                Lasts[1] = Second
            else:
                Lasts[0] = Second
        while queue.qsize() > 500:
            print(i/10)
  
    print(int(time.time()), ' - fin First')

    
    
if __name__ == "__main__":
    Gif = 0
    
    S = 2048*2
    Width, Height = [S] * 2
    
    im = Image.new('RGB', (Width, Height), (0,0,0))
    draw = ImageDraw.Draw(im)
    
    Nbr = 1_000_0
    DownLeftReal, UpRightReal = np.array([0, 0]), np.array([1, 1])
    Points = np.array([np.array([.5, .25]), np.array([.75, .5]), np.array([.5, .75]), np.array([.25, .5])])
        
    radius = S//1024 + 1
    radius = np.array([radius, radius])
    
    for i in Points:
        i = ((i - DownLeftReal) / (UpRightReal - DownLeftReal) * np.array([Width, Height]))
        draw.ellipse((*(i-radius), *(i+radius)), fill="white")
    
    test = np.array([0, 0])
    RealCoord = Queue()
    CalculateCoords = Process(target=NextCoord, args=(RealCoord, Points, Nbr, DownLeftReal, UpRightReal, Width, Height, radius))
    print(int(time.time()), ' - deb All')
    CalculateCoords.start()
    
    for i in range(Nbr):
        current = RealCoord.get()
        draw.ellipse(current, fill="blue")
        if not i%100 and Gif:
            im.save(f'Gif/{i//100}.png', 'PNG', quality=100)
    print(int(time.time()), ' - fin Creation')
    im.save(f'Images/{Nbr} - {Width}*{Height} - {time.time():.0f}.png', 'PNG', quality=100)
    
    CalculateCoords.kill()
    print(int(time.time()), ' - fin All')