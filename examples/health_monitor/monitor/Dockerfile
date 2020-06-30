FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY data ./
COPY spark_monitors.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "spark_monitors.py"]