FROM python:3

RUN mkdir /opt/app && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install flask

COPY basicserver.py /opt/app

EXPOSE 5000/tcp

CMD ["/opt/venv/bin/python", "/opt/app/basicserver.py"]
