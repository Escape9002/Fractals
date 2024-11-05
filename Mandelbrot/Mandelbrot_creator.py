from multiprocessing import Pool
import multiprocessing

import time
from PIL import Image
import colorsys
import math


px, py = -0.7746806106269039, -0.1374168856037867 #Tante Renate
max_iteration = 2500
w, h = 1024,1024
folder = "Mandelbrot_jpg\\"

def Mandelbrot(x,y,max_iteration,minx,maxx,miny,maxy, R):
    zx = 0
    zy = 0
    RX1, RX2, RY1, RY2 = px-R/2, px+R/2,py-R/2,py+R/2
    cx = (x-minx)/(maxx-minx)*(RX2-RX1)+RX1
    cy = (y-miny)/(maxy-miny)*(RY2-RY1)+RY1
    i=0
    while zx**2 + zy**2 <= 4 and i < max_iteration:
        temp = zx**2 - zy**2
        zy = 2*zx*zy + cy
        zx = temp + cx
        i += 1
    return i

def gen_Mandelbrot_image(sequence, mfactor, R):
  bitmap = Image.new("RGB", (w, h), "white")
  pix = bitmap.load()
  for x in range(w):
    for y in range(h):
      c=Mandelbrot(x,y,max_iteration,0,w-1,0,h-1, R)
      v = c**mfactor/max_iteration**mfactor
      hv = 0.67-v
      if hv<0: hv+=1
      r,g,b = colorsys.hsv_to_rgb(hv,1,1-(v-0.1)**2/0.9**2)
      r = min(255,round(r*255))
      g = min(255,round(g*255))
      b = min(255,round(b*255))
      pix[x,y] = int(r) + (int(g) << 8) + (int(b) << 16)
  bitmap.save(folder+"Mandelbrot_"+str(sequence)+".jpg")

def work_log(work_data):
    print(" sequence %s for %s mfactor with %s R" % (work_data[0], work_data[1], work_data[2]))
    start = time.time()
    gen_Mandelbrot_image(work_data[0], work_data[1], work_data[2])
    end = time.time()
    print(" Process %s Finished. Elapsed time: %s" % (work_data[0], (end-start)))


def pool_handler(work):
    p = Pool(multiprocessing.cpu_count()-8)
    p.map(work_log, work)


if __name__ == '__main__':
  work = list()
  R=3
  f = 0.975
  RZF = 1/1000000000000
  k=1
  while R>RZF:
    if k>1000: break
    mfactor = 0.5 + (1/1000000000000)**0.1/R**0.1
    work.append([k,mfactor, R])
    
    R *= f
    k+=1
  print(work)
  start_total = time.time()
  pool_handler(work)
  end_total = time.time()
  print("Process finished, elapsed time: %s" % (end_total-start_total))