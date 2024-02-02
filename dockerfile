FROM python

WORKDIR /usr/src/app

COPY requirement* ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "uvicorn", "src",".main",":app", "--reload", "--port 8080" ]
