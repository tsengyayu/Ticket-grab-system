# from selenium import webdriver
# driver = webdriver.Chrome('/Users/zengalier/Desktop/chromedriver')
# driver.get('https://selcrs.nsysu.edu.tw/')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
from keras import models
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

s = Service('/Users/zengalier/Desktop/chromedriver')
browser = webdriver.Chrome(service=s)
url = 'https://selcrs.nsysu.edu.tw/'
browser.get(url)

account = browser.find_element("xpath", '/html/body/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td/div[1]/form/div[1]/input')
account.clear()
account.send_keys('B084020052')

password = browser.find_element("xpath", '/html/body/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td/div[1]/form/div[2]/input')
password.clear()
password.send_keys('123456Zx')

browser.save_screenshot('/Users/zengalier/Desktop/test.png')
element = browser.find_element("id", "imgVC")
# element = browser.find_element_by_id("imgVC")
print(element.location)  # 打印元素坐标
print(element.size)  # 打印元素大小

left = element.location['x'] * 2
top = element.location['y'] * 2
right = (element.location['x'] + element.size['width']) * 2
bottom = (element.location['y'] + element.size['height']) * 2
img = Image.open('/Users/zengalier/Desktop/test.png')
im = img.crop((left, top, right, bottom))
im.show()
im.save('/Users/zengalier/Desktop/code.png')

img_rows = None
img_cols = None
digits_in_img = 4
model = None
np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

def split_digits_in_img(img_array):
    x_list = list()
    for i in range(digits_in_img):
        step = img_cols // digits_in_img
        x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
    return x_list

if os.path.isfile('cnn_model.h5'):
    model = models.load_model('cnn_model.h5')
else:
    print('No trained model found.')
    exit(-1)

# img_filename = input('Varification code img filename: ')
img = load_img('/Users/zengalier/Desktop/code.png', color_mode='grayscale')
img_array = img_to_array(img)
img_rows, img_cols, _ = img_array.shape
x_list = split_digits_in_img(img_array)

varification_code = list()

for i in range(digits_in_img):
    confidences = model.predict(np.array([x_list[i]]), verbose=0)
    # result_class = model.predict_classes(np.array([x_list[i]]), verbose=0)
    predict_x = model.predict(np.array([x_list[i]]))
    result_class = np.argmax(predict_x, axis=1)
    varification_code.append(result_class[0])
    print('Digit {0}: Confidence=> {1}    Predict=> {2}'.format(i + 1, np.squeeze(confidences), np.squeeze(result_class)))
print('Predicted varification code:', varification_code)

var1 = str(varification_code[0])
var2 = str(varification_code[1])
var3 = str(varification_code[2])
var4 = str(varification_code[3])
answer = var1+var2+var3+var4
print(answer)
code = browser.find_element("name", 'ValidCode')
code.clear()
code.send_keys(answer)
browser.find_element("xpath", '/html/body/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td/div[1]/form/div[4]/span/input').click()
print("finished")