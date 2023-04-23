# Hawkeye
Hawkeye is a tool to support to visualize the code graph.

## How to use by docker
### x86_64
Start the Hawkeye daemon with the following command. This command also update the Hawkeye to the most recent version from github.
```
$ docker-compose --file ./docker/x86_64/docker-compose.yml up
```

Stop the Hawkeye daemon with following command.
```
$ docker-compose --file ./docker/x86_64/docker-compose.yml down -d
```

### arm64
Start the Hawkeye daemon with the following command. This command also update the Hawkeye to the most recent version from github.
```
$ docker-compose --file ./docker/arm64/docker-compose.yml up
```

Stop the Hawkeye daemon with following command.
```
$ docker-compose --file ./docker/arm64/docker-compose.yml down -d
```

## How to use in local
### Pre-requisites
1. Install python3 (recommended version: 3.11.2)
2. Install python packages
    1. ```$ sudo apt-get install python3-cairocffi libcairo2 libcairo2-dev```
    2. ```$ pip3 install -r requirements.txt```
3. Install node.js (recommended version: 12.22.12)
4. Install node.js packages
    1. ```$ cd web```
    2. ```$ npm install```

### Run
Use following command to run hawkeye server
```
$ python3 ./hawkeye.py
```
