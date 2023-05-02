from multiprocessing import Process, Queue
import numpy as np
import time


def fx(x, y):
    return np.double(-.8 - .1*x+ 1.1*x*x -1.2*x*y + .3*y + 1.1*y*y)

def fy(x, y):
    return np.double(.3*x+ .4*x*x + .2*x*y - 1.1*y + .7*y*y)


class Equation:
    def __init__(self, equations: list[str]=None) -> None:
        self.Equation = lambda x: np.array([fx(*x), fy(*x)])
    
    def next(self, Coords):
        return self.Equation(Coords)

def NextCoord(queue: Queue, coords: np.array, equation: Equation):
    while True:
        queue.put(coords)
        coords = equation.next(coords)


def Converter(Real: Queue, Screen: Queue, DLR, URR, W, H, R, P):
    Diff = np.array([W, H]) / (URR - DLR)
    
    if P:
        while True:
            current = Real.get()
            current = ((current - DLR) * Diff).astype("ushort")
            current = [*(current-R), *(current+R)]
            Screen.put(current)
    else:
        while True:
            current = Real.get()
            current = ((current - DLR) * Diff).astype("ushort")
            Screen.put(current)
    
    
if __name__ == "__main__":
    Pil = True
    
    S = 2048*2
    Width, Height = [S] * 2
    
    Nbr = 10000
    
    DownLeftReal, UpRightReal = np.array([-1, 2]), np.array([2, -1])
    
    radius = 6
    radius = np.array([radius, radius])
    
    test = np.array([0, 0])
    Eq = Equation()
    RealCoord = Queue()
    ScreenCoord = Queue()
    CalculateCoords = Process(target=NextCoord, args=(RealCoord, test, Eq,))
    ConvertCoords = Process(target=Converter, args=(RealCoord, ScreenCoord, DownLeftReal, UpRightReal, Width, Height, radius, Pil))
    CalculateCoords.start()
    ConvertCoords.start()
    
    if Pil:
        from PIL import Image, ImageDraw
        
        im = Image.new('RGB', (Width, Height), (0,0,0))
        draw = ImageDraw.Draw(im)
        
        for i in range(Nbr):
            current = ScreenCoord.get()
            draw.ellipse(current, fill="blue")
        
        im.save(f'Polynomial Equation/PIL/{Nbr} - {time.time():.0f}.png', 'PNG', quality=100)
    else:
        import pygame
        pygame.init()
        
        screen = pygame.display.set_mode((Width, Height), pygame.NOFRAME)
        
        t = 0
        while True:
            for events in pygame.event.get():
                pass

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.image.save(screen, f"Polynomial Equation/Pygame/{time.time():.0f}.png")
                break
            
            current = ScreenCoord.get()
            pygame.draw.circle(screen, (255, 255, 255), current, 2)
            t += 1
            if t%100 == 0:
                pygame.display.flip()
            
        pygame.quit()

CalculateCoords.kill()
ConvertCoords.kill()