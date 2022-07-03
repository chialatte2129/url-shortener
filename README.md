需在有Docker與docker-compose的環境執行
docker-compose up -d
確定
docker ps
確定service有正常啟動

docker exec -ti <container_id> python init_db.py
將資料庫初始化

docker-compose down
停止服務