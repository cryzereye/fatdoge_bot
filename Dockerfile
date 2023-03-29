FROM python:3.8.16-bullseye
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "module/main.py"]