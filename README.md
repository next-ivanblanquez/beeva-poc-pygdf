# beeva-poc-pygdf

## INDEX
* [Introduction](#introduction)
  * [Amazon Web Services EC2 instances and AMIs](#amazon-web-services-ec2-instances-and-amis)
  * [PyGDF and Miniconda ecosystem](#pygdf-and-miniconda-ecosystem)
* [Installation](#installation)
* [Experiments](#experiments)
* [Conclusions](#conclusions)
* [References](#references)

### Introduction
Proof of Concept with PyGDF at BEEVA.

Comparison between Pandas and PyGDF,performance behavior at the same processes over the same dataset.

### Installation

#### Amazon Web Services EC2 instances and AMIs

To use PyGDF we need a machine with NVIDIA graphic card and CUDA support, in this case I use an AWS EC2 instance to install PyGDF. Instance type is [p2.xlarge](https://aws.amazon.com/es/ec2/instance-types) based on a [Deep Learning AMI Ubuntu Version](https://aws.amazon.com/marketplace/pp/B06VSPXKDX) and with CPU [Intel Xeon E5 2686 v4](http://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%20E5-2686%20v4.html).

On the other hand I tests Pandas code in AWS EC2 instance optimized to computing. Instance type is  [c4.4xlarge](https://aws.amazon.com/es/ec2/instance-types) based on a [Deep Learning AMI Ubuntu Version](https://aws.amazon.com/marketplace/pp/B06VSPXKDX) and with CPU [Intel Xeon E5 2666 v3](http://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%20E5-2666%20v3.html). I decided use the same software in both instances to get better results in the comparison.

This type of AMI's **has a problem**, when you reboot or stop instance and restart it again, CUDA drivers dissapears due to unattended upgrades. **To solves this** you should change upgrades configuration with steps below:

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


Now when you reboot or stop and reestart instances, if you run *"nvidia-smi"* command you can get information about GPU instead of a message saying that driver is not installed.

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

PyGDF needs Python and [Anaconda](https://www.continuum.io/), but you can use [Miniconda](https://github.com/conda/conda) instead.

Please follow these steps to complete de installation:
1. Clone pygdf code from github reposotiory:
```
  git clone https://github.com/gpuopenanalytics/pygdf.git (por https)
```  

2. Install Miniconda:
```
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
  bash Miniconda2-latest-Linux-x86_64.sh
```
  After this you need reboot terminal to apply changes into the path.

3. Make virtual enviroment. In folder when you clone pygdf run this code
```
  cd pygdf
  conda-env create --name pygdf_dev --file conda_environments/testing_py35.yml
```

4. Install PyGDF. And then, int the folder before, run code below:
```
  /home/ubuntu/miniconda2/envs/pygdf_dev/bin/python3.5 setup.py install
```

5. To activate and deactivate virtual enviroment run this code:
```
  source activate pygdf_dev
  source deactivate pygdf_dev
```


### Experiments

 I ran three blocks of operations through to dataset (you can get code [here](https://github.com/beeva-ivanblanquez/beeva-poc-pygdf/tree/master/code)):
 * **Statistical operations through columns** (Count, Maximum, Minimun, Mean and Standard deviation).
 * **Filter operations with conditions in two columns** (The best and the worst movies in years 1995, 2000 and 2005).
 * **Join operations between two datasets**. In this case at first, I run join on ratings and users where ratings size is always greater than users, and then I turn arround the join and use users at first dataset where users size always is less than ratings. I did it to campare behavior int different cases.

 I used two dataset that are structures with information about users, movies and rating that users assignt to each movie, see example below:
* users
```
 user_id    age    ocupation     zip
    1        1        10        48067
    2        56       16        70072
    3        25       15        55117
    4        45       7         02460
    5        25       20        55455
    6        50       9         55117
    7        35       1         06810
    8        25       12        11413
    9        25       17        61614
    10       35       1         95370
```
* Ratings
```
 user_id  movie_id  rating  timestamp
    1      1193       5     978300760
    1       661       3     978302109
    1       914       3     978301968
    1      3408       4     978300275
    1      2355       5     978824291
    1      1197       3     978302268
    1      1287       5     978302039
    1      2804       5     978300719
    1       594       4     978302268
    1       919       4     978301368
```

I grow up Ratings dataset each iteration from 1M items to 100M items.

You can downlad dataset here:
* [Users 60K](https://s3-eu-west-1.amazonaws.com/poc-pygdf/users.dat)
* [Ratings 1M](https://s3-eu-west-1.amazonaws.com/poc-pygdf/ratings-1M.dat)
* [Ratings 10M](https://s3-eu-west-1.amazonaws.com/poc-pygdf/ratings-10M.dat)
* [Ratings 20M](https://s3-eu-west-1.amazonaws.com/poc-pygdf/ratings-20M.dat)
* [Ratings 100M](https://s3-eu-west-1.amazonaws.com/poc-pygdf/ratings-100M.dat)

 These are experiments results time processing (milliseconds) for each operation. The best time of each of them is marked as bold:

* 1M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) | Pandas optimized (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|-------------------------------|
| Count     | 0.53 | 0.75 | N/A | **0.42** |N/A|
| Max       | 28.34 | 19.47 | 5.78 |17.70 |**5.00**|
| Min       | **2.32**  | 17.93 | 4.97 |17.67 |4.59|
| Mean      | **3.70** | 21.35  | 7.59|19.42|6.22|
| Std       | 133.02 | 40.75   | 19.84 |34.93 |**16.32**|
| The best movies in 1995, 2000 and 2005        | 11188.71 | 39.91   | N/A | **25.78**|N/A|
| The worst movies in 1995, 2000 and 2005       | 974.27 | 20.27   | N/A |**16.79** |N/A|
| left join    | 4847.80 / 1155.26 | 27.64 / 3.91 |N/A | ** 20.22/ 2.28** |N/A|
| inner join    | 215.77 / 222.05 | 99.89 / 1.13 |N/A | **3.95/ 0.94** |N/A|
| outer join    | 3724.74 / 4067.20 | 112.32 / 32.66 |N/A | **87.63/ 25.24** |N/A|
| right join    | 5529.90 / 3916.37 | 1.25 / 16.81 |N/A | **1.13/ 10.60** |N/A|


* 10M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) | Pandas optimized (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|-------------------------------|
| Count     | 0.57 | 0.67 | N/A |**0.45**| N/A |
| Max       | **33.93** | 196.36 | 49.19|244.64 |41.73|
| Min       | **8.50**  | 196.85 | 49.22|243.72 |41.00|
| Mean      | **10.05** | 217.09  |68.26 |255.85|57.57|
| Std       | **133.38** | 582.98 | 341.12|579.01 |232.28|
| The best movies in 1995, 2000 and 2005        | 8745.70 | 244.94 |  N/A |**208.56** | N/A |
| The worst movies in 1995, 2000 and 2005       | 7552.94 | 213.67 |  N/A |**169.39** | N/A |
| left join    | 35910.73 /  1380.50 | 341.91 / 143.42 |  N/A |**255.90 / 87.09**| N/A |
| inner join    | 273.63 / 282.37 | 93.76 / 97.05 |  N/A |**78.53 / 75.11** | N/A |
| outer join    | 34739.84 / 34726.06 | 2181.72 / 669.98 |  N/A |**1798.23 / 530.40** | N/A |
| right join    |52969.77 / 34624.85  | 94.64 / 311.74 |  N/A |**78.76 / 242.91**| N/A |

* 20M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) | Pandas optimized (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|-------------------------------|
| Count     | **0.62** | 0.70 | N/A | 1.46| N/A |
| Max       | **39.65** | 392.64 |95.60|1923.22 |77.62|
| Min       | **15.26** | 394.04 |95.96|1921.84 |76.93|
| Mean      | **15.65** | 433.16 | 133.66|371.43|99.55|
| Std       | **150.43** | 910.86 | 535.15|971.77|357.86|
| The best movies in 1995, 2000 and 2005        | 16591.48 | 484.87   | N/A | **373.29** | N/A |
| The worst movies in 1995, 2000 and 2005       | 15012.63 | 421.05   | N/A | **334.33** | N/A |
| left join    | 69988.08 / 1484.54 | 669.67 / 247.11 | N/A | **501.79 / 173.57** | N/A |
| inner join    | 344.51 /  366.11 | 190.80 /  190.71 | N/A | **151.23 / 150.09** | N/A |
| outer join    | 69034.65 /  69001.08 | 6426.18 / 1354.70 | N/A | **5081.73 / 1059.21** | N/A |
| right join    | 105703.47 /  68888.84  | 189.69 / 617.19 | N/A | **151.99 / 479.14** | N/A |

* 100M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) | Pandas optimized (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|-------------------------------|
| Count     | **0.49** | 0.54 | N/A | ERROR | N/A |
| Max       | **80.27** | 2051.41 | 498.01|ERROR|ERROR |
| Min       | **55.30** | 2054.29 | 514.93 | ERROR| ERROR|
| Mean      | **54.63** | 2288.84 | 697.96 | ERROR| ERROR|
| Std       | **248.68** | 6193.14 | 2772.05 | ERROR|ERROR |
| The best movies in 1995, 2000 and 2005        | 84433.31 | **2477.05**   | N/A | ERROR|  N/A |
| The worst movies in 1995, 2000 and 2005       | 79118.32 | **2178.04**   | N/A | ERROR| N/A |
| left join    | ERROR | **3831.21 / 1330.92** | N/A | ERROR | N/A |
| inner join    | ERROR | **1074.42 / 1053.31** | N/A | ERROR | N/A |
| outer join    | ERROR | **38308.51 / 7404.61** | N/A | ERROR | N/A |
| right join    | ERROR | **1046.55 / 3419.30** | N/A | ERROR | N/A |


### Select/Where

* Operations:
  * 1: timestamp >= 788918400
  * 2: timestamp >= 788918400 and timestamp <= 820454399
  * 3: (timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199)
  * 4: (timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)
  * 5: ((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)
  * 1B: timestamp >= 820454400
  * 2B: timestamp >= 820454400 or timestamp <= 852076799
  * 3B: (timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199)
  * 4B: (timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)
  * 5B: ((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)


* 1M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|---------------------|
| 1 | 775.43|37.80 | **31.00**|
| 2 | 147.23 | 25.78| **21.00**|
| 3 | 154.73|27.15 |**23.00** |
| 4 | 156.65| 31.89 | **26.00**|
| 5 |163.54 | 27.07| **23,00** |
| 1B |144.91 | 23.20| **19.00**|
| 2B |146.99 | 24.84| **21.00** |
| 3B | 149.31| 13.75| **12.00**|
| 4B | 158.22 | 19.70 | **14.00**|
| 5B | 164.84| 21.50| **16.00**|


* 10M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|---------------------|
| 1 |849.13|434.88|**377.00**|
| 2 |**166.98**|426.40|364.00|
| 3 |156.68|182.32|**152.00**|
| 4 |**167.73**|260.66|214.00|
| 5 |**174.29**|239.22|190.00|
| 1B |**160.72**|392.97|328.00|
| 2B |**163.47**|426.63|364.00|
| 3B |**162.91**|195.87|165.00|
| 4B |**167.08**|269.15|230.00|
| 5B |**173.22**|291.76|245.00|


* 20M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|---------------------|
| 1 |890.03|821.89|**696.00**|
| 2 |**207.19**|834.24|706.00|
| 3 |**180.39**|344.05|276.00|
| 4 |**191.03**|506.25|404.00|
| 5 |**192.17**|451.71|354.00|
| 1B |**205.48**|762.90|643.00|
| 2B |**205.81**|848.63|705.00|
| 3B |**182.26**|383.43|316.00|
| 4B |**189.74**|513.58|411.00|
| 5B |**206.36**|554.27|442.00|


### Conclusions

As you can read [here](https://www.mapd.com/blog/2017/05/30/end-to-end-on-the-gpu-with-the-gpu-data-frame-gdf/), GPU Data Frame is thinking and designed for manage data in GPU-side and avoid intercommunicate through GPU-PCI-CPU. Maybe this is the main advantage of this project. Using Pandas we can found some advantages and some disadvantage, I talk about them in each of three scenarios:

* **Statistical operations through columns**
  * GDF implements [Apache Arrow](https://arrow.apache.org/) specification allocating data in columns, so processes looping through columns are faster using PyGDF than using Pandas (between 5 and 20 times faster), except when data size is small, because time to transfer data from disk to gpu is greater than time to process these data. The more data there is, the more difference.


* **Filter/Select Where queries**
  * In this case, when you need process rows PyGDF behavior is very slow, and always process is faster using instance computing optimized (proof for data with 100M of items is not posible to run in c4.4xlarge instance because there is not enough memory to load data). The difference is between 40 and 60 times faster in Pandas (more with dataset is small) and this difference remains stable


* **Joins**
  * I ran two different proofs here, when join a dataset small with bigger one and the opposite case.
  * In all cases Pandas running in computing optimized instances is faster than PyGDF between 3 and 4800 times.
  * Pandas is faster than PyGDF and very very faster in left, outer and right join.
  * Pandas still fater than PyGDF but when dataset growing up that difference decreases specially in inner and left join (when size(A) < size(B)).


* **Other Considerations**
  * PyGDF is faster than Pandas in columnar operations.
  * PyGDF has less operations set than Pandas, and you need Pandas or Numpy to load data, doe not load data directly.
  * PyGDF is still in beta phase, there ar not a release (will be released on september), so there is not a community to follow this project yet and is not easy to install.
  * PyGDF neither has not a complete examples or a good documentation of all features.
  * PyGDF only accepts numerical data.
  * PyGDF is not a tool for replace Pandas and improve performance.
  * I think main benefit of GDF is to mantain dataset in GPU scope and work with other tools in this scope
  * Next step shoul be a PoC using MapD,GDF and H2.io as indicatee in [this. post](https://devblogs.nvidia.com/parallelforall/goai-open-gpu-accelerated-data-analytics/).

### References
* [A little bit introduction to Pandas](https://jarroba.com/pandas-python-ejemplos-parte-i-introduccion/)
* [Pandas official docs](https://pandas.pydata.org/pandas-docs/stable/index.html)
* [A Beginner’s Guide to Optimizing Pandas Code for Speed](https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6)
* [What is GPU Computing](http://www.nvidia.es/object/gpu-computing-es.html)
* [Post by MapD of GPU Data Frame](https://www.mapd.com/blog/2017/05/30/end-to-end-on-the-gpu-with-the-gpu-data-frame-gdf/)
* [Description of CUDA and Parallel Processiong in GPUs](http://www.nvidia.es/object/cuda-parallel-computing-es.html)
* [Example of how GDF Accelerate data analytics](https://devblogs.nvidia.com/parallelforall/goai-open-gpu-accelerated-data-analytics/)
* [NVIDIA Tesla homepage](http://www.nvidia.es/object/tesla-high-performance-computing-es.html)
* [Apache Arrow official website](https://arrow.apache.org/)
* [PyGDF repository in GitHub](https://github.com/gpuopenanalytics/pygdf)
* [PyGDF api reference](http://pygdf.readthedocs.io/en/latest/api.html)
* [Wiki about Gpu Data Frame and its libraries](https://github.com/gpuopenanalytics/libgdf/wiki)
* [MovieLens dataset website](https://grouplens.org/datasets/movielens/)
* [Article about efficient data transfer through zero copy](https://www.ibm.com/developerworks/library/j-zerocopy/)
* [AWS User Guide for Accelerated Computing Instances](http://docs.aws.amazon.com/es_es/AWSEC2/latest/UserGuide/accelerated-computing-instances.html)
