FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY voting_planner.py ./

ENTRYPOINT ["python", "voting_planner.py"]