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

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|
| Count     | 0.5397796630859375 | 0.7538795471191406 | N/A | **0.42247772216796875** |
| Max       | 28.344392776489258 | 19.478797912597656 | **5.789756774902344** |17.70329475402832 |
| Min       | **2.321958541870117**  | 17.937660217285156 | 4.972934722900391 |17.675399780273438 |
| Mean      | **3.7069320678710938** | 21.35443687438965  | 7.592678070068359|19.426345825195312|
| Std       | 133.02135467529297 | 40.7567024230957   | **19.84882354736328** |34.93976593017578 |
| The best movies in 1995, 2000 and 2005        | 11188.719749450684 | 39.910316467285156   | N/A | **25.78258514404297**|
| The worst movies in 1995, 2000 and 2005       | 974.2720127105713 | 20.278215408325195   | N/A |**16.7996883392334** |
| left join    | 4847.801923751831 / 1155.2624702453613 | 27.64296531677246 / 3.9191246032714844 |N/A | ** 20.226478576660156/ 2.2802352905273438** |
| inner join    | 215.77215194702148 / 222.059965133667 | 99.89643096923828 / 1.132965087890625 |N/A | **3.950834274291992/ 0.946044921875** |
| outer join    | 3724.7469425201416 / 4067.2049522399902 | 112.32447624206543 / 32.66310691833496 |N/A | **87.63790130615234/ 25.241374969482422** |
| right join    | 5529.9012660980225 / 3916.3753986358643 | 1.2564659118652344 / 16.813278198242188 |N/A | **1.13463401794433/ 10.601043701171875** |


* 10M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|
| Count     | 0.5795955657958984 | 0.6728172302246094 | N/A |**0.4508495330810547**|
| Max       | **33.93745422363281** | 196.3639259338379 | 49.19314384460449|244.6448802947998 |
| Min       | **8.50057601928711**  | 196.85602188110352 | 49.22342300415039|243.7267303466797 |
| Mean      | **10.051250457763672** | 217.09084510803223  |68.26043128967285 |255.8584213256836|
| Std       | **133.38470458984375** | 582.9811096191406 | 341.1288261413574|579.0176391601562 |
| The best movies in 1995, 2000 and 2005        | 8745.709419250488 | 244.94028091430664 |  N/A |**208.56070518493652** |
| The worst movies in 1995, 2000 and 2005       | 7552.948713302612 | 213.67120742797852 |  N/A |**169.39544677734375** |
| left join    | 35910.73250770569 /  1380.5065155029297 | 341.91274642944336 / 143.42331886291504 |  N/A |**255.90252876281738 / 87.09359169006348**|
| inner join    | 273.6356258392334 / 282.37247467041016 | 93.76001358032227 / 97.05257415771484 |  N/A |**78.53984832763672 / 75.11520385742188** |
| outer join    | 34739.8464679718 / 34726.06563568115 | 2181.725025177002 / 669.980525970459 |  N/A |**1798.2358932495117 / 530.4086208343506** |
| right join    |52969.77210044861 / 34624.85861778259  | 94.64144706726074 / 311.7403984069824 |  N/A |**78.76896858215332 / 242.91491508483887**|

* 20M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|
| Count     | **0.6260871887207031** | 0.7033348083496094 | N/A | 1.4688968658447266|
| Max       | **39.650917053222656** | 392.64726638793945 |95.60108184814453|1923.2287406921387 |
| Min       | **15.261411666870117** | 394.0465450286865 |95.96395492553711|1921.8406677246094 |
| Mean      | **15.659332275390625** | 433.16197395324707 | 133.6658000946045|371.43754959106445|
| Std       | **150.43091773986816** | 910.8619689941406 | 535.1519584655762|971.7750549316406|
| The best movies in 1995, 2000 and 2005        | 16591.485023498535 | 484.8752021789551   | N/A | **373.29959869384766** |
| The worst movies in 1995, 2000 and 2005       | 15012.631416320 | 421.0529327392578   | N/A | **334.3355655670166** |
| left join    | 69988.08264732361 / 1484.544277191162 | 669.6755886077881 / 247.11060523986816 | N/A | **501.79409980773926 / 173.57945442199707** |
| inner join    | 344.5172309875488 /  366.119384765625 | 190.80686569213867 /  190.71674346923828 | N/A | **151.2315273284912 / 150.09188652038574** |
| outer join    | 69034.65151786804 /  69001.08456611633 | 6426.183700561523 / 1354.7029495239258 | N/A | **5081.736087799072 / 1059.216022491455** |
| right join    | 105703.47046852112 /  68888.84925842285  | 189.69488143920898 / 617.1934604644775 | N/A | **151.99518203735352 / 479.142427444458** |

* 100M items:

| Operation | PyGDF (p2.xlarge)  | Pandas (p2.xlarge) | Pandas optimized (p2.xlarge) | Pandas (c4.4xlarge) |
|-----------|--------------------|--------------------|------------------------------|---------------------|
| Count     | **0.4909038543701172** | 0.5466938018798828 | N/A | ERROR |
| Max       | **80.27124404907227** | 2051.4168739318848 | 498.00944328308105 |ERROR|
| Min       | **55.30118942260742** | 2054.2919635772705 | 514.9331092834473 | ERROR|
| Mean      | **54.63266372680664** | 2288.846969604492 | 697.965145111084 | ERROR|
| Std       | **248.6863136291504** | 6193.148612976074 | 2772.050380706787 | ERROR|
| The best movies in 1995, 2000 and 2005        | 84433.31599235535 | **2477.0567417144775**   | N/A | ERROR|
| The worst movies in 1995, 2000 and 2005       | 79118.32404136658 | **2178.0457496643066**   | N/A | ERROR|
| left join    | ERROR | **3831.214666366577 / 1330.929517745971** | N/A | ERROR |
| inner join    | ERROR | **1074.42307472229 / 1053.316354751587** | N/A | ERROR |
| outer join    | ERROR | **38308.51697921753 / 7404.616355895996** | N/A | ERROR |
| right join    | ERROR | **1046.5500354766846 / 3419.306516647339** | N/A | ERROR |


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
