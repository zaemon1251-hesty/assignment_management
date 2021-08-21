## assignment_management
moodleで提示された課題を取得して管理するアプリです


## quick start
1. docker-composeで環境構築
```sh
$ docker-compose build --no-cache 
$ docker-compose up -d 
```
2. appコンテナの中に入り、データベースをつくる
```bash
$ docker-compose exec app bash
# cd model
# python models.py
# cd ..(appに戻る)
```
3. 実行する
```sh
# python app.py main
```
