from PIL import Image
import glob
 
frames = []
imgs = glob.glob("Images/*.png")
for i in imgs[::10]:
    new_frame = Image.open(i)
    frames.append(new_frame)

print('go')

frames[0].save('Animation.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300, loop=0)