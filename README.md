# Hawkeye

## Pre-requisites
1. Install python3 (recommended version: 3.11.2)
2. Install python packages
    1. ```$ sudo apt-get install python3-cairocffi libcairo2 libcairo2-dev```
    2. ```$ pip3 install -r requirements.txt```
3. Install node.js (recommended version: 12.22.12)
4. Install node.js packages
    1. ```$ cd web```
    2. ```$ npm install```

## How to use in local
Use following command to run hawkeye server
```
$ python3 ./hawkeye.py
```

## How to use by docker
In case of x86_64,

```
$ docker build ./docker/x86_64
$ docker run -p 3000-3001:3000-3001 -it <docker ID>
```
