FROM python:3.12

WORKDIR /app

COPY src/requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

COPY src /app

EXPOSE 8080
CMD [ "python", "main.py" ]
