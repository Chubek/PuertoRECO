FROM continuumio/miniconda:latest

WORKDIR /home/reco_app

COPY . ./


RUN apt-get update && apt-get install build-essential libsvm-dev -y

RUN conda update -n base -c defaults conda

RUN chmod +x boot.sh

RUN conda env create -f environment.yml


RUN echo "source activate reco3" > ~/.bashrc
ENV PATH /opt/conda/envs/reco3/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"] 