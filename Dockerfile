FROM python:3.8.16-bullseye
WORKDIR /fatdoge_bot
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "module/main.py"]