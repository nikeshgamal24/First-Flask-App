FROM python:3.8-slim-buster

WORKDIR /WEB_SERVICE_ASSIGNMENT1

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
