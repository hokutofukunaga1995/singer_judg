import os
import re
import bs4
import time
import requests
import pprint

#サイトから特定の歌手の歌詞を集める


#html取得
def load(url):
    res = requests.get(url)

    return res.text


#htmlの中から歌詞を取得
def pickup_tag(html, find_tag):
    soup = bs4.BeautifulSoup(str(html), 'html.parser')
    paragraphs_all = soup.find_all(find_tag)

    return paragraphs_all


#歌詞の整形
def parse(html):
    soup = bs4.BeautifulSoup(str(html), 'html.parser')
    #htmlタグの削除
    words_of_song_row = soup.getText()
    words_of_song_row = words_of_song_row.replace('\n', '')
    words_of_song_row = words_of_song_row.replace('　', '')

    #英数字の削除
    words_of_song_row = re.sub(r'[a-zA-Z0-9]', '', words_of_song_row)
    words_of_song_row = re.sub(r'[ ＜＞♪`‘’“”・…_！？!-/:-@[-`{-~]', '', words_of_song_row)
    words_of_song = re.sub(r'注意：.+', '', words_of_song_row)

    return words_of_song


def excute():
    artist_url = input('歌詞データの欲しい歌手のuta-netページのurlをコピペしてください: ')
    while artist_url == '':
        artist_url = input('入力されていません。歌詞データの欲しい歌手のuta-netページのurlをコピペしてください: ')
    
    try:
        #ページの取得
        html = load(artist_url)

        #アーティスト名取得
        soup = bs4.BeautifulSoup(str(html), 'html.parser')
        artist_name_td2 = soup.find(class_='td2')
        artist_name_a = pickup_tag(artist_name_td2, 'a')[0]
        artist_name = artist_name_a.getText()
        
        #テキスト名取得
        txt_name = artist_name + '.txt'
        txt_path = os.getcwd() + '/txt_files/' + txt_name
        
        with open(txt_path, 'a') as f:

            # 曲ページの先頭アドレス
            base_url = 'https://www.uta-net.com'

            #曲ごとのurlを格納
            musics_url = []
            #歌詞を格納
            words_of_songs = ''


            """ 曲のurlを取得 """
            # 50曲までのtd要素の取り出し
            flag = 0
            for td in pickup_tag(html, 'td'):
                # a要素の取り出し
                for a in pickup_tag(td, 'a'):
                    # href属性にsongを含むか
                    if 'song' in a.get('href'): 
                        if flag < 50:
                            # urlを配列に追加
                            musics_url.append(base_url + a.get('href'))
                            flag += 1
                    else:
                        break



            """ 歌詞の取得 """
            for i, page in enumerate(musics_url):
                print('{}曲目:{}'.format(i + 1, page))
                html = load(page)
                time.sleep(2)
                for div in pickup_tag(html, 'div'):
                    # id検索がうまく行えなかった為、一度strにキャスト
                    div = str(div)
                    # 歌詞が格納されているdiv要素か
                    if r'itemprop="text"' in div:
                        # 不要なデータを取り除く
                        words_of_song = parse(div)
                        print(words_of_song, end = '\n\n')
                        # 歌詞を１つにまとめる
                        words_of_songs += words_of_song + '\n'

                        # 4秒待機
                        time.sleep(2)
                        break

            # 歌詞の書き込み
            f.write(words_of_songs)
            return txt_name
    
    except TypeError:
        print('入力URLをお確かめください')
        excute()

    except AttributeError:
        print('URLが誤っています。入力URLをお確かめください')
        excute()
