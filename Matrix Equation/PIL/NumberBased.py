import numpy as np
import os
from PIL import Image, ImageDraw, ImageColor

class Equation:
    MATRIX = np.array([[.4, .2], [-.2, .4]])
    OFFSETS = np.array([[0, 0], [0, 1], [-1, 0], [1, 0], [0, -1]])
    K = 1000000
    rdn = np.random.default_rng()
    scale = 1024
    color = [(40, 83, 107, 255), (236, 125, 16, 255), (144, 227, 154, 255), (157, 209, 241, 255), (201, 140, 167, 255)]
    
    def __init__(self, base: np.array, matrix: np.array = None, \
        offsets: np.array = None, K: int = None, scale: int = None):
        if scale is None:
            scale = self.scale
        self.scale = np.uint32(np.power(2, np.floor(np.log2(scale*10))))
        if K is None:
            K = self.K
        self.K = K
        if f"{self.K}.npy" in os.listdir("PIL/Arrays"):
            self.coords: np.ndarray = np.load(f"PIL/Arrays/{self.K}.npy")
            self.K = 0
            return
        
        self.base = base
        if matrix is None:
            matrix = self.MATRIX
        if offsets is None:
            offsets = self.OFFSETS
        self.coords = np.ndarray((K, 5, 2), dtype=np.float64)
        self.count = 0
        self.matrix = matrix
        self.offsets = offsets
    
    def next(self):
        if self.K==0: return
        self.base = self.matrix.dot(self.base)
        Res = np.array([self.base, self.base, self.base, self.base, self.base]) + self.offsets
        self.coords[self.count] = Res
        self.count += 1
        self.base = self.rdn.choice(Res)
    
    def calculate(self):
        if self.K==0: return
        for i in range(self.K):
            self.next()
        print("End of loop")
    
    def drawPart(self, Idx: int, Total: int, Queue) -> Image:
        print("Drawing part", Idx)
        img = Image.new("RGBA", (10*self.scale, 10*self.scale), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        for Coords in self.coords[Idx//Total*self.coords.shape[0]:(Idx+1)//Total*self.coords.shape[0]]:
            for j in range(5):
                x, y = Coords[j]
                x = int(x * 2*self.scale + 5*self.scale)
                y = int(y * 2*self.scale + 5*self.scale)
                draw.point((x, y), fill=self.color[j])
        Queue.put(img)

    def draw(self, filename: str = None):
        img = Image.new("RGBA", (10*self.scale, 10*self.scale), (255, 255, 255, 255))
        
        
        print("Size in memory:", self.coords.nbytes/1024/1024/1024, "GB")
        
        import multiprocessing as mp
        print(f"Launching pool of {mp.cpu_count()} workers")
        Queue = mp.Manager().Queue()
        Coeur = mp.cpu_count()
        pool = mp.Pool(Coeur)
        for i in range(Coeur):
            pool.apply_async(self.drawPart, (i, Coeur, Queue))
        print("Waiting for pool to finish")
        pool.close()
        pool.join()
        
        print("Drawing final image")
        for _ in range(Coeur):
            img = Image.alpha_composite(img, Queue.get())
        
        
        if filename is not None:
            img.save(f'PIL/Images/{filename}')
        img.show()
        
    def save(self):
        if self.K==0: return
        np.save(f"PIL/Arrays/{self.K}", self.coords)
    
    def __str__(self):
        return f"Equation({self.base})"



if __name__ == "__main__":
    Eq = Equation(np.array([0, 0]), K=10_00_000, scale=1024)
    Eq.calculate()
    Eq.save()
    Eq.draw(f"{Eq.K} - {Eq.scale}.png")