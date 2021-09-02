## assignment_management
moodleで提示された課題を取得して管理するアプリです

## 初期設定
1. docker-composeで環境構築
```sh
$ docker-compose build
$ docker-compose up -d 
```


## web-server を立ち上げる手順
1. ホストOSで http://localhost:80 アクセスする（上手くいかない場合、もう一度1の手順を繰り返すといいかも）

## 標準的な機能を試す手順

1. コンテナにログインし実行する
```sh
$ docker-compose exec app
# python service.py main
```
