## assignment_management

提示された課題を取得して管理するアプリです。

- 課題が掲載されているサイトをスクレイピングして情報を取得
- 課題の追加、管理
- メールによる課題のリマインダ
- ユーザーごとに管理

https://github.com/iktakahiro/dddpy を参考に クリーンアーキテクチャに従った設計に挑戦しています。
現在は WebAPI の開発途中です。

## 今後の計画

- React & TypeScript でフロント部分を作る
- 単位取得状況を受け取って卒業できるかどうか判定する機能の追加
- Google Calender API の連携（課題やリマインダーのデータを DB ではなく google calender で管理）
- CI&CD 環境構築

## 関係するライブラリや技術など

- poetry
- docker
- FastAPI
- postgresql
- sqlalchemy
- Nginx
- JWT
- selenium
- aws (以前 Amazon ECS Fargate で本番環境を構築してみましたが、使用料が超高かったので、どこで本番環境を構築するか模索中です)

## サーバー を立ち上げる手順

1. docker-compose で環境構築

```sh
$ docker-compose build (--no-cache)
$ docker-compose up -d
```

3. ホスト OS で http://localhost/docs アクセスする（上手くいかない場合、もう一度 1 の手順を繰り返すといいかも）
