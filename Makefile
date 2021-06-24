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

run-scheduler:
	docker-compose -f docker-compose.scheduler.yml up -d

end-scheduler:
	docker-compose -f docker-compose.scheduler.yml down

# dev
build-dev-image:
	docker build -f Dockerfile.dev -t lottery_crawler:latest .

run-dev-mysql:
	docker-compose -f docker-compose.db.dev.yml up -d

end-dev-mysql:
	docker-compose -f docker-compose.db.yml domn

run-dev-scheduler:
	docker-compose -f docker-compose.scheduler.dev.yml up -d

end-dev-scheduler:
	docker-compose -f docker-compose.scheduler.dev.yml down