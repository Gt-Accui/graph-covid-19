# gra-cov-19
"gra-cov-19" is the app that plots the chart(s) when you upload a CSV file.

# DEMO
![gra-cov-19](https://user-images.githubusercontent.com/63509152/106367252-8863b200-6384-11eb-8fb0-3c1ecc7c441c.gif)
- ## [Demo on Heroku](https://graph-covid-19.herokuapp.com/ "gra-cov-19")

# Notice
I'm sorry.  I am a Japanese who is **not very good at English**.  
So this README may be a little difficult to read ~~because it is written using google translate~~.

Also, "グラコヴ19"( : "gra-cov-19") is the app **made in practice**.  
**Enjoy** if it behaves unexpectedly.

# Features
"gra-cov-19" reads the CSV file as soon as that is uploaded and assigns an axis from the values in each column.  
And if it has one X-axis and one or more Y-axes, "gra-cov-19" immediately tries to plot the line chart(s).  
At this time, assign a numerical value to the Y-axis and other values to the X-axis.

By the way, the name is not "chart-covid-19" because the word "gra-cov" has a good feeling  
... and the glyphs of **"g" and "9" are similar**.

# Usage
## 1. CSV file registration
- Press the "新規"( : "New") button at the top right of the index page. (Then the 'create' page opens.)
- Enter in each field. ("名称" : "Name" , "出典" : "Source")
- Select a CSV file. (You can drag and drop.)
- Press the button "保存"( : "Save") at the bottom right of the page.

The chart(s) will then be plotted if possible. 
## 2. Change chart(s) settings
- Press the tab button "設定" ( : Settings) at the top left of the page.
- Change the value of any field.  
("種別" : "Type" , "折れ線グラフ" : "Line chart(s)" , "積み棒グラフ" : "Stacking bar chart(s)" , "軸" : "Axis" , "表示名" : "Display name")
- Press the corresponding button "保存"( : "save").

The settings will be reflected.
# Note
The main target is open data released by the Japanese Ministry of Health, Labor and Welfare.  
https://www.mhlw.go.jp/stf/covid-19/open-data.html  
For example, the CSV file is "UTF-8" encoded, contains headers, and has a date as the Key.

# Requirement
asgiref 3.3.1
python 3.9.1  
beautifulsoup4 4.9.3  
dj-database-url 0.5.0  
Django 3.1.4  
django-bootstrap4 2.3.1  
django-crispy-forms 1.10.0  
django-filter 2.4.0  
importlib-metadata 2.1.1  
numpy 1.19.3  
pandas 1.1.5  
python-dateutil 2.8.1  
plotly 4.14.1  
pytz 2020.4  
retrying 1.3.3  
six 1.15.0  
soupsieve 2.1  
sqlparse 0.4.1  
whitenoise 5.2.0  
zipp 3.4.0

# License
"gra-cov-19" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
