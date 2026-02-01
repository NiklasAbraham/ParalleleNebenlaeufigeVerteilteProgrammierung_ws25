FROM python:3.9-slim
RUN pip install flask
COPY server.py /app/server.py
WORKDIR /app
CMD ["python", "server.py"]