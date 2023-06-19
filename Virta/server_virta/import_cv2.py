import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import math
import argparse
import imutils
from scipy.spatial import distance as dist

interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
interpreter.allocate_tensors()

img = cv2.imread('Hp_nesy\Denis.jpg')
image= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
width = image.shape[1]
height = image.shape[0]

imagedt=image.copy()
imagedt=tf.image.resize_with_pad(np.expand_dims(image, axis=0),192,192)
plt.imshow(image)

#resizeimage
img = image.copy()
img =tf.image.resize_with_pad(np.expand_dims(image, axis=0), 192,192)

input_image = tf.cast(img, dtype=tf.float32)

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'],np.array(input_image))
interpreter.invoke()

keypoint = interpreter.get_tensor(output_details[0]['index'])
shaped = np.squeeze(np.multiply(interpreter.get_tensor(interpreter.get_output_details()[0]['index']),[height,width,1])).astype(int)
shaped[0], shaped[1]

EDGES = {
        (0, 1): 'm',
        (0, 2): 'c',
        (1, 3): 'm',
        (2, 4): 'c',
        (0, 5): 'm',
        (0, 6): 'c',
        (5, 7): 'm',
        (7, 9): 'm',
        (6, 8): 'c',
        (8, 10): 'c',
        (5, 6): 'y',
        (5, 11): 'm',
        (6, 12): 'c',
        (11, 12): 'y',
        (11, 13): 'm',
        (13, 15): 'm',
        (12, 14): 'c',
        (14, 16): 'c'
    }
#drawkeypoint 
for kp in shaped:
            ky, kx, kp_conf = kp
            cv2.circle(image, (int(kx), int(ky)), 20, (0,255,0), -1)
            continue

    #drawline
for edge, color in EDGES.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            image = cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)),(0,255,0), 10)
            continue

    #hitungskala #daritriangle
    #menghitung skala gambar tinggi
skalaheight=(((height*200)/267)/200)

    #menghitung skala gambar lebar
skalawidht=(((width*200)/140)/200)

    #perhitungan Euclidean Distance
    #hitung Lebar bahu 1
bahu1=math.pow(shaped[5][1]-shaped[6][1],2)
bahu2=math.pow(shaped[5][0]-shaped[6][0],2)
Panjang_Bahu=math.sqrt(bahu1 + bahu2)
ld= int((Panjang_Bahu/skalawidht)+32)

print(Panjang_Bahu)
print("lebar bahu",(int(ld)),"cm")

#hitung panjang tangan 2
tangan1=math.pow(shaped[10][1]-shaped[6][1],2)
tangan2=math.pow(shaped[10][0]-shaped[6][0],2)
Panjang_Tangan=math.sqrt(tangan1 + tangan2)
pt= int((Panjang_Tangan/skalaheight) + 14)

print(Panjang_Tangan)
print("Panjang Tangan",(int(pt)),"cm")

  #huitung panjang kemeja 3
kemeja1=math.pow(shaped[12][1]-shaped[6][[1]],2)
kemeja2=math.pow(shaped[12][0]-shaped[6][0],2)
panjang_kemeja=math.sqrt(kemeja1+kemeja2)
pk= int((panjang_kemeja/skalaheight)+8)

print(panjang_kemeja)
print("Panjang baju",(int(pk)),"cm")

  #huitung panjang celana 
celana1=math.pow(shaped[16][1]-shaped[12][[1]],2) 
celana2=math.pow(shaped[16][0]-shaped[12][0],2)
panjang_celana=math.sqrt(celana1+celana2)
pc= int((panjang_celana/skalaheight)+26)

print(panjang_celana)
print("Panjang celana",(int(pc)),"cm")

  #hitung lingkar dada 5
d1=math.pow(shaped[5][1]-shaped[6][1],2) #bahu1
d2=math.pow(shaped[5][0]-shaped[6][0],2)#bahu2
pd=math.sqrt(d1 + d2)#lebar dada
pd2 = pd/2
a=math.pow(pd,2)
b=math.pow(pd2,2)
elips = 2*math.pi*math.sqrt((a+b)/2)
lingd= int((elips/skalawidht)+6)

print(elips)
print("Lingkar Dada",(int(lingd)),"cm")

  #hitung lingkar pinggang 6
pinggang1=math.pow(shaped[11][1]-shaped[12][1],2) #hip1
pinggang2=math.pow(shaped[11][0]-shaped[12][0],2)#hip2
lpinggang=math.sqrt(pinggang1 + pinggang2) #lebar pinggang
lpinggang2 = lpinggang/2
a1=math.pow(lpinggang,2)
b1=math.pow(lpinggang2,2)
elips1 = 2*math.pi*math.sqrt((a1+b1)/2)
lingkarpinggang= int((elips1/skalawidht)+35)

print(elips1)
print("Lingkar pinggang",(int(lingkarpinggang)),"cm")

  #hitung lingkar pinggul 7
pinggul1=math.pow(shaped[11][1]-shaped[12][1],2) #hip1
pinggul2=math.pow(shaped[11][0]-shaped[12][0],2)#hip2
lpinggul=math.sqrt(pinggul1 + pinggul2) #lebar panggul
lpinggul2 = lpinggul/2
a2=math.pow(lpinggul,2)
b2=math.pow(lpinggul2,2)
elips2 = 2*math.pi*math.sqrt((a2+b2)/2)
lingkarpinggul= int((elips2/skalawidht)+49)

print(elips2)
print("Lingkar pinggul",(int(lingkarpinggul)),"cm")

  #hitung lingkar paha 8
paha1=math.pow(shaped[5][1]-shaped[6][1],2) #kaki1
paha2=math.pow(shaped[5][0]-shaped[6][0],2)#kaki2
lebarkaki=math.sqrt(paha1 + paha2)#lebar 1 celana
lebarkaki2 = lebarkaki/2
lingkaran = math.pi*lebarkaki2
lebarpaha= int((lingkaran/skalawidht)+32)

print(lingkaran)
print("Lingkar paha",(int(lebarpaha)),"cm")

if ld <= 46 and pk <= 67.5 and pt <= 60 :
    ukuran = "S"
    #print("UKURAN KEMEJA S")
elif ld <= 38 and pk<= 70 and pt <= 61.5:
    ukuran = "M"
    #print("UKURAN KEMEJA M")
elif ld <= 48 and pk<= 72.5 and pt <= 63 :
    ukuran = "L"
    #print("UKURAN KEMEJA L")
else: 
      ukuran = "XL"
      #print("UKURAN KEMEJA XL")
          
Hasil_Pengukuran=[ ld,pt,pk,pc,ukuran]

if lingkarpinggang <= 72 and pc<=90  :
      ukuran = "S"
      #print("UKURAN CELANA S")
elif lingkarpinggang <= 76 and pc<=90  :
      ukuran = "M"
      #print("UKURAN CELANA M")
elif lingkarpinggang <= 80 and pc<=92 :
      ukuran = "L"
      #print("UKURAN CELANA L")
else:
      ukuran = "XL"
          #print("UKURAN CELANA XL")
          
Hasil_Pengukuran2=[ lingkarpinggang,pc,ukuran]

print (Hasil_Pengukuran)
print (Hasil_Pengukuran2)


#cewek
#hitung Lebar bahu 
bahu1=math.pow(shaped[5][1]-shaped[6][1],2)
bahu2=math.pow(shaped[5][0]-shaped[6][0],2)
Panjang_Bahu=math.sqrt(bahu1 + bahu2)
lb= int((Panjang_Bahu/skalawidht)+26)

print(Panjang_Bahu)
print("lebar bahu",(int(lb)),"cm")

#hitung panjang tangan 
tangan1=math.pow(shaped[10][1]-shaped[6][1],2)
tangan2=math.pow(shaped[10][0]-shaped[6][0],2)
Panjang_Tangan=math.sqrt(tangan1 + tangan2)
pt= int((Panjang_Tangan/skalaheight) + 8)

print(Panjang_Tangan)
print("Panjang Tangan",(int(pt)),"cm")

#hitung panjang jas 
jas1=math.pow(shaped[12][1]-shaped[6][[1]],2)
jas2=math.pow(shaped[12][0]-shaped[6][0],2)
panjang_jas=math.sqrt(jas1+jas2)
pj= int((panjang_jas/skalaheight)+4)

print(panjang_jas)
print("Panjang jas",(int(pj)),"cm")

#huitung panjang rok 
rok1=math.pow(shaped[16][1]-shaped[12][[1]],2) 
rok2=math.pow(shaped[16][0]-shaped[12][0],2)
panjang_rok=math.sqrt(rok1+rok2)
pr= int((panjang_rok/skalaheight)+19)

print(panjang_rok)
print("Panjang rok",(int(pr)),"cm")

#hitung lingkar dada 
d1=math.pow(shaped[5][1]-shaped[6][1],2) #bahu1
d2=math.pow(shaped[5][0]-shaped[6][0],2)#bahu2
pd=math.sqrt(d1 + d2)#lebar dada
pd2 = pd/2
a=math.pow(pd,2)
b=math.pow(pd2,2)
elips = 2*math.pi*math.sqrt((a+b)/2)
lingd= int((elips/skalawidht)+30)

print(elips)
print("Lingkar Dada",(int(lingd)),"cm")

#hitung lingkar pinggang 
pinggang1=math.pow(shaped[11][1]-shaped[12][1],2) #hip1
pinggang2=math.pow(shaped[11][0]-shaped[12][0],2)#hip2
lpinggang=math.sqrt(pinggang1 + pinggang2) #lebar pinggang
lpinggang2 = lpinggang/2
a1=math.pow(lpinggang,2)
b1=math.pow(lpinggang2,2)
elips1 = 2*math.pi*math.sqrt((a1+b1)/2)
lingkarpinggang= int((elips1/skalawidht)+28)

print(elips1)
print("Lingkar pinggang",(int(lingkarpinggang)),"cm")

#hitung lingkar pinggul 
pinggul1=math.pow(shaped[11][1]-shaped[12][1],2) #hip1
pinggul2=math.pow(shaped[11][0]-shaped[12][0],2)#hip2
lpinggul=math.sqrt(pinggul1 + pinggul2) #lebar panggul
lpinggul2 = lpinggul/2
a2=math.pow(lpinggul,2)
b2=math.pow(lpinggul2,2)
elips2 = 2*math.pi*math.sqrt((a2+b2)/2)
lingkarpinggul= int((elips2/skalawidht)+45)

print(elips2)
print("Lingkar pinggul",(int(lingkarpinggul)),"cm")


if lb <= 38 and pj <= 63 and pt <= 51 :
  ukuran = "S"
  #print("UKURAN JAS S")
elif lb <= 39 and pj<= 63 and pt <= 51:
  ukuran = "M"
  #print("UKURAN JAS M")
elif lb <= 40 and pj<= 63 and pt <= 52 :
   ukuran = "L"
   #print("UKURAN JAS L")
else: 
    ukuran = "XL"
    #print("UKURAN JAS XL")
        
Hasil_Pengukuran=[ lb,pt,pj,ukuran]

if lingkarpinggang <= 72 and pc<=90  :
    ukuran = "S"
    #print("UKURAN ROK S")
elif lingkarpinggang <= 76 and pc<=90  :
    ukuran = "M"
    #print("UKURAN ROK M")
elif lingkarpinggang <= 80 and pc<=92 :
    ukuran = "L"
    #print("UKURAN ROK L")
else:
    ukuran = "XL"
        #print("UKURAN ROK XL")
        
Hasil_Pengukuran2=[ lingkarpinggang,pr,ukuran]

print (Hasil_Pengukuran)
print (Hasil_Pengukuran2)

