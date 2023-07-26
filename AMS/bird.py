from multiprocessing import Process, Queue
import numpy as np
import time
from PIL import Image, ImageDraw

def F(k):
    X = np.sin(np.pi*k/20000)**12 * (.5*np.cos(31*np.pi*k/10000)**16 * np.sin(6*np.pi*k/10000) + 1/6*np.sin(31*np.pi*k/10000)**20) + 3*k/20000 + np.cos(31*np.pi*k/10000)**6 * np.sin(np.pi/2*((k-10000)/10000)**7-np.pi/5)
    
    Y = -9/4*np.cos(31*np.pi*k/10000)**6 * np.cos(np.pi/2*(((k-10000)/10000)**7)-np.pi/5)*((2/3)+(np.sin(np.pi*k/20000)*np.sin(3*np.pi*k/20000))**6) + 3/4*np.cos(3*np.pi*(k-10000)/10000)**10*np.cos(9*np.pi*(k-10000)/10000)**10*np.cos(36*np.pi*(k-10000)/10000)**14+.7*((k-10000)/10000)**2
    
    R = np.sin(np.pi*k/20000)**10*.25*np.cos(31*np.pi/10000+25*np.pi/32)**20+.05*np.cos(31*np.pi*k/10000)**2+1/30*(3/2-np.cos(62*np.pi*k/10000)**2)
    
    return np.array([X, Y]), R
 
def NextCoord(queue: Queue, equation, M, DLR, URR, W, H, R=1):
    Diff = np.array([W, H]) / (URR - DLR)
    k = np.double(0)
    Step = np.double(M/9830)
    while k<=9830:
        Coords, Rad = equation(k)
        Rad /= 2
        Coords = [Coords-Rad, Coords+Rad]
        current = ((Coords - DLR) * Diff)
        
        queue.put(current)
        k += Step
    print(int(time.time()), ' - fin First')

    

if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    # from matplotlib import cm, use, colors
    # use('Qt5Agg')
    # fig, ax = plt.subplots()
    # Xs, Ys, Rs = np.ndarray(9830), np.ndarray(9830), np.ndarray(9830)
    # for i in range(9830):
    #     K = np.ushort(i+1)
    #     [Xs[i], Ys[i]], Rs[i] = F(K)
    
    # Points = list(range(9830))
    
    # ax.plot(Points, Xs, label="Xs")
    # ax.plot(Points, Ys, label="Ys")
    # ax.plot(Points, Rs, label="Rs")
    
    # plt.show()
    # print(5/0)
    Gif = 0
    
    S = 2048
    Width, Height = [S] * 2
    
    im = Image.new('RGB', (Width, Height), (0,0,0))
    draw = ImageDraw.Draw(im)
    
    Nbr = 2 * 10 ** 5
    Nbr = 9830
    DownLeftReal, UpRightReal = np.array([-1, -3]), np.array([1.8, 2.5])
        
    
    test = np.array([0, 0])
    RealCoord = Queue()
    CalculateCoords = Process(target=NextCoord, args=(RealCoord, F, Nbr, DownLeftReal, UpRightReal, Width, Height))
    print((U:=int(time.time())), ' - deb All')
    CalculateCoords.start()
    
    for i in range(Nbr):
        current = RealCoord.get()
        draw.ellipse((current[0][0], current[0][1], current[1][0], current[1][1]), fill="blue")
    print(int(time.time()), ' - fin Creation')
    im.save(f'Images/{Nbr} - {Width}*{Height} - {time.time():.0f}.png', 'PNG', quality=100)
    im.close()
    CalculateCoords.kill()
    print(int(time.time()), ' - fin All')