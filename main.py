from PIL import Image, ImageOps, ImageDraw
from bresenham import bresenham
from skimage.color import rgb2gray
from skimage.draw import line
import numpy as np
import matplotlib.pyplot as plt
import sys

#DEFINE CONSTANTS HERE

args = sys.argv
#BOARD_WIDTH = 100 #CM
#PIXEL_WIDTH = 0.05
#LINE_TRANSPARENCY = 0.5
#NUM_NAILS = 300
#MAX_ITERATIONS = 1000
BOARD_WIDTH = int(args[1]) #CM
PIXEL_WIDTH = float(args[2])
LINE_TRANSPARENCY = float(args[3])
NUM_NAILS = int(args[4])
MAX_ITERATIONS = int(args[5])
NAILS_SKIP = 10

pixels = int(BOARD_WIDTH/PIXEL_WIDTH)
size = (pixels+1, pixels+1)

def cropToCircle(path):
    img = Image.open(path).convert("L")
    img = img.resize(size);
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)

    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

#Cropping image to a circle
ref = cropToCircle("image2.jpg")

base = cropToCircle("base.png")

#Calculating pixels and setting up nail perimeter
angles = np.linspace(0, 2*np.pi, NUM_NAILS)  # angles to the dots
cx, cy = (BOARD_WIDTH/2/PIXEL_WIDTH, BOARD_WIDTH/2/PIXEL_WIDTH)  # center of circle
xs = cx + BOARD_WIDTH*0.5*np.cos(angles)/PIXEL_WIDTH
ys = cy + BOARD_WIDTH*0.5*np.sin(angles)/PIXEL_WIDTH
nails = list(map(lambda x,y: (int(x),int(y)), xs,ys))

#plt.scatter(xs, ys, c = 'red', s=2)  # plot points
#plt.show()

cur_nail = 80
ref_arr = ref.load()
base_arr = base.load()

for i in range(MAX_ITERATIONS):
    best_line = None
    new_nail = None
    min_avg_value = 10000
    for n in range(cur_nail+1+NAILS_SKIP,cur_nail+len(nails)-2*NAILS_SKIP):
        n = n%NUM_NAILS
        tmp_value = 0
        new_line = line(nails[cur_nail][0], nails[cur_nail][1], nails[n][0], nails[n][1])
        num_pts = len(new_line[0])
        #plt.scatter(new_line[0],new_line[1], c = 'blue', s=0.2)  # plot points

        for j in range(num_pts):
            tmp_value += ref_arr[int(new_line[0][j]), int(new_line[1][j])][0]
        #print(n, tmp_value/num_pts)

        if tmp_value/num_pts < min_avg_value:
            best_line = new_line
            new_nail = n
            #print(new_nail,tmp_value/num_pts)
            min_avg_value = tmp_value/num_pts

    #We've found the most optimal line: add it to output and subtract from photo
    if new_nail == cur_nail:
        title = str(BOARD_WIDTH)+'W-'+str(PIXEL_WIDTH)+"P-"+str(NUM_NAILS)+'N-'+str(MAX_ITERATIONS)+'-'+str(LINE_TRANSPARENCY)+'.png'
        print(title)
        base.save(title)
        ref.save(title+'orig.png')

    for k in range(len(best_line[0])):
        new_darkness = int(min(255, (1+LINE_TRANSPARENCY)*ref_arr[int(best_line[0][k]), int(best_line[1][k])][0]))
        new_lightness = int(max(0, base_arr[int(best_line[0][k]), int(best_line[1][k])][0]-(1-LINE_TRANSPARENCY)*255))
        ref_arr[int(best_line[0][k]), int(best_line[1][k])] = (new_darkness,0)
        base_arr[int(best_line[0][k]), int(best_line[1][k])] = (new_lightness,0)
    #print(ref_arr[nails[new_nail][0],nails[new_nail][1]])
    print("Iteration ",i, " Complete: ","(",cur_nail,",",new_nail,")")
    cur_nail = new_nail

title = str(BOARD_WIDTH)+'W-'+str(PIXEL_WIDTH)+"P-"+str(NUM_NAILS)+'N-'+str(MAX_ITERATIONS)+'-'+str(LINE_TRANSPARENCY)+'.png'
print(title)
base.save(title)
ref.save(title+"orig.png")
