from bs4 import BeautifulSoup
import requests
import re
import schedule
import time



def remove(string):
    pattern = re.compile(r'น' r'\s+')
    #pattern = re.compile(r'รอบที่ บน-ล่าง รายละเอียด')
    return re.sub(pattern, ' น.\n', string)

def lottoyekee():

    url = "https://www.lottoheng168.com/Manager/Result"
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all('table',{ "class" : "table table-striped table-dark resultlotto"},limit=10)
    for tag in tags:
        textdata = remove(tag.get_text()).replace("รายละเอียด","")
        reCom = textdata.replace('\n','-').replace('น.-','น.\n📢 3ตัว:').replace(',',' 🔸 2ตัว:').replace('----','\n')
        print(reCom.replace('---รอบที่-บน-ล่าง\n--',''))
        my_data_file = open("help/lotto.txt","w")
        my_data_file.write('ผลหวยจับยี่กี 2️⃣4️⃣ ชั่วโมง\n\n'+reCom.replace('---รอบที่-บน-ล่าง\n--',''))
        my_data_file.close()
