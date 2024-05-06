import urllib.request as request  # 導入 urllib.request 模塊，以 request 作為縮寫方便調用
import ssl  # 導入 ssl 模塊，用於處理 HTTPS 請求時的安全性問題
import bs4  # 導入 BeautifulSoup 模組，用於解析 HTML 內容
import csv  # 導入 csv 模組，用於將數據寫入 CSV 文件
ssl._create_default_https_context = ssl._create_unverified_context  # 忽略 HTTPS 安全警告


URL  = "https://www.ptt.cc/bbs/Lottery/index.html"  # 要爬取的網頁 URL

def get_data(url):
   
    requestObj = request.Request(url, headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        'Cookie': 'over18=1'
    })  # 構建請求對象，包含 headers 以模擬瀏覽器訪問

    with request.urlopen(requestObj) as response:
        data = response.read().decode('utf-8')  # 讀取響應數據並解碼為 UTF-8 格式

    root = bs4.BeautifulSoup(data, "html.parser")  # 使用 BeautifulSoup 解析 HTML 內容

    titles = root.find_all("div", class_ = "title")  # 查找所有標題元素

  
    
    for title in titles:
        article_dict = {}  # 創建空字典，用於存儲每個文章的相關信息
        if title.a != None:
            URL_NEXT = "https://www.ptt.cc" + title.a["href"]  # 獲取下一篇文章的 URL
            requestObj_2 = request.Request(URL_NEXT, headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                'Cookie': 'over18=1'
            })  # 構建第二個請求對象，獲取該文章的完整內容         

            with request.urlopen(requestObj_2) as response_2:
                full_data = response_2.read().decode("utf-8")  # 讀取該文章的響應數據

            root_2 = bs4.BeautifulSoup(full_data, "html.parser")  # 使用 BeautifulSoup 解析文章內容的 HTML

            span_title = root_2.find("span",string = "標題")  # 查找標題
            if span_title != None:
                title = span_title.next_sibling.string
                article_dict["title"] = str(title)  # 將標題存入字典中

            like = root_2.find_all("span",string = "推 ")  # 查找推文
            article_dict["like"] = str(len(like))  # 獲取推文數量並存入字典中

            dislike = root_2.find_all("span",string = "噓 ")  # 查找噓文
            article_dict["dislike"] = str(len(dislike))  # 獲取噓文數量並存入字典中

            span_time = root_2.find("span",string = "時間")  # 查找時間信息
            if span_time != None:
                time = span_time.next_sibling.string
                article_dict["time"] = str(time)  # 將時間信息存入字典中
                article_list.append(article_dict)  # 將該文章的信息字典添加到文章列表中
        
    next_url = "https://www.ptt.cc" + root.find("a", string = "‹ 上頁")["href"]  # 獲取下一頁的 URL
    return next_url

article_list = []  # 創建空列表，用於存儲所有文章的信息
count = 0
while count < 3:  # 循環獲取多個頁面的文章信息
    URL = get_data(URL)  # 獲取下一頁的 URL
    count += 1

header = ["title", "like", "dislike", "time"]  # 定義 CSV 文件的列標題
with open(f"article.csv", 'w') as file:  # 打開 CSV 文件並寫入文章信息
    writer = csv.DictWriter(file, fieldnames=header)
    for row in article_list:
        writer.writerow(row)  # 將每篇文章的信息寫入 CSV 文件中
