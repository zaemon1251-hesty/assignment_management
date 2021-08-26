# assignment_management
moodleで提示された課題を取得して管理するアプリです

## 初期設定
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
```

## web-server を立ち上げる手順
1. ホストOSで http://localhost:80 アクセスする（上手くいかない場合、もう一度初期設定の1を繰り返すといいかも）

## 標準的な機能を試す手順
1. 実行する
```sh
$ docker-compose exec app bash
# python service.py main
```
