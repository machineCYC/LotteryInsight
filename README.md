# LotteryInsight

## 環境設定

    VERSION=DEV python genenv.py

## build images

    docker build -f Dockerfile -t lottery_crawler:latest .
    docker build -f Dockerfile.cache -t lottery_crawler:dev .

## run local mysql db

    docker-compose -f docker-compose.db.yml up
    docker-compose -f docker-compose.db.yml down

## run scheduler

    docker-compose -f docker-compose.scheduler.yml up
    docker-compose -f docker-compose.scheduler.yml down

## push docker to dockerhub

    docker tag lottery_crawler:latest machinedockercyc/lotterydocker:latest
    docker push machinedockercyc/lotterydocker:latest