FROM python:3.8-slim
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update; apt-get install -y libgomp1; rm -rf /var/lib/apt/lists/*
RUN python -c "import cnocr; model = cnocr.CnOcr(model_name='conv-lite-fc')"
EXPOSE 80
ENV SLACK_BOT_PORT 80
CMD python main.py