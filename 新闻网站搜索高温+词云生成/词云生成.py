import random
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取Excel文件
data = pd.read_excel('news.xlsx')

# 将新闻标题数据转换为字符串格式
news_titles = ' '.join(data['新闻标题'].astype(str))

# 使用jieba分词进行中文分词
word_list = jieba.lcut(news_titles)

# 设置停用词列表（可根据实际需要添加）
stopwords = ['的', '了', '和', '在', '是', '我', '你', '专家', '多地',
             '或', '发布', '将', '今日', '有', '吗', '等', '下']


def warm_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # 生成随机的暖色调（适合高温题材）
    h = random.randint(0, 30)
    s = random.randint(60, 100)
    l = random.randint(50, 70)
    return f"hsl({h}, {s}%, {l}%)"


# 去除停用词
word_list = [word for word in word_list if word not in stopwords]

# 将词语列表转换为空格分隔的字符串
words = ' '.join(word_list)

for i in range(1, 11):  # 循环十个以挑选最好的
    # 生成词云图
    wordcloud = WordCloud(max_words=40, width=1000, height=1000,
                          font_path="/Users/tomatotaco1/Library/Fonts/FZLTHProGlobal-Demibold.TTF",
                          background_color='white', color_func=warm_color_func).generate(words)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # 保存词云图为图片文件
    wordcloud.to_file('wordcloud' + str(i) + '.png')
