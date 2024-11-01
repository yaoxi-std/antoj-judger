FROM python:3.13

ADD . /opt/antoj-judger

WORKDIR /opt/antoj-judger

RUN pip install -r requirements.txt

CMD ["python3", "-m", "main"]
