# FunBox Test task

![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white)
![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Testing

![pytest](https://img.shields.io/badge/pytest_asyncio-2496ED?style=for-the-badge&logo=pytest&logoColor=white)
![codecov](https://img.shields.io/codecov/c/github/Umbreella/funbox_test?style=for-the-badge&logo=codecov)

## Description

[Task Description](TaskDescription.pdf)

Completed items:

1. :white_check_mark: Written in Python version 3.7+
2. :white_check_mark: Provides a JSON API over HTTP
3. :white_check_mark: Provides two HTTP resources
    1. :white_check_mark: Download visits
    2. :white_check_mark: Getting statistics
4. :white_check_mark: Redis is used to store data
5. :white_check_mark: Code covered with tests

## Getting Started

### Dependencies

![redis_stack](https://img.shields.io/badge/redis_stack-DC382D?style=for-the-badge&logo=redis&logoColor=white)

### Environment variables

* To run the application:
    * add in **environment variables** path to **.env** file
    * overwrite **.env** file
* The list of all environment variables is specified in the **[.env](.env)**

## Docker

1. docker-compose.yml

```docker
version: "3"

services:
  funbox_test:
    image: umbreella/funbox_test:latest
    ports:
      - [your_open_port]:8000
    env_file:
      - [path_to_env_file]
```

* Docker-compose run

```commandline
docker-compose up -d
```

## Endpoints

* API docs

```commandline
[your_ip_address]/api/docs/
```
