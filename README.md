# URL Shortener 短網址服務

一個基於Flask，利用sqlite、Redis實現的短網址服務。並透過Docker解決不同環境下的佈署問題。


## 環境需求

需在有Docker與docker-compose的環境執行



## 佈署服務

將專案從Server拉到本機環境
```
git clone https://github.com/chialatte2129/url-shortener.git
```
進入專案資料夾
```
cd url-shortener
```
編輯.env設定
```
nano .env
```

.env檔填寫如下內容
```env
DEBUG=False
SECRET_KEY=MY_SECRET_KEY
```
使用docker-compose啟動服務
```
docker-compose up -d
```

確定docker container有正常啟動
```
docker ps
```

首次啟動後，將資料庫初始化
```
docker exec -ti <your_container_id> python init_db.py
```
服務會啟在 http://127.0.0.1:5000/

停止服務
```
docker-compose down
```
