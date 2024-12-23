@echo off

docker build . -t dss.com
docker run -p 80:8000 dss.com