FROM openjdk:slim
COPY --from=python:3.7 / /

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY data ./data
COPY spark_monitors.py ./

ENTRYPOINT ["python", "spark_monitors.py"]