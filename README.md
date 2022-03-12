## assignment_management
moodleで提示された課題を取得して管理するアプリです

## web-server を立ち上げる手順
1. docker-composeで環境構築
```sh
$ docker-compose build --no-cache 
$ docker-compose up -d 
```
2. appコンテナの中に入り、データベースと管理者ユーザーをつくる
```bash
$ docker-compose exec app-server bash
# cd model
# python models.py
```
3. ホストOSで http://localhost:80 アクセスする（上手くいかない場合、もう一度1の手順を繰り返すといいかも）
