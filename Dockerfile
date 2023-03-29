FROM python:3.10.10-windowsservercore-ltsc2022
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "module/main.py"]