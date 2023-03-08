import base64
import json

import cv2
import flask
import numpy as np
from flask import Flask, request
from flask_cors import CORS
from matplotlib import pyplot as plt

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/grayscaleReversal", methods=['POST'])
def grayscale_reversal():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dst = 255 - gray

    base64_str = cv2.imencode('.jpg', dst)[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


@app.route("/histogram", methods=['POST'])
def histogram():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    chans = cv2.split(img)
    colors = ("b", "g", "r")
    plt.figure()
    plt.title("Flattened Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")

    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.savefig('img/histogram.jpg', dpi=300, format='png')

    base64_str = cv2.imencode('.jpg', cv2.imread('img/histogram.jpg'))[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


@app.route("/histogramEqualization", methods=['POST'])
def histogram_equalization():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eq = cv2.equalizeHist(gray)

    base64_str = cv2.imencode('.jpg', eq)[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


@app.route("/segmentedLinearTransformation", methods=['POST'])
def segmented_linear_transformation():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]  # 图片的高度和宽度
    imgStretch = np.empty((height, width), np.uint8)  # 创建空白数组
    r1, s1, r2, s2 = float(data['r1']), float(data['s1']), float(data['r2']), float(data['s2'])

    if not (0 < r1 < r2 < 255 and 0 < s1 < s2 < 255):
        return "ERROR"

    k1 = s1 / r1  # imgGray[h,w] < r1:
    k2 = (s2 - s1) / (r2 - r1)  # r1 <= imgGray[h,w] <= r2
    k3 = (255 - s2) / (255 - r2)  # imgGray[h,w] > r2
    for h in range(height):
        for w in range(width):
            if gray[h, w] < r1:
                imgStretch[h, w] = k1 * gray[h, w]
            elif r1 <= gray[h, w] <= r2:
                imgStretch[h, w] = k2 * (gray[h, w] - r1) + s1
            elif gray[h, w] > r2:
                imgStretch[h, w] = k3 * (gray[h, w] - r2) + s2

    plt.figure(figsize=(8, 3))
    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.8, wspace=0.1, hspace=0.1)
    plt.subplot(131), plt.title("s=T(r)")
    x = [0, r1, r2, 255]
    y = [0, s1, s2, 255]
    plt.plot(x, y)
    plt.xlabel("r, Input value")
    plt.ylabel("s, Output value")
    plt.subplot(132), plt.imshow(gray, cmap='gray', vmin=0, vmax=255), plt.title("Grey"), plt.axis('off')
    plt.subplot(133), plt.imshow(imgStretch, cmap='gray', vmin=0, vmax=255), plt.title("Stretch"), plt.axis('off')
    plt.savefig('img/segmented_linear_transformation.jpg', dpi=300, format='png')

    base64_str = cv2.imencode('.jpg', cv2.imread('img/segmented_linear_transformation.jpg'))[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


@app.route("/logarithmicTransformation", methods=['POST'])
def logarithmic_transformation():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    c = float(data['c'])

    logarithmic = np.uint8(c * np.log(1.0 + img) + 0.5)

    plt.figure(figsize=(8, 3))
    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.8, wspace=0.1, hspace=0.1)
    plt.subplot(131), plt.title("s=T(r)")
    x = np.linspace(0, 250, 250)
    y = c * np.log(1.0 + x)
    plt.plot(x, y)
    plt.xlabel("r, Input value")
    plt.ylabel("s, Output value")
    plt.subplot(132), plt.imshow(gray, cmap='gray', vmin=0, vmax=255), plt.title("Grey"), plt.axis('off')
    plt.subplot(133), plt.imshow(logarithmic, cmap='gray', vmin=0, vmax=255), plt.title("Stretch"), plt.axis('off')
    plt.savefig('img/logarithmic_transformation.jpg', dpi=300, format='png')

    base64_str = cv2.imencode('.jpg', cv2.imread('img/logarithmic_transformation.jpg'))[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


@app.route("/gammaTransformation", methods=['POST'])
def gamma_transformation():
    data = json.loads(request.get_data())
    img_stream = np.array(base64.b64decode(data['base64'])).tobytes()
    img_stream = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(img_stream, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    c, v = float(data['c']), float(data['v'])

    lut = np.zeros(256, dtype=np.float32)
    for i in range(256):
        lut[i] = c * i ** v
    gamma = np.uint8(cv2.LUT(img, lut) + 0.5)  # 像素灰度值的映射

    plt.figure(figsize=(8, 3))
    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.8, wspace=0.1, hspace=0.1)
    plt.subplot(131), plt.title("s=T(r)")
    x = np.linspace(0, 250, 250)
    y = c * x ** v
    plt.plot(x, y)
    plt.xlabel("r, Input value")
    plt.ylabel("s, Output value")
    plt.subplot(132), plt.imshow(gray, cmap='gray', vmin=0, vmax=255), plt.title("Grey"), plt.axis('off')
    plt.subplot(133), plt.imshow(gamma, cmap='gray', vmin=0, vmax=255), plt.title("Stretch"), plt.axis('off')
    plt.savefig('img/gamma_transformation.jpg', dpi=300, format='png')

    base64_str = cv2.imencode('.jpg', cv2.imread('img/gamma_transformation.jpg'))[1].tobytes()
    base64_str = base64.b64encode(base64_str).decode('utf-8')
    return flask.jsonify({'base64': base64_str})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8002)
