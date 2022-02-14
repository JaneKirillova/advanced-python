FROM python:3.8
WORKDIR /workdir
COPY main.py main.py
RUN mkdir -p /workdir/artifacts
RUN apt-get update
RUN python3 -m pip install pydot
RUN apt-get -y install graphviz
RUN python3 -m pip install networkx
RUN python3 -m pip install thebestastlibrary
RUN apt-get install -y texlive

CMD python3 /workdir/main.py