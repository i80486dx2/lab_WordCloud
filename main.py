import os
import re
import json
import argparse
from wordcloud import WordCloud
from MeCab import Tagger
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np 
import re

# コマンドライン引数受け取り
parser = argparse.ArgumentParser()
parser.add_argument('-path', help='データのパスを指定する ./data/~/',required=True) 
parser.add_argument('-c', nargs='*', help='指定したチャンネルのWordCloudを作成する',required=True) 
parser.add_argument('-mask', help='マスク画像のパスを指定する ./~.png') 
args = parser.parse_args()

channels = args.c
path = args.path
if args.mask is not None:
    mask_img = np.array(Image.open(args.mask))

# テキスト取得
texts = ''
for i in range(len(channels)):
    files = os.listdir(path+channels[i])
    for j in range(len(files)):
        file_name = os.path.join(path,channels[i],files[j])
        f = open(file_name, 'r')
        tmp = json.load(f)  
        for k in range(len(tmp)):
            string = tmp[k]['text'].replace('\n', '')
            string = re.sub(r'<.*>','',string)
            string = re.sub(r':.*:','',string)
            texts += string

# 分かちがち
m = Tagger()
parse_text = m.parse(texts)
parse_text = parse_text.split('\n')
re_m_text = ''
for i in range(len(parse_text)):
    if '名詞' in parse_text[i] and  parse_text[i].isdigit() == False :
        if  (not "非自立" in parse_text[i]) and (not "代名詞" in parse_text[i]) and (not "数" in parse_text[i]) and (len(parse_text[i].split()[0]) > 1):
            re_m_text += parse_text[i].split()[0] + '\n'

 # ストップワードの設定
stop_words = []
tmp = open("stopwords.txt", encoding="utf-8").read().split()
for i in range(len(tmp)):
    stop_words.append(tmp[i])

# WordCloud作成
if args.mask is not None:
    wordcloud = WordCloud(
        font_path="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
        max_font_size=60,
        stopwords=set(stop_words),
        mask=mask_img,
        background_color="white"
    ).generate(re_m_text)
else:
    wordcloud = WordCloud(
        font_path="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
        max_font_size=60,
        stopwords=set(stop_words),
        background_color="white"
    ).generate(re_m_text)

# 画像保存
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.rcParams['figure.dpi'] = 500

if args.mask is not None:
    plt.savefig(args.mask[:-4] + '_output.png', dpi=400)
else:
    plt.savefig('output.png', dpi=400)