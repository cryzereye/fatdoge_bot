FROM python:3.8.16-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "module/main.py"]