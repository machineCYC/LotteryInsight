# LotteryInsight

## Environment setting

    1. setup python env (must install pipenv pyenv)
        - pipenv --python /home/**username**/.pyenv/versions/3.6.9/bin/python3.6 shell

    2. sync python library
        - pipenv sync

    3. create .env file
        - python genenv.py

    4. setting environment variable in .env file

## Local develop setup

    1. create local mysql server
        - make run-dev-mysql

    2. develop the crawler in LotteryInsight/crawlers folder

    If you want to try regular crawler data, you can try step 3
    3. create local scheduler
        - make build-dev-image
        - make run-dev-scheduler

    4. If complete develop, please end up mysql server and scheduler.

        close mysql server
        - make end-dev-mysql

        close scheduler
        - make end-dev-scheduler
