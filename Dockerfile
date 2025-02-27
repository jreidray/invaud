FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
VOLUME /data
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "start:app"]