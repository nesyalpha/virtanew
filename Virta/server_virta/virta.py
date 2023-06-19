import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import math
import matplotlib.pyplot as plt
import sys
import json, os
from flask import Flask, request, jsonify
import uuid

letak = "C:/xampp/htdocs/gambar"
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# run_with_ngrok(app)


@app.route("/test", methods=["GET", "POST"])
def detect():
    # Check if an image file is present in the request
    if "image_post" not in request.files:
        return jsonify(
            bahu="0",
            tangan="0",
            badan="0",
            panjang_kaki="0",
            lingkar_dada="0",
            lingkaran_pinggang="0",
            lingkar_pinggul="0",
            lingkar_paha="0",
            ukuran_kemeja="0",
            ukuran_celana="0",
            gambar="0",
            message="Gak Berhasil",
            status="NOK",
        )

    image_file = request.files["image_post"]
    interpreter = tf.lite.Interpreter(
        model_path="lite-model_movenet_singlepose_lightning_3.tflite"
    )
    interpreter.allocate_tensors()

    # Read the image file using OpenCV
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # membacagambar
    imagedt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    width = imagedt.shape[1]
    height = imagedt.shape[0]
    # resizeimage
    img = imagedt.copy()
    img = tf.image.resize_with_pad(np.expand_dims(imagedt, axis=0), 192, 192)

    # converttofloat
    input_image = tf.cast(img, dtype=tf.float32)

    # detailinputoutput
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # penggabungan gambar dengan image data
    interpreter.set_tensor(input_details[0]["index"], np.array(input_image))
    interpreter.invoke()
    # keypoint
    keypointsdetection = interpreter.get_tensor(output_details[0]["index"])
    shaped = np.squeeze(
        np.multiply(
            interpreter.get_tensor(interpreter.get_output_details()[0]["index"]),
            [height, width, 1],
        )
    ).astype(int)
    shaped[0], shaped[1]

    EDGES = {
        (0, 1): "m",
        (0, 2): "c",
        (1, 3): "m",
        (2, 4): "c",
        (0, 5): "m",
        (0, 6): "c",
        (5, 7): "m",
        (7, 9): "m",
        (6, 8): "c",
        (8, 10): "c",
        (5, 6): "y",
        (5, 11): "m",
        (6, 12): "c",
        (11, 12): "y",
        (11, 13): "m",
        (13, 15): "m",
        (12, 14): "c",
        (14, 16): "c",
    }

    # drawkeypoint
    for kp in shaped:
        ky, kx, kp_conf = kp
        image = cv2.circle(imagedt, (int(kx), int(ky)), 20, (0, 255, 0), -1)
        continue
    # drawline
    for edge, color in EDGES.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        image = cv2.line(
            imagedt, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10
        )
        continue

    # hitungskala
    # menghitung skala gambar tinggi
    skalaheight = ((height * 200) / 250) / 200

    # menghitung skala gambar lebar
    skalawidht = ((width * 200) / 140) / 200

    # perhitungan Euclidean Distance
    # hitung bahu
    bahu1 = math.pow(shaped[5][1] - shaped[6][1], 2)
    bahu2 = math.pow(shaped[5][0] - shaped[6][0], 2)
    Panjang_Bahu = math.sqrt(bahu1 + bahu2)
    ld = int((Panjang_Bahu / skalawidht) + 32)

    print(Panjang_Bahu)
    print("lebar bahu", (int(ld)), "cm")

    # hitung panjang tangan 2
    tangan1 = math.pow(shaped[10][1] - shaped[6][1], 2)
    tangan2 = math.pow(shaped[10][0] - shaped[6][0], 2)
    Panjang_Tangan = math.sqrt(tangan1 + tangan2)
    pt = int((Panjang_Tangan / skalaheight) + 14)

    print(Panjang_Tangan)
    print("Panjang Tangan", (int(pt)), "cm")

    # huitung panjang kemeja 3
    kemeja1 = math.pow(shaped[12][1] - shaped[6][[1]], 2)
    kemeja2 = math.pow(shaped[12][0] - shaped[6][0], 2)
    panjang_kemeja = math.sqrt(kemeja1 + kemeja2)
    pk = int((panjang_kemeja / skalaheight) + 8)

    print(panjang_kemeja)
    print("Panjang baju", (int(pk)), "cm")

    # huitung panjang celana
    celana1 = math.pow(shaped[16][1] - shaped[12][[1]], 2)
    celana2 = math.pow(shaped[16][0] - shaped[12][0], 2)
    panjang_celana = math.sqrt(celana1 + celana2)
    pc = int((panjang_celana / skalaheight) + 26)

    print(panjang_celana)
    print("Panjang celana", (int(pc)), "cm")

    # hitung lingkar dada 5
    d1 = math.pow(shaped[5][1] - shaped[6][1], 2)  # bahu1
    d2 = math.pow(shaped[5][0] - shaped[6][0], 2)  # bahu2
    pd = math.sqrt(d1 + d2)  # lebar dada
    pd2 = pd / 2
    a = math.pow(pd, 2)
    b = math.pow(pd2, 2)
    elips = 2 * math.pi * math.sqrt((a + b) / 2)
    lingd = int((elips / skalawidht) + 6)

    print(elips)
    print("Lingkar Dada", (int(lingd)), "cm")

    # hitung lingkar pinggang 6
    pinggang1 = math.pow(shaped[11][1] - shaped[12][1], 2)  # hip1
    pinggang2 = math.pow(shaped[11][0] - shaped[12][0], 2)  # hip2
    lpinggang = math.sqrt(pinggang1 + pinggang2)  # lebar pinggang
    lpinggang2 = lpinggang / 2
    a1 = math.pow(lpinggang, 2)
    b1 = math.pow(lpinggang2, 2)
    elips1 = 2 * math.pi * math.sqrt((a1 + b1) / 2)
    lingkarpinggang = int((elips1 / skalawidht) + 35)

    print(elips1)
    print("Lingkar pinggang", (int(lingkarpinggang)), "cm")

    # hitung lingkar pinggul 7
    pinggul1 = math.pow(shaped[11][1] - shaped[12][1], 2)  # hip1
    pinggul2 = math.pow(shaped[11][0] - shaped[12][0], 2)  # hip2
    lpinggul = math.sqrt(pinggul1 + pinggul2)  # lebar panggul
    lpinggul2 = lpinggul / 2
    a2 = math.pow(lpinggul, 2)
    b2 = math.pow(lpinggul2, 2)
    elips2 = 2 * math.pi * math.sqrt((a2 + b2) / 2)
    lingkarpinggul = int((elips2 / skalawidht) + 49)

    print(elips2)
    print("Lingkar pinggul", (int(lingkarpinggul)), "cm")

    # hitung lingkar paha 8
    paha1 = math.pow(shaped[5][1] - shaped[6][1], 2)  # kaki1
    paha2 = math.pow(shaped[5][0] - shaped[6][0], 2)  # kaki2
    lebarkaki = math.sqrt(paha1 + paha2)  # lebar 1 celana
    lebarkaki2 = lebarkaki / 2
    lingkaran = math.pi * lebarkaki2
    lebarpaha = int((lingkaran / skalawidht) + 32)

    print(lingkaran)
    print("Lingkar paha", (int(lebarpaha)), "cm")

    if ld <= 46 and pk <= 68 and pt <= 60   :
        ukuran = "S"
    elif ld <= 47 and pk <= 70 and pt <= 62  :
        ukuran = "M"
    elif ld <= 48 and pk <= 73 and pt <= 63  :
        ukuran = "L"
    elif ld <= 49 and pk <= 75  and pt <= 65 :
        ukuran = "XL"
    else:
      ukuran= "XXL"

    Hasil_Pengukuran =[ ld, pk, pt, ukuran]
    

    if lingkarpinggang <= 73 and pc<= 99  :
        ukuran2 = "28"
    elif lingkarpinggang <= 75 and pc<= 100  :
        ukuran2 = "29"
    elif lingkarpinggang <= 78 and pc<= 101 :
        ukuran2 = "30"
    elif lingkarpinggang <= 80 and pc<= 102 :
        ukuran2 = "31"
    elif lingkarpinggang <= 83 and pc<= 102 :
        ukuran2 = "32"
    elif lingkarpinggang <= 85 and pc<= 104 :
        ukuran2 = "33"
    elif lingkarpinggang <= 88 and pc<= 104 :
        ukuran2 = "34"
    elif lingkarpinggang <= 90 and pc<= 105 :
        ukuran2 = "35"
    elif lingkarpinggang <= 93 and pc<= 105 :
        ukuran2 = "36"
    elif lingkarpinggang <= 95 and pc<= 106:
        ukuran2 = "37"
    elif lingkarpinggang <= 98 and pc<= 106 :
        ukuran2 = "38"
    else:
        ukuran2 = "39"

    Hasil_Pengukuran2=[ lingkarpinggang,pc,ukuran2]

    print (Hasil_Pengukuran)
    print (Hasil_Pengukuran2)

    path_file = "static/%s.jpg" % uuid.uuid4().hex
    cv2.imwrite(path_file, image)

    return jsonify(
        bahu=ld,
        tangan=pt,
        badan=pk,
        panjang_kaki=pc,
        lingkar_dada=lingd,
        lingkaran_pinggang=lingkarpinggang,
        lingkar_pinggul=lingkarpinggul,
        lingkar_paha=lebarpaha,
        ukuran_kemeja=ukuran,
        ukuran_celana=ukuran2,
        gambar=path_file,
        message="Berhasil",
        status="OK",
    )


@app.route("/test2", methods=["GET", "POST"])
def detect2():
    # Check if an image file is present in the request
    if "image_post" not in request.files:
        return jsonify(
            bahu="0",
            tangan="0",
            badan="0",
            panjang_kaki="0",
            lingkar_dada="0",
            lingkaran_pinggang="0",
            lingkar_pinggul="0",
            lingkar_paha="0",
            ukuran_jas="0",
            ukuran_rok="0",
            gambar="0",
            message="Gak Berhasil",
            status="NOK",
        )

    image_file = request.files["image_post"]
    interpreter = tf.lite.Interpreter(
        model_path="lite-model_movenet_singlepose_lightning_3.tflite"
    )
    interpreter.allocate_tensors()

    # Read the image file using OpenCV
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # membacagambar
    imagedt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    width = imagedt.shape[1]
    height = imagedt.shape[0]
    # resizeimage
    img = imagedt.copy()
    img = tf.image.resize_with_pad(np.expand_dims(imagedt, axis=0), 192, 192)

    # converttofloat
    input_image = tf.cast(img, dtype=tf.float32)

    # detailinputoutput
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # penggabungan gambar dengan image data
    interpreter.set_tensor(input_details[0]["index"], np.array(input_image))
    interpreter.invoke()
    # keypoint
    keypointsdetection = interpreter.get_tensor(output_details[0]["index"])
    shaped = np.squeeze(
        np.multiply(
            interpreter.get_tensor(interpreter.get_output_details()[0]["index"]),
            [height, width, 1],
        )
    ).astype(int)
    shaped[0], shaped[1]

    EDGES = {
        (0, 1): "m",
        (0, 2): "c",
        (1, 3): "m",
        (2, 4): "c",
        (0, 5): "m",
        (0, 6): "c",
        (5, 7): "m",
        (7, 9): "m",
        (6, 8): "c",
        (8, 10): "c",
        (5, 6): "y",
        (5, 11): "m",
        (6, 12): "c",
        (11, 12): "y",
        (11, 13): "m",
        (13, 15): "m",
        (12, 14): "c",
        (14, 16): "c",
    }

    # drawkeypoint
    for kp in shaped:
        ky, kx, kp_conf = kp
        image = cv2.circle(imagedt, (int(kx), int(ky)), 20, (0, 255, 0), -1)
        continue
    # drawline
    for edge, color in EDGES.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        image = cv2.line(
            imagedt, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10
        )
        continue

    # hitungskala
    # menghitung skala gambar tinggi
    skalaheight = ((height * 200) / 250) / 200

    # menghitung skala gambar lebar
    skalawidht = ((width * 200) / 140) / 200

    # perhitungan Euclidean Distance
    # hitung bahu
    bahu1 = math.pow(shaped[5][1] - shaped[6][1], 2)
    bahu2 = math.pow(shaped[5][0] - shaped[6][0], 2)
    Panjang_Bahu = math.sqrt(bahu1 + bahu2)
    ld = int((Panjang_Bahu / skalawidht) + 26)

    print(Panjang_Bahu)
    print("lebar bahu", (int(ld)), "cm")

    # hitung panjang tangan 2
    tangan1 = math.pow(shaped[10][1] - shaped[6][1], 2)
    tangan2 = math.pow(shaped[10][0] - shaped[6][0], 2)
    Panjang_Tangan = math.sqrt(tangan1 + tangan2)
    pt = int((Panjang_Tangan / skalaheight) + 8)

    print(Panjang_Tangan)
    print("Panjang Tangan", (int(pt)), "cm")

    # huitung panjang kemeja 3
    kemeja1 = math.pow(shaped[12][1] - shaped[6][[1]], 2)
    kemeja2 = math.pow(shaped[12][0] - shaped[6][0], 2)
    panjang_kemeja = math.sqrt(kemeja1 + kemeja2)
    pk = int((panjang_kemeja / skalaheight) + 4)

    print(panjang_kemeja)
    print("Panjang baju", (int(pk)), "cm")

    # huitung panjang celana
    celana1 = math.pow(shaped[16][1] - shaped[12][[1]], 2)
    celana2 = math.pow(shaped[16][0] - shaped[12][0], 2)
    panjang_celana = math.sqrt(celana1 + celana2)
    pc = int((panjang_celana / skalaheight) + 19)

    print(panjang_celana)
    print("Panjang celana", (int(pc)), "cm")

    # hitung lingkar dada 5
    d1 = math.pow(shaped[5][1] - shaped[6][1], 2)  # bahu1
    d2 = math.pow(shaped[5][0] - shaped[6][0], 2)  # bahu2
    pd = math.sqrt(d1 + d2)  # lebar dada
    pd2 = pd / 2
    a = math.pow(pd, 2)
    b = math.pow(pd2, 2)
    elips = 2 * math.pi * math.sqrt((a + b) / 2)
    lingd = int((elips / skalawidht) + 30)

    print(elips)
    print("Lingkar Dada", (int(lingd)), "cm")

    # hitung lingkar pinggang 6
    pinggang1 = math.pow(shaped[11][1] - shaped[12][1], 2)  # hip1
    pinggang2 = math.pow(shaped[11][0] - shaped[12][0], 2)  # hip2
    lpinggang = math.sqrt(pinggang1 + pinggang2)  # lebar pinggang
    lpinggang2 = lpinggang / 2
    a1 = math.pow(lpinggang, 2)
    b1 = math.pow(lpinggang2, 2)
    elips1 = 2 * math.pi * math.sqrt((a1 + b1) / 2)
    lingkarpinggang = int((elips1 / skalawidht) + 28)

    print(elips1)
    print("Lingkar pinggang", (int(lingkarpinggang)), "cm")

    # hitung lingkar pinggul 7
    pinggul1 = math.pow(shaped[11][1] - shaped[12][1], 2)  # hip1
    pinggul2 = math.pow(shaped[11][0] - shaped[12][0], 2)  # hip2
    lpinggul = math.sqrt(pinggul1 + pinggul2)  # lebar panggul
    lpinggul2 = lpinggul / 2
    a2 = math.pow(lpinggul, 2)
    b2 = math.pow(lpinggul2, 2)
    elips2 = 2 * math.pi * math.sqrt((a2 + b2) / 2)
    lingkarpinggul = int((elips2 / skalawidht) + 45)

    print(elips2)
    print("Lingkar pinggul", (int(lingkarpinggul)), "cm")

    if ld <= 38 and pk <= 63 and pt <= 51:
        ukuran3 = "S"
    # print("UKURAN JAS S")
    elif ld <= 39 and pk <= 63 and pt <= 51:
        ukuran3 = "M"
    # print("UKURAN JAS M")
    elif ld <= 40 and pk <= 63 and pt <= 52:
        ukuran3 = "L"
    # print("UKURAN JAS L")
    else:
        ukuran3 = "XL"
        # print("UKURAN JAS XL")

    Hasil_Pengukuran3 = [ld, pt, pk, ukuran3]

    if lingkarpinggang <= 72 and pc <= 90:
        ukuran4 = "S"
        # print("UKURAN ROK S")
    elif lingkarpinggang <= 76 and pc <= 90:
        ukuran4 = "M"
        # print("UKURAN ROK M")
    elif lingkarpinggang <= 80 and pc <= 92:
        ukuran4 = "L"
        # print("UKURAN ROK L")
    else:
        ukuran4 = "XL"
        # print("UKURAN ROK XL")

    Hasil_Pengukuran4 = [lingkarpinggang, pc, ukuran4]

    print(Hasil_Pengukuran3)
    print(Hasil_Pengukuran4)

    path_file = "static/%s.jpg" % uuid.uuid4().hex
    cv2.imwrite(path_file, image)

    return jsonify(
        bahu=ld,
        tangan=pt,
        badan=pk,
        panjang_kaki=pc,
        lingkar_dada=lingd,
        lingkaran_pinggang=lingkarpinggang,
        lingkar_pinggul=lingkarpinggul,
        ukuran_jas=ukuran3,
        ukuran_rok=ukuran4,
        gambar=path_file,
        message="Berhasil",
        status="OK",
    )


app.run(host="127.0.0.1", port=5000)
