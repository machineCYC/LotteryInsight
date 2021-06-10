build-latest-image:
	docker build -f Dockerfile -t lottery_crawler:latest .

tag-latest-image:
	docker tag lottery_crawler:latest machinedockercyc/lottery_crawler:latest

push-latest-image:
	docker push machinedockercyc/lottery_crawler:latest

login-dockerhub:
	echo "$PASSWORD" | docker login -u machinedockercyc --password-stdin

logout-dockerhub:
	docker logout

build-image: login-dockerhub build-latest-image tag-latest-image push-latest-image logout-dockerhub
