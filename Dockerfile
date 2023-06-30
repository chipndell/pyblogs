FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /socialpost
WORKDIR /socialpost
COPY requirements.txt /socialpost/
RUN pip install -r requirements.txt
COPY . /socialpost/
