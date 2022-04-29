from PIL import Image, ImageOps, ImageDraw
from bresenham import bresenham
from skimage.color import rgb2gray
from skimage.draw import line
import numpy as np
import matplotlib.pyplot as plt
import sys

#GET INPUT CONSTANTS HERE

args = sys.argv
BOARD_WIDTH = int(args[1])          #CM
PIXEL_WIDTH = float(args[2])        #ex: 1 - suggest keeping this constant and changing board width only
LINE_TRANSPARENCY = float(args[3])  #value between 0 to 1
NUM_NAILS = int(args[4])            #ex: 300
MAX_ITERATIONS = int(args[5])       #ex: 4000

# identifys if the process should be beautified or not
BEAUTIFY = False

if len(args) > 6:
    BEAUTIFY = args[6].lower() == 'true'

    
NAILS_SKIP = 10
OUTPUT_TITLE = "output"
RESULT_TITLE = "result"

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
ref = cropToCircle("image.jpg")

base = Image.new('L', size, color=255)

#Calculating pixels and setting up nail perimeter
angles = np.linspace(0, 2*np.pi, NUM_NAILS)  # angles to the dots
cx, cy = (BOARD_WIDTH/2/PIXEL_WIDTH, BOARD_WIDTH/2/PIXEL_WIDTH)  # center of circle
xs = cx + BOARD_WIDTH*0.5*np.cos(angles)/PIXEL_WIDTH
ys = cy + BOARD_WIDTH*0.5*np.sin(angles)/PIXEL_WIDTH
nails = list(map(lambda x,y: (int(x),int(y)), xs,ys))
res = ""

# showing input values if BEAUTIFY is true
if BEAUTIFY:
    res += "Board Width: " + str(BOARD_WIDTH) + "\n"
    res += "Pixel Width: " + str(PIXEL_WIDTH) + "\n"
    res += "Line Transparency: " + str(LINE_TRANSPARENCY) + "\n"
    res += "Number of Nails: " + str(NUM_NAILS) + "\n"
    res += "Maximum Iterations: " + str(MAX_ITERATIONS) + "\n"

#Uncomment to show nails plot
#plt.scatter(xs, ys, c = 'red', s=2)
#plt.show()

cur_nail = 1        #start at arbitrary nail
ref_arr = np.transpose(np.array(ref)[:, :, 0])
base_arr = base.load()

for i in range(MAX_ITERATIONS):
    best_line = None
    new_nail = None
    min_avg_value = 10000
    for n in range(cur_nail+1+NAILS_SKIP,cur_nail+len(nails)-NAILS_SKIP):
        n = n%NUM_NAILS
        tmp_value = 0
        new_line = line(nails[cur_nail][0], nails[cur_nail][1], nails[n][0], nails[n][1])
        num_pts = len(new_line[0])

        tmp_value = np.sum(ref_arr[new_line])

        if tmp_value/num_pts < min_avg_value:
            best_line = new_line
            new_nail = n
            #print(new_nail,tmp_value/num_pts)
            min_avg_value = tmp_value/num_pts

    #Uncomment for progress pictures every x=200 iterations
    #if i%200 == 0:
    #    title = OUTPUT_TITLE+str(BOARD_WIDTH)+'W-'+str(PIXEL_WIDTH)+"P-"+str(NUM_NAILS)+'N-'+str(i)+'-'+str(LINE_TRANSPARENCY)+'.png'
    #    print(title)
    #    base.save(title)
    #    res += "\n --- "+str(i)+" --- \n"

    ref_arr[best_line] = 255
    addLine = ImageDraw.Draw(base)
    addLine.line((nails[cur_nail][0],nails[cur_nail][1],nails[new_nail][0],nails[new_nail][1]), fill=0)

    # differing every 100 step if BEAUTIFY is true
    if BEAUTIFY:
        if i % 100 == 0:
            res += "\n" + "\n" + "-----   " + str(i) + "   -----" + "\n" + "\n"

    res += " " + str(new_nail)
    print("Iteration ",i, " Complete: ","(",cur_nail,",",new_nail,")")
    cur_nail = new_nail

# title if BEAUTIFY is true
if BEAUTIFY:
    title = '--' + str(BOARD_WIDTH) + 'bw-' + str(PIXEL_WIDTH) + "pw-" + str(
        LINE_TRANSPARENCY) + 'lt-' + str(NUM_NAILS) + 'n-' + str(MAX_ITERATIONS) + 'i'
else:
    title = str(BOARD_WIDTH)+'W-'+str(PIXEL_WIDTH)+"P-"+str(
        NUM_NAILS)+'N-'+str(MAX_ITERATIONS)+'-'+str(LINE_TRANSPARENCY)


results = open(RESULT_TITLE + title + ".txt", "w")
results.write(res)
results.close()
base.save(OUTPUT_TITLE + title + '.png')
