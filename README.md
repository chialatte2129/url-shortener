# URL Shortener 短網址服務

一個基於Flask，利用sqlite、Redis實現的短網址服務。並透過Docker解決不同環境下的佈署問題。


## 環境需求

需在有Docker與docker-compose的環境執行



## 佈署服務

將專案拉到local
```
git pull https://github.com/chialatte2129/url-shortener.git
```
進入專案資料夾
```
cd url-shortener
```
編輯.env設定
```
nano .env
```

.env的內容如下
```env
DEBUG=False
SECRET_KEY=ABCDEFGHIJKLMNOPQUSTUVWXYZ
```
啟動服務
```
docker-compose up -d
```

確定service有正常啟動

```
docker ps
```

首次啟動將資料庫初始化
```
docker exec -ti <container_id> python init_db.py
```

停止服務
```
docker-compose down
```
