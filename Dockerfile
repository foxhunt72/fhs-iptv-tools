FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip install . && pip install -r requirements-dev.txt
#docker build -t fhs-test
ENTRYPOINT ["/usr/local/bin/fhs-iptv-tools"]
# docker buildx build --platform linux/arm64,linux/amd64 --tag foxhunt72/fhs-iptv-tools:latest --tag foxhunt72/fhs-iptv-tools:0.8.12 .
