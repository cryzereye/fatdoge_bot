FROM python:3.10.7-windowsservercore-ltsc2022 as build
COPY . /app 
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [“python”, “module/main.py”]