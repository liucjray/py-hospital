import re
import requests
from PIL import Image
import pytesseract

from config.config import *
from helpers.Common import *
from helpers.Encoder import *


class OCRService:
    config = None
    img = None

    def __init__(self):
        self.config = dict(get_config())
        self.img_dir = dict_get(self.config, 'OCR.IMG_DIR')

    def get_tesseract(self):
        cmd = dict_get(self.config, 'OCR.CMD_PATH')
        pytesseract.pytesseract.tesseract_cmd = cmd
        return pytesseract

    def set_img(self, path):
        self.img = Image.open(path)
        self.img = self.img.convert('L')
        return self

    def to_string(self, pass_img=None):
        if pass_img is not None:
            self.img = pass_img
        return self.get_tesseract().image_to_string(self.img)

    def download_img(self):
        url = 'http://www.kmuh.org.tw/NetRegQuery/UserControl/CaptchaImage.ashx'
        r = requests.get(url)
        ext = r.headers['Content-Type'].split('/')[1]
        tmp_name = to_md5(r.text) + '.' + ext

        # save image
        tmp_img_path = self.img_dir + tmp_name
        with open(tmp_img_path, 'wb') as f:
            f.write(r.content)

        # image to string
        ans = self.set_img(tmp_img_path).to_string()
        new_ans = ''.join(re.findall(self.get_pattern(), ans))
        pass

        if len(ans) == 4:
            os.rename(tmp_img_path, self.img_dir + ans + '.' + ext)
            print('parse success: ' + ans + ' / ' + new_ans)
        else:
            os.remove(tmp_img_path)
            print('parse failed: ' + ans + ' / ' + new_ans)

    def get_pattern(self):
        return '[a-zA-Z0-9]'

    def del_all_imgs(self):
        folder = self.img_dir
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

# img = dict_get(ocr.config, 'OCR.IMG_DIR', None)
# ans = ocr.set_img(img + 'B5WD.jpg').to_string()
# print(ans)
# ans = ocr.set_img(img + 'JA57.jpg').to_string()
# print(ans)
# ans = ocr.set_img(img + 'P7L9.jpg').to_string()
# print(ans)
# ans = ocr.set_img(img + 'Y6Y9.jpg').to_string()
# print(ans)
