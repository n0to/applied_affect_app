FROM tiangolo/uvicorn-gunicorn:python3.8
LABEL maintainer="nishant@noto.ai"

RUN apt-get update && apt-get install -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN mkdir -p /usr/src/applied_affect_app
WORKDIR /usr/src/applied_affect_app
COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./app .