FROM python:3.9

WORKDIR /my_docker/
RUN pip3 install pylint
ENTRYPOINT ["sh", "-c", "pylint $FILE > /report/report.txt"]
CMD ["/bin/bash"]
