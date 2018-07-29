#--------------- coding:utf8 -------------
import jieba
from os import path  #用来获取文档的路径

#词云
from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
#词云生成工具
from wordcloud import WordCloud,ImageColorGenerator
#需要对中文进行处理
import matplotlib.font_manager as fm

#背景图
bg=np.array(Image.open("张静.jpg"))

#获取当前的项目文件加的路径
d=path.dirname(__file__) 
#读取停用词表
stopwords_path='stopwords.txt'
#添加需要自定以的分词
jieba.add_word("葡萄牙")
jieba.add_word("阿根廷")
jieba.add_word("乌拉圭")

#读取要分析的文本
text_path="signature.txt"
#读取要分析的文本，读取格式
text=open(path.join(d,text_path),encoding="utf8").read()
#定义个函数式用于分词
def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    #进行分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    #打开停用词表
    f_stop=open(stopwords_path,encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
    return ' '.join(mywordList)
text1=jiebaclearText(text)
#生成
wc=WordCloud(
    background_color="white", 
    max_words=200,
    mask=bg,            #设置图片的背景
    max_font_size=60,

    random_state=42,
    font_path='/home/dys/pythonTest/simheittf/simhei.ttf'
    # font_path='C:/Windows/Fonts/simkai.ttf'   #中文处理，用系统自带的字体
    ).generate(text1)
#为图片设置字体
# my_font=fm.FontProperties(fname='C:/Windows/Fonts/simkai.ttf')
my_font = fm.FontProperties(fname='/home/dys/pythonTest/simheittf/simhei.ttf')
#产生背景图片，基于彩色图像的颜色生成器
image_colors=ImageColorGenerator(bg)
#开始画图
plt.imshow(wc.recolor(color_func=image_colors))
#为云图去掉坐标轴
plt.axis("off")
#画云图，显示
plt.figure()
#为背景图去掉坐标轴
plt.axis("off")
plt.imshow(bg,cmap=plt.cm.gray)

#保存云图
wc.to_file("gril.png")
plt.show()