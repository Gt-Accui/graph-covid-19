# gra-cov-19
"gra-cov-19" is the app that plots the chart(s) when you upload a CSV file.

# DEMO
- ## [Demo on Heroku](https://graph-covid-19.herokuapp.com/ "gra-cov-19")

# Notice
I'm sorry.  I am a Japanese who is **not very good at English**.  
So this README may be a little difficult to read ~~because it is written using google translate~~.

Also, "gra-cov-19" is the app **made in practice**.  
**Enjoy** if it behaves unexpectedly.

# Features
"gra-cov-19" reads the CSV file as soon as that is uploaded and assigns an axis from the values in each column.  
And if it has one X-axis and one or more Y-axes, "gra-cov-19" immediately tries to plot the line chart(s).  
At this time, assign a numerical value to the Y-axis and other values to the X-axis.

By the way, the name is not "cha-cov-19" because the word "gra-cov" has a good feeling  
... and the glyphs of **"g" and "9" are similar**.

# Requirement

"hoge"を動かすのに必要なライブラリなどを列挙する
 
* huga 3.5.2
* hogehuga 1.0.2
 
# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する
 
```bash
pip install huga_package
```
 
# Usage
 
DEMOの実行方法など、"hoge"の基本的な使い方を説明する
 
```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```
 
# Note
The main target is open data released by the Japanese Ministry of Health, Labor and Welfare.  
https://www.mhlw.go.jp/stf/covid-19/open-data.html  
For example, the CSV file is "UTF-8" encoded, contains headers, and has a date as the Key.

# License
"gra-cov-19" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
