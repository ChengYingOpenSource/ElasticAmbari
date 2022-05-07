# 问题列表

1. 执行`yum install xmlstarlet`没有找到软件包 

> centos下默认没有xmlstarlet的源，需要添加源地址
```
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

2. 执行`make`报错1：
```
ImportError: No module named setuptools
```

> centos7下默认使用python2.7，且没有安装pip，使用以下命令安装

```bash
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
python get-pip.py
```

3. 执行`make`报错2：
```
gcc: error: yaml/_yaml.c: No such file or directory
gcc: fatal error: no input files
```

> pyyaml依赖Cython编译c文件，故需要安装Cython

```bash
pip install Cython
```

4. 执行`make`报错3：
```
yaml/_yaml.h:2:18: fatal error: yaml.h: No such file or directory
```

> 缺失库文件libyaml-devel

```bash
yum install -y libyaml-devel
```

5. 执行`make`卡在`git clone https://github.com/yaml/pyyaml.git`
> 由于mpack依赖pyyaml修改yaml配置文件，在make的过程中下载pyyaml源码速度太慢，我修改了make文件的`https://github.com/yaml/pyyaml.git` 为 `https://gitee.com/mirrors/pyyaml.git`

6. 如果整体比较慢，可以试试我fork到gitee的地址
```bash
git clone https://gitee.com/he1992/ElasticAmbari.git
```

# 最终依赖环境安装命令
````bash
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
python get-pip.py && \
rm -rf get-pip.py && \
pip install Cython && \
yum install -y make xmlstarlet libyaml-devel
````