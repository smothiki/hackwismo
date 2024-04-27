FROM python:3.11

ADD . /
RUN pip3 install -r requirements.txt
EXPOSE 7860
ENTRYPOINT [ "python","app.py" ]