FROM python:3.8-slim

COPY . /src/

RUN apt-get update

WORKDIR /src

RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload"]

