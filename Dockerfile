# ベースイメージの指定
FROM python:3.9-alpine3.13
# メンテナー
LABEL maintainer=""

# ログのリアルタイム表示
ENV PYTHONUNBUFFERED 1

# 必要なファイルをコンテナにコピー
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

# 依存関係のインストール
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # 隔離された環境: 仮想環境を使用することで、コンテナ内のPythonパッケージがシステム全体に影響を与えることなく隔離されます。
    # これにより、依存関係の競合を防ぎ、クリーンな環境を保つことができます。
    # バージョン管理の簡素化: 各プロジェクトごとに異なるPythonパッケージのバージョンを管理しやすくなります。
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # 柔軟な構成: 環境変数（ここではDEV）に基づいて、開発依存関係や本番依存関係を条件付きでインストールできます。s
    # これにより、同じDockerfileを使って異なる環境を構築することができます。
    # 効率的なビルド: 必要な依存関係だけをインストールすることで、イメージのサイズやビルド時間を最小限に抑えることができます。
    rm -rf /tmp && \
    # イメージサイズの削減: 不要なファイル（ここでは/tmp）を削除することで、最終的なイメージサイズを小さイメージサイズの削減: 
    # 不要なファイル（ここでは/tmp）を削除することで、最終的なイメージサイズを小さくできます。これにより、デプロイメントや配布が効率的になります。
    # セキュリティの向上: 不要なファイルを削除することで、潜在的なセキュリティリスクを減らすことができます。
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
    # 非特権ユーザーの作成

ENV PATH="/py/bin:$PATH"

USER django-user
