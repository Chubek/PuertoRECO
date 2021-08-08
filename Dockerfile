FROM continuumio/miniconda:latest

WORKDIR /home/docker_conda_template

COPY faceapp.py ./
COPY boot.sh ./
COPY scripts/ ./
COPY templates/ ./
COPY unit_tests/ ./
COPY .env ./
COPY codes_dict.py ./
COPY requirements.txt ./
COPY README.md ./
COPY main.py ./


RUN chmod +x boot.sh

RUN conda create -n reco3 python=3.9
RUN conda activate reco3
RUN pip install -r requirements.txt

RUN echo "source activate reco3" > ~/.bashrc
ENV PATH /opt/conda/envs/reco3/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"] 