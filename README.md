# QuickPasteRedux
### A simple pastebin clone in python and [starlette](https://www.starlette.io)

![Licence](https://img.shields.io/github/license/CUB3D/QuickPasteRedux)

## Try it out
Current stable version -> [qp.cub3d.pw](https://qp.cub3d.pw)

## How to run
- Clone the repo: ```git clone https://github.com/CUB3D/QuickPasteRedux```
- Copy .env.default to .env and set the database uri
- Install the dependencies: ```pip install -r requirements.txt```
- Start the server: ```hypercorn app.main:app -c Hypercorn-DEV.toml --access-log - --error-log -```

## Running with docker-compose
```
version: '3'
services:
 quickpasteredux:
   container_name: Web
   build: .
   ports:
     - "8086:8080"
   volumes:
     - files:/home/code/files
   environment:
     DEBUG: "false"
     DATABASE_URL: <TODO>
   restart: unless-stopped
volumes:
 files:
```
