FROM centos:latest
RUN dnf clean all && rm -r /var/cache/dnf && dnf upgrade -y dnf  update -y & echo hostname
RUN dnf  install -y python3-pip 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["avito_hw1.py"] 
