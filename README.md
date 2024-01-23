# URL Shortener Service

A URL shortener service based on `Flask`, implemented using `bootstrap`, `sqlite` and `Redis`. Deployment across different environments is facilitated through `Docker`.

<div align="center">
	<img width="80" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/>
	<img width="80" src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png" alt="Flask" title="Flask"/>
	<img width="80" src="https://user-images.githubusercontent.com/25181517/182884894-d3fa6ee0-f2b4-4960-9961-64740f533f2a.png" alt="redis" title="redis"/>
	<img width="80" src="https://user-images.githubusercontent.com/25181517/183898054-b3d693d4-dafb-4808-a509-bab54cf5de34.png" alt="Bootstrap" title="Bootstrap"/>
	<img width="80" src="https://github.com/marwin1991/profile-technology-icons/assets/136815194/82df4543-236b-4e45-9604-5434e3faab17" alt="SQLite" title="SQLite"/>
</div>

## Features

1. Submit url to get shorter URL
<p align="center" width="100%">
    <img width="70%" src="/public/main_page.png"> 
</p>

2. Show redirection url list
<p align="center" width="100%">
    <img width="70%" src="/public/short_url_list.png"> 
</p>

3. Analyzed of each url
<p align="center" width="100%">
    <img width="70%" src="/public/url_analyze.png"> 
</p>

## Caching

For optimal operational efficiency, we minimize database reads during redirection by first checking for records in the redis cache. If not found, we proceed with a database query. For logging, we utilize a Redis Queue, processed by a separate thread, ensuring real-time responses.

<p align="center" width="100%">
    <img width="70%" src="/public/URL_Shorterner.drawio.png"> 
</p>

## Environment Requirements

Execution requires an environment with Docker and docker-compose.

## Service Deployment

1. Clone the project from the server to your local environment:

```sh
git clone https://github.com/chialatte2129/url-shortener.git
```

2. Enter the project folder

```sh
cd url-shortener
```

3. Edit the `.env` configuration. For Windows environments, you can use Notepad

```sh
nano .env
```

4. Fill in the `.env` file with the following content:

```env
DEBUG=False
SECRET_KEY=MY_SECRET_KEY
```

5. Use `docker-compose` to start the service:

```sh
docker-compose up -d
```

6. Ensure that the docker container has started successfully, and copy the `container id`

```sh
docker ps
```

7. After the first startup, perform database initialization. Replace `<your_container_id>` with the container id copied in the previous step:

```sh
docker exec -ti <your_container_id> python init_db.py
```

8. The server runs at http://127.0.0.1:5000/

9. To stop the server, run:

```sh
docker-compose down
```

## LICENCE

mit
