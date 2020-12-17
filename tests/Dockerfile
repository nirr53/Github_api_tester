FROM python:3.7
WORKDIR /tests
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install pytest, requests
RUN ["pytest", "-v", "test_*.py"]
CMD tail -f /dev/null
