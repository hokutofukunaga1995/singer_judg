import MeCab
from settings import *

def analyze(txt_name):
    #スクレイピングした歌詞のデータを取得
    txt_path = txt_files_path + txt_name
    words_of_song = open(txt_path, 'r').read()

    #曲ごとに区切る
    lines = words_of_song.split('\n')
    num = len(lines)

    mecab = MeCab.Tagger('-Ochasen')
    mecab.parse('')

    #一曲ごとに取得
    for i in range(num): 
        node = mecab.parseToNode(lines[i])
        output = []

        #意味をなさないような単語を除外する。
        stoplist=['「', '」', 'じゅう', 'そこら', 'れる', 'くい','ん','よう','の']

        # 品詞に分解して、助詞や接続詞などは除外している。
        while node:
            word_type = node.feature.split(",")[0]
            if word_type in ["名詞","形容詞","副詞","動詞"]:
                if not node.surface in stoplist and not node.surface.isdigit():
                    output.append(node.surface.upper())
            node = node.next
        #形態素解析された単語のリストをWordCloud用に処理している。
        text = ' '.join(output)

    return text
    




