FROM python:3.9.5

ADD requirements.txt /requirements.txt

ADD main.py /main.py

ADD okteto-stack.yaml /okteto-stack.yaml

ADD Dockerfile /Dockerfile

RUN pip install -r requirements.txt

EXPOSE 8080

COPY ./app /app

CMD ["python3", "main.py"]
