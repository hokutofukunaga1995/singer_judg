from wordcloud import WordCloud
import numpy as np
from PIL import Image

from settings import *

def wordcloud(txt_name, text):

    #日本語はWindowsのフォントのパスを貼り付ける
    fpath = font_path
    image_path = image_files_path
    png_path = png_files_path

    back_img = np.array(Image.open(path))
    wc = WordCloud(background_color="white",
                        font_path = fpath, width=800,height=600, mask=back_img).generate(text)
    #WordCloudの画像は同じディレクトリ内に保存されます。
    png_name = str(txt_name) + '.png'
    wc.to_file(png_path + png_name)