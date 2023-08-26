FROM python:3.12.0b4-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

CMD [ "python", "./run.py" ]