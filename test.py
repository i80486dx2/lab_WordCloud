import os
from wordcloud import WordCloud
from MeCab import Tagger
import matplotlib.pyplot as plt
import requests
import re


text = open("test.txt", encoding="utf-8").read()
m = Tagger()
m_text = m.parse(text)
re_m_text = re.sub("\t.*","", m_text)

url = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
r = requests.get(url)
tmp = r.text.split('\r\n')

 # ストップワードの設定
stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
            u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
            u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
            u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'',u'から',u'ため',u'性',u'による',u'版',u'出版']

for i in range(len(tmp)):
    if len(tmp[i]) < 1:
        continue
    stop_words.append(tmp[i])

wordcloud = WordCloud(
    font_path="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
    max_font_size=60,
    stopwords=set(stop_words)
).generate(re_m_text)

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

