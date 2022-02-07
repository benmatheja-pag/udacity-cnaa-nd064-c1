FROM python:3.8-slim-buster

EXPOSE 3111/tcp

WORKDIR /techtrends

COPY techtrends/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY techtrends/ .
RUN python3 init_db.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=3111"]