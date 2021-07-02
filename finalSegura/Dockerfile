FROM python:3.9


RUN pip install Django~=2.2.4
RUN pip install mysql-connector-python
RUN pip install PyMySQL
RUN pip install mysqlclient
RUN pip install gunicorn
RUN pip install cryptography
RUN pip install requests

ENV llave=""
ENV bdName=""
ENV bdUser="root"
ENV bdPassword=""
ENV bdHost=""
ENV bdPort="3306"

RUN mkdir /code
RUN mkdir /start

COPY ./run.sh /start

WORKDIR /code

RUN chmod +x /start/run.sh


CMD /start/run.sh