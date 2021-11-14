# GPA網站刷評論神器 ProxySpammer

## ★★★★★(網站已經改版，無法使用)★★★★★
## 簡介 Introduction
一開始修了某教授的課，但是因為教授不給交作業，所以打算去GPA網站按不喜歡的評價，經過研究後發現網站一個IP(token)只能進行一次評價，所以想到可以**透過Proxy API不斷取得新的IP(new token)來進行重複刷評價的動作**，主要應用request套件和Proxy API實現，重複使用過的Proxy也會被記錄下來到本地的txt檔(可重置)。

-  Proxy API: https://www.proxyscan.io/
-  GPA課程搜尋頁面:https://gpa.ntustexam.com/

----------------------------------------

## 環境設定 Environment
- 1.開發環境:**Python 3.7.8**
- 2.終端機執行 ```pip install -r requirements.txt``` 安裝會使用到的套件
- 3.使用工具:
    * 解析HTML物件:```beautifulsoup4==4.10.0```
    * 請求網站資料:```requests==2.25.1```    

----------------------------------------
## 網站研究 Research
經過研究網站封包傳遞發現，評論是透過訪問網頁評論API所觸發，觀察**封包傳輸方式採用POST，封包內部資料主要包含token、id，token必須由搜尋該課程搜尋頁面取得，id為該課程的編號，且不能直接訪問目標課程頁面，必須要先經過課程搜尋頁面再進入搜尋結果頁面觸發網頁評論API**，直接訪問目標課程頁面會被拒絕訪問(HTTP 403 Forbidden)。

- 網頁訪問流程: **課程搜尋面頁->搜尋結果頁面**
- 網頁評論API封包傳輸方式: **POST**
- token: **課程搜尋頁面會提供(似乎依IP而不同)**
- id: **手動點擊一次評論觀察封包可以發現課程id(數字)**
----------------------------------------
## 運作過程 Operation
- ### 程式流程圖
    - 初始條件:**必須先取得課程id**
    - 終止條件:**Proxy API無法提供新的Proxy Server**

    ![](https://i.imgur.com/IwNTb5f.png)

----------------------------------------

## 成果 Result
- **成功**評論返回**success**
- **重複**返回**duplicated**
- **失敗**返回**failed**

![](https://i.imgur.com/JXxuPBH.png)