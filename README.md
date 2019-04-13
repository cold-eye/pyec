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
c = Corrector(special_file="movies.txt")
print(c.correct_special_word("三傻大闹宝莱屋"))
```
结果：
```python
三傻大闹宝莱坞
```




