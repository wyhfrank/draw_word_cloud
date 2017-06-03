# coding=utf-8
import codecs
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from subprocess import call

def Preprocessing(inFile, outFile):
    f = codecs.open(outFile, 'w', 'utf-8')  # 文字コードにUTF-8を指定してファイルを開く
    for line in codecs.open(inFile, 'r', 'utf-8'):  # 一行ずつファイルを読み込み
        tweet = line[:-1]  # 文末の改行コードを除く
        tweet = re.sub("\@[^\s]+\s+", "", tweet)  # @mentionを除く
        tweet = re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", tweet)  # URLを除く
        tweet = re.sub("#[^\s]+\s*", "", tweet)  # hashtagを除く
        tweet = re.sub(u'([「」\(\)（）【】『』])', r'\1\n', tweet)  # かっこで分割
        tweet = re.sub(u'([「」\(\)（）【】『』])', "", tweet)  # かっこ削除
        tweet = re.sub(u'([！？．。])', r'\1\n', tweet)  # ！？、。で分割
        if len(tweet) > 2:
            f.write(tweet)

    f.close()

def call_mecab(inFile, outFile):
    call(["mecab", inFile, '-o', outFile])

#inputはMecabの形態素解析結果
#サーバル	名詞,固有名詞,一般,*,*,*,サーバル,サーバル,サーバル

def PostProcess(inFile, outFile, stopWords): #stopWordsは辞書形式
    f=codecs.open(outFile, 'w','utf-8') #出力用ファイルをオープン
    for line in codecs.open(inFile, 'r','utf-8'):
        morph=line.strip().split('\t') #Tabで分割
        if len(morph)>1 and morph[0] not in stopWords: #Stop wordsの除去
           parts=morph[1].split(',') #コンマで分割
           if parts[0]==u'名詞' or parts[0]==u'動詞': #名詞 or 動詞を抽出したい
               f.write(morph[0] + ' ')
        else:
            f.write('\n')
    f.close()


def GenerateTagCloud(inFile):  # 前処理後のファイル（一行一単語）が入力
    tweets = ""
    for line in codecs.open(inFile, 'r', 'utf-8'):
        tweets = line[:-1] + tweets

    fpath = './yugothil.ttf'  # 日本語を使うため、システムフォントのパス指定が必要
    wordcloud = WordCloud(font_path=fpath).generate(tweets)
    # Display the generated image:
    plt.imshow(wordcloud)
    plt.axis("off")

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5, font_path=fpath).generate(tweets)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
