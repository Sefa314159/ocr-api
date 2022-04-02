import paddleocr
import re
import hashlib
import requests


def download_image(image_url):
    try:
        response = requests.get(image_url)
    except Exception as e:
        return e

    img_name = image_url.split('/')[-1]
    img_name = re.sub('[!@#$?=:,+,-]', '', img_name)
    img_name = hashlib.md5(img_name.encode("utf-8")).hexdigest()
    path = 'tmp/' + img_name + ".jpg"
    file = open(path, "wb")
    file.write(response.content)
    file.close()
    return path


def read_text_from_image(image_path):
    paddle_ocr_en = paddleocr.PaddleOCR(lang='en', use_gpu=False, use_angle_cls=True, use_dilation=True,
                                        max_text_length=50,
                                        label_list=['0', '45', '60', '90', '135', '180', '225', '270', '315'],
                                        enable_mkldnn=True, det_sast_polygon=True, gpu_mem=1250, use_mp=True)
    text_and_boxes = paddle_ocr_en.ocr(image_path, det=True, rec=True, cls=True)
    return " ".join([i[1][0] for i in text_and_boxes])
