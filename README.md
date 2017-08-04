# beeva-poc-pygdf
Proof of Concept with PyGDF at BEEVA

### Installation

#### Amazon Web Services EC2 instance and AMI

To use PyGDF we need a machine with NVIDIA graphic card and CUDA support, in this case I use an AWS EC2 instance to install PyGDF. Instance type is [p2.xlarge](https://aws.amazon.com/es/ec2/instance-types) based on a [Deep Learning AMI Ubuntu Version](https://aws.amazon.com/marketplace/pp/B06VSPXKDX). This type of AMI's **has a problem**, when you reboot or stop instance and start it again, CUDA drivers dissapears due to unattended upgrades. **To solves this** you should change upgrades configuration with steps below:

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

 I run the same code to proccess count, max, min, mean and std over the same dataset using Pandas an PyGDF framework.

 Dataset is a structure with information about users, movies and raiting that users assignt to each movie, see example below:
```
 user_id  movie_id  rating  timestamp
    1      1193       5  978300760
    1       661       3  978302109
    1       914       3  978301968
    1      3408       4  978300275
    1      2355       5  978824291
    1      1197       3  978302268
    1      1287       5  978302039
    1      2804       5  978300719
    1       594       4  978302268
    1       919       4  978301368
```

I grow up dataset each iteration from 1M of items to 100M of items

 These are experiments results time processing (ms) for each operation:

* 1M of items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) |
|-----------|--------------------|--------------------|
| Count     | **0.5397796630859375** | 0.7538795471191406 |
| Max       | 28.344392776489258 | **19.478797912597656** |
| Min       | **2.321958541870117**  | 17.937660217285156 |
| Mean      | **3.7069320678710938** | 21.35443687438965  |
| Std       | 133.02135467529297 | **40.7567024230957**   |


* 10M of items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) |
|-----------|--------------------|--------------------|
| Count     | **0.5795955657958984** | 0.6728172302246094 |
| Max       | **33.93745422363281** | 196.3639259338379 |
| Min       | **8.50057601928711**  | 196.85602188110352 |
| Mean      | **10.051250457763672** | 217.09084510803223  |
| Std       | **133.38470458984375** | 582.9811096191406 |

* 20M of items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) |
|-----------|--------------------|--------------------|
| Count     | **0.6260871887207031** | 0.7033348083496094 |
| Max       | **39.650917053222656** | 392.64726638793945 |
| Min       | **15.261411666870117** | 394.0465450286865 |
| Mean      | **15.659332275390625** | 433.16197395324707 |
| Std       | **150.43091773986816** | 910.8619689941406 |

* 100M of items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) |
|-----------|--------------------|--------------------|
| Count     | **0.4909038543701172** | 0.5466938018798828 |
| Max       | **80.27124404907227** | 2051.4168739318848 |
| Min       | **55.30118942260742** | 2054.2919635772705 |
| Mean      | **54.63266372680664** | 2288.846969604492 |
| Std       | **248.6863136291504** | 6193.148612976074 |


### Conclusions

- La desviación estándar es distinat, puede variar, hasta en las unidades

### Related Links
* [A little bit introduction to Pandas](https://jarroba.com/pandas-python-ejemplos-parte-i-introduccion/)
* [Pandas official docs](https://pandas.pydata.org/pandas-docs/stable/index.html)
* [A post by MapD of GPU Data Frame](https://www.mapd.com/blog/2017/05/30/end-to-end-on-the-gpu-with-the-gpu-data-frame-gdf/)
* [A description of CUDA and Parallel Processiong in GPUs](http://www.nvidia.es/object/cuda-parallel-computing-es.html)
* [Apache Arrow official website](https://arrow.apache.org/)
* [PyGDF repository in GitHub](https://github.com/gpuopenanalytics/pygdf)
* [PyGDF api reference](http://pygdf.readthedocs.io/en/latest/api.html)
* [Wiki about Gpu Data Frame and its libraries](https://github.com/gpuopenanalytics/libgdf/wiki)
* [MovieLens dataset website](https://grouplens.org/datasets/movielens/)
* [Article about efficient data transfer through zero copy](https://www.ibm.com/developerworks/library/j-zerocopy/)
* [AWS User Guide for Accelerated Computing Instances](http://docs.aws.amazon.com/es_es/AWSEC2/latest/UserGuide/accelerated-computing-instances.html)
