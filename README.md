# beeva-poc-pygdf
Proof of Concept with PyGDF at BEEVA

### Installation

#### Amazon Web Services EC2 instances and AMI

To use PyGDF we need a machine with NVIDIA graphic card and CUDA support, in this case I use an AWS EC2 instance to install PyGDF. Instance type is [p2.xlarge](https://aws.amazon.com/es/ec2/instance-types) based on a [Deep Learning AMI Ubuntu Version](https://aws.amazon.com/marketplace/pp/B06VSPXKDX). This type of AMI's *has a problem*, when you reboot or stop instance and start it again, CUDA drivers dissapears due to unattended upgrades. *To solves this* you should change upgrades configuration with steps below:

```
sudo vim /etc/apt/apt.conf.d/20auto-upgrades
```

And change file content for this one:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "0";
```


```
sudo vim /etc/apt/apt.conf.d/10periodic
```

And change file content for this one:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
```


Now when you reboot or stop and reestar instances, if you run nvidia-smi command you can get information about GPU instead of a message saying that driver is not installed

```
nvidia-smi -q | head

==============NVSMI LOG==============

Timestamp                           : Thu Aug  3 10:01:15 2017
Driver Version                      : 375.66

Attached GPUs                       : 1
GPU 0000:00:1E.0
  Product Name                    : Tesla K80
  Product Brand                   : Tesla
```


#### PyGDF and Miniconda ecosystem

PyGDF needs a Python and [Anaconda](https://www.continuum.io/), but you can use [Miniconda](https://github.com/conda/conda) instead.

Please follow these steps to complete de installation:
1. Clone pygdf code form github reposotiory:
```
  git clone https://github.com/gpuopenanalytics/pygdf.git (por https)
```  

2. Install Miniconda:
```
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
  bash Miniconda2-latest-Linux-x86_64.sh
```
  After this you need reboot terminal to apply changes into the path

3. Make virtual enviroment. In folder when you clone pygdf run this code
```
  cd pygdf
  conda-env create --name pygdf_dev --file conda_environments/testing_py35.yml
```

4. Install PyGDF. In the same folder before run:
```
  /home/ubuntu/miniconda2/envs/pygdf_dev/bin/python3.5 setup.py install
```

5. To activate and deactivate virtual enviroment run this code:
```
  source activate pygdf_dev
  source deactivate pygdf_dev
```






### Experiments


### Conclusions
