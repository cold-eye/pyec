# pyec
中文纠错以及英文纠错

## 安装依赖
git clone https://github.com/fengzuo97/pyec.git  
cd pyec  
pip install -r requirements.txt  
系统需要是linux，kenlm需要手动按照官网的要求编译。 

## 如何使用
```python
from cn_corrector import Corrector
```
短文本纠错，例如电影网站需要对用户的搜索关键字进行纠错，首先将电影名字统计成为一个文件，每个名字一行。
原理是利用编辑距离或者音近字寻找候选集，判断候选集是否在统计文件中。
```python
c = Corrector(special_file="movies.txt", ngram_model="people_chars_lm.klm")
print(c.correct_special_word("三傻大闹宝莱屋"))
```
结果：
```python
三傻大闹宝莱坞
```
长文本纠错，有两种方式，一种是用ngram模型，另一种是用bert预测mask，ngram模型来自pycorrector，可以自己训练大模型替换。
```python
c.correct_sentence("奥巴马总统访文中国。") 
c.correct_sentence("我把我的眼睛弄丢了")
c.correct_with_bert("我把我的眼睛弄丢了")
```
结果:
```python
[6, '问'] 
[]
[[5, '镜']] 
```
ngam语言模型纠错不能纠正real word的错误，但是利用Bert预训练的mask预测可以。

## 不完善之处
这个纠错程序还不完善，为了降低误判率，我将错误的情况限定为一句话中只有一个错误，并且错误的字是音近字，虽然这种做法可以涵盖大部分情况，并且大幅度降低误判率，但是会漏掉很多错误情况，

## 未来的工作
添加英文纠错  
添加神经网络的语言模型代替ngram






