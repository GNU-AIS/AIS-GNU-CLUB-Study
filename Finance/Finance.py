from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time

# 네이버에서 종목 코드를 불러옴
def searchNameForNaver(name):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')
    wd.get(url+name)
    time.sleep(1)
    
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tagEm = soup.find('em', attrs={'class':'t_nm'})
    print(tagEm.string)
    return tagEm.string
    
# 네이버 금융에서 증시 정보를 검색 저장
def searchFinance(code, maxPage):
    url = "https://finance.naver.com/item/sise_day.naver?code="
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')
    wd.get(url+code)
    time.sleep(1)

    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')

    '''pgrr = soup.find('td', class_='pgRR')
    pgrr.a["href"].split('=')
    lastPage = int(pgrr.a["href"].split('=')[-1])'''
    
    thStringList = []
    spanStringList = []

    thList = soup.tbody.select('th')
    
    for th in thList:
        thStringList.append(th.string)
    
    for cntPage in range(int(maxPage)):
        pageUrl = url+code+'&page='+str(cntPage+1)
        data = requests.get(pageUrl, headers={'User-agent': 'Mozilla/5.0'}).text
        
        soup = BeautifulSoup(data, 'html.parser')
        spanList = soup.select('span')
        spanList.pop(0)

        for span in spanList:
            if span.string.find('\t') != -1:
                tmp = span.string
                tmp = tmp.strip('\n')
                tmp = tmp.strip('\t')
                tmp = tmp.replace('\n', '')
                spanStringList.append(tmp)
                continue


            spanStringList.append(span.string)
    
    l = [spanStringList[r*7:(r+1)*7]for r in range(10*int(maxPage))]
    
    return [thStringList, l]


def main():
    result = []
    print("크롤링 시작 >")
    searchName = input('검색 기업을 입력하시오: ')
    maxPage = input('최대 페이지를 입력하시오: ')
    code = searchNameForNaver(searchName)
    result = searchFinance(code, maxPage)
    
    CB_tbl = pd.DataFrame(result[1], columns = tuple(result[0]))
    CB_tbl.to_csv('./today.csv', encoding='cp949', mode='w', index=True)
    

if __name__ == '__main__':
    main()