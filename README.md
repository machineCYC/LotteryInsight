# LotteryInsight

## 環境設定

    VERSION=DEV python genenv.py

## build images

    docker build -f Dockerfile -t lottery_crawler:latest .

## run local mysql db

    docker-compose -f docker-compose.db.yml up
    docker-compose -f docker-compose.db.yml down

## run scheduler

    docker-compose -f docker-compose.scheduler.yml up
    docker-compose -f docker-compose.scheduler.yml down