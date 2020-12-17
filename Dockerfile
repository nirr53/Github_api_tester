FROM python:3.7
WORKDIR /tests
COPY * /tests
#RUN pip3 install -r requirements.txt
RUN pip3 install pytest
RUN pip3 install requests
RUN pip3 install configparser
RUN ["pytest", "-v", "-s"]
CMD tail -f /dev/null
