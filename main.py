import os
import re
import bs4
import time
import requests
import pprint

import MeCab

from wordcloud import WordCloud
import numpy as np
from PIL import Image

import crowling, Morphological_analysis, word_of_songs_wordcloud

font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

def main():
    txt_name = crowling.excute()
    output = Morphological_analysis.analyze(txt_name)
    word_of_songs_wordcloud.wordcloud(output, txt_name)


if __name__ == '__main__':
    main()
    