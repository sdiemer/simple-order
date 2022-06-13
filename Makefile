DOCKER_IMAGE_NAME ?= django-docker-dev
PROJECT_PORT ?= 8500

lint:
ifndef IN_FLAKE8
	docker run -v ${CURDIR}:/apps registry.ubicast.net/docker/flake8:latest make lint_python
else
	flake8 .
endif

deadcode:
ifndef IN_VULTURE
	docker run -v ${CURDIR}:/apps registry.ubicast.net/docker/vulture:latest make deadcode
else
	vulture --exclude docker/,submodules/ --min-confidence 90 --ignore-names user_modified,hints,fk_name,modeladmin,perm,perm_list,startloc .
endif

test:
ifndef DOCKER
	docker run --rm -e "PYTEST_ARGS=${PYTEST_ARGS}" -v ${CURDIR}:/opt/src ${DOCKER_IMAGE_NAME} make test
else
	pytest --reuse-db --cov=simple_order ${PYTEST_ARGS}
endif

run:
ifndef DOCKER
	docker run --rm -it -e DOCKER=1 -v ${CURDIR}:/opt/src -p ${PROJECT_PORT}:${PROJECT_PORT} ${DOCKER_IMAGE_NAME} make run
else
	bash docker/prepare.sh
	python3 simple_order/manage.py runserver 0.0.0.0:${PROJECT_PORT}
endif

shell:
ifndef DOCKER
	docker run --rm -it -e DOCKER=1 -v ${CURDIR}:/opt/src -p ${PROJECT_PORT}:${PROJECT_PORT} ${DOCKER_IMAGE_NAME} make shell
else
	bash docker/prepare.sh
	bash
endif

django_shell:
ifndef DOCKER
	docker run --rm -it -e DOCKER=1 -v ${CURDIR}:/opt/src ${DOCKER_IMAGE_NAME} make django_shell
else
	bash docker/prepare.sh
	python3 simple_order/manage.py shell
endif

django_makemigrations:
ifndef DOCKER
	docker run --rm -it -e DOCKER=1 -v ${CURDIR}:/opt/src ${DOCKER_IMAGE_NAME} make django_makemigrations
else
	bash docker/prepare.sh
	python3 simple_order/manage.py makemigrations
endif
