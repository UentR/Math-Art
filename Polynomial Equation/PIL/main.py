from multiprocessing import Process, Queue
import numpy as np
import time
from PIL import Image, ImageDraw

def fx(x, y):
    return np.double(-.8 - .1*x+ 1.1*x*x -1.2*x*y + .3*y + 1.1*y*y)

def fy(x, y):
    return np.double(.3*x+ .4*x*x + .2*x*y - 1.1*y + .7*y*y)


class Equation:
    def __init__(self, equations: list[str]=None) -> None:
        self.Equation = lambda x: np.array([fx(*x), fy(*x)])
    
    def next(self, Coords):
        return self.Equation(Coords)

def NextCoord(queue: Queue, coords: np.array, equation: Equation, M, DLR, URR, W, H, R):
    Diff = np.array([W, H]) / (URR - DLR)
    
    for i in range(M):
        current = ((coords - DLR) * Diff)
        current = [*(current-R), *(current+R)]
        queue.put(current)
        coords = equation.next(coords)
    print(int(time.time()), ' - fin First')


def Converter(Real: Queue, Screen: Queue, DLR, URR, W, H, R, M):
    Diff = np.array([W, H]) / (URR - DLR)
    
    for i in range(M):
        current = Real.get()                    # too slow
        current = ((current - DLR) * Diff)      #.astype("ushort")
        current = [*(current-R), *(current+R)]
        Screen.put(current)
    print(int(time.time()), ' - fin Second')
    
    
if __name__ == "__main__":
    Gif = 0
    
    S = 2048*4
    Width, Height = [S] * 2
    
    im = Image.new('RGB', (Width, Height), (0,0,0))
    draw = ImageDraw.Draw(im)
    
    Nbr = 30000
    DownLeftReal, UpRightReal = np.array([-1, 2]), np.array([1.5, -1])
    
    radius = S//1024 + 1
    radius = np.array([radius, radius])
    
    test = np.array([0, 0])
    Eq = Equation()
    RealCoord = Queue()
    # ScreenCoord = Queue()
    CalculateCoords = Process(target=NextCoord, args=(RealCoord, test, Eq, Nbr, DownLeftReal, UpRightReal, Width, Height, radius))
    # ConvertCoords = Process(target=Converter, args=(RealCoord, ScreenCoord, DownLeftReal, UpRightReal, Width, Height, radius, Nbr))
    print(int(time.time()), ' - deb All')
    CalculateCoords.start()
    # ConvertCoords.start()
    
    for i in range(Nbr):
        current = RealCoord.get()
        draw.ellipse(current, fill="blue")
        if not i%100 and Gif:
            im.save(f'Gif/{i//100}.png', 'PNG', quality=100)
    print(int(time.time()), ' - fin Creation')
    im.save(f'Images/{Nbr} - {Width}*{Height} - {time.time():.0f}.png', 'PNG', quality=100)
    
    CalculateCoords.kill()
    # ConvertCoords.kill()
    print(int(time.time()), ' - fin All')