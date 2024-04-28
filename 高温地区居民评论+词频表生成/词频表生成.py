import pandas as pd
import jieba
from collections import Counter

# 读取Excel文件
data = pd.read_excel('comments.xlsx')

# 将新闻标题数据转换为字符串格式
news_titles = ' '.join(data['评论'].astype(str))

# 使用jieba分词进行中文分词
word_list = jieba.lcut(news_titles)

# 设置停用词列表（可根据实际需要添加）
stopwords = ['的', '了', '和', '在', '是', '我', '你']

# 去除停用词
word_list = [word for word in word_list if word not in stopwords]

# 统计词频
word_counts = Counter(word_list)

# 创建词频表的DataFrame
word_freq_table = pd.DataFrame({'词语': [], '频次': []})

# 填充词频表的数据
for word, count in word_counts.most_common():
    word_freq_table = word_freq_table._append({'词语': word, '频次': count}, ignore_index=True)

# 将词频表保存为Excel文件
word_freq_table.to_excel('word_freq.xlsx', index=False)
