# Use the latest Ubuntu for image
#FROM ubuntu:latest
FROM pytorch/pytorch:latest

# Runa  system update & Install python3 and pip3
RUN apt-get update && apt-get install -y python3 \
	python3-pip

RUN apt-get install -y libtinfo-dev

# Install jupyter
RUN pip3 install jupyter

# install Numpy
RUN pip3 install numpy

# install Pandas
RUN pip3 install pandas

# Install Matplotlib
RUN pip3 install matplotlib

# Install Seaborn
RUN pip3 install seaborn

# Install Sklearn
RUN pip3 install sklearn

# Install Tensorflow
#RUN pip3 install tensorflow

# Install pytorch
#RUN pip3 install torch torchvision
#RUN pip3 install torch torchvision -f https://download.pytorch.org/whl/torch_stable.html

# Install simpletransformers
RUN pip3 install simpletransformers

# Create a new system user
#RUN useradd -ms /bin/bash tirads_user

# Change to this new user
#USER tirads_user

# Set the container working directory to the user home folder
#WORKDIR /home/tirads_user
WORKDIR /

# Start the jupyter notebook
#ENTRYPOINT ["jupyter", "notebook", "--ip=*"]

# Follow the next steps 
	# BUILD - docker build . -t tirads
	# Search Images: docker images
	# Create a volume - docker volume create --name notebooks
	# RUN Jupyter:
		# First close all notebooks: jupyter-notebook stop 8888
		# Then run: docker run -it -d -v notebooks:/home/jupyter -p 8888:8888 image_id 
		# This will execute on background and give a token, like: a8ef2ef249d3fcf36ce895b06e3856527ddd5f24a5f0078ef1e516c1e128cca7
		# search for running containers: docker ps 
		# stop containers - docker stop container_name
		# remove -d to run on terminal, not on background
		# run terminal: docker exec -it <container> /bin/bash

