import numpy as np
import os
from PIL import Image, ImageDraw, ImageColor

color = [(40, 83, 107, 255), (236, 125, 16, 255), (144, 227, 154, 255), (157, 209, 241, 255), (201, 140, 167, 255)]

def drawPart(Idx: int, Total: int, Dict, Coords:np.array) -> Image:
    print("Drawing part", Idx)
    img = Image.new("RGBA", (Coords.shape[0], Coords.shape[0]), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    for x in np.arange(Coords.shape[0]):
        for y in np.arange(Coords.shape[0]):
            if Coords[x, y] != 0:
                draw.point((x, y), fill=color[Coords[x, y]-1])
    Dict[Idx] = img
    # img.show()



class Equation:
    MATRIX = np.array([[.4, .2], [-.2, .4]])
    OFFSETS = np.array([[0, 0], [0, 1], [-1, 0], [1, 0], [0, -1]])
    K = 1000000
    rdn = np.random.default_rng()
    scale = 1024
    
    def __init__(self, base: np.array, matrix: np.array = None, \
        offsets: np.array = None, K: int = None, scale: int = None):
        if scale is None:
            scale = self.scale
        self.scale = np.uint64(np.power(2, np.ceil(np.log2(scale))))
        if K is None:
            K = self.K
        self.K = K
        if f"{self.K}-{self.scale}.npy" in os.listdir("PIL/Arrays"):
            print("Found array in memory")
            self.coords: np.ndarray = np.load(f"PIL/Arrays/{self.K}-{self.scale}.npy")
            self.K = 0
            return
        
        self.base = base
        if matrix is None:
            matrix = self.MATRIX
        if offsets is None:
            offsets = self.OFFSETS
        self.coords = np.zeros((self.scale, self.scale), dtype=np.uint8)
        print("Size in memory:", self.coords.nbytes/1024/1024/1024, "GB")
        self.count = 0
        self.matrix = matrix
        self.offsets = offsets
    
    def next(self):
        if self.K==0: return
        self.base = self.matrix.dot(self.base)
        Res = np.array([self.base, self.base, self.base, self.base, self.base]) + self.offsets
        for Enum, (x, y) in enumerate(Res):
            x = int(x * self.scale/5 + self.scale/2)
            y = int(y * self.scale/5 + self.scale/2)
            self.coords[x, y] = Enum+1
        self.count += 1
        self.base = self.rdn.choice(Res)
    
    def calculate(self):
        if self.K==0: return
        for i in range(self.K):
            self.next()
        print("End of loop")
    
    def draw(self, filename: str = None):
        img = Image.new("RGBA", (self.scale, self.scale), (255, 255, 255, 255))
        print("Size in memory:", self.coords.nbytes/1024/1024/1024, "GB")
        
        import multiprocessing as mp
        print(f"Launching pool of {mp.cpu_count()} workers")
        Dict = mp.Manager().dict()
        Coeur = mp.cpu_count()
        Precalc = np.uint64(self.coords.shape[0]//np.sqrt(Coeur))
        Precalc2 = np.uint16(np.sqrt(Coeur))
        pool = mp.Pool(Coeur)
        for i in range(Coeur):
            StartX, StartY = Deb = np.array(np.divmod(i, Precalc2)) * Precalc
            EndX, EndY = Deb + Precalc
            pool.apply_async(drawPart, (i, Coeur, Dict, self.coords[StartX:EndX, StartY:EndY], ))
        print("Waiting for pool to finish")
        pool.close()
        pool.join()
        
        print("Drawing final image")
        for i in range(Coeur):
            StartX, StartY = np.array(np.divmod(i, Precalc2)) * Precalc
            img.paste(Dict[i], (StartX, StartY), Dict[i])
        
        
        if filename is not None:
            img.save(f'PIL/Images/{filename}')
        img.show()
        
    def save(self):
        if self.K==0: return
        np.save(f"PIL/Arrays/{self.K}-{self.scale}", self.coords)
    
    def __str__(self):
        return f"Equation({self.base})"



if __name__ == "__main__":
    Eq = Equation(np.array([0, 0]), K=100_000_000, scale=10000)
    Eq.calculate()
    Eq.save()
    Eq.draw(f"{Eq.K} - {Eq.scale}.png")