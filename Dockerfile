FROM python:3.8-slim
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update; apt-get install -y libgomp1; rm -rf /var/lib/apt/lists/*
EXPOSE 80
ENV PORT 80
CMD python main.py