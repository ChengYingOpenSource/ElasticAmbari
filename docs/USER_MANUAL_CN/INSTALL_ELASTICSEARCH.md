# 安装ElasticSearch服务

## 选择安装ElasticSearch服务

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9gu15gbj223k13otgq.jpg)

## 选择Master节点

可以选择多个节点

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9ijuiorj223013847d.jpg)

## 选择Data节点

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9jgh4avj224w0ratdf.jpg)

## 修改相关配置

### `elasticsearch-env`：基本的属性

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9musnx4j21c60j6whc.jpg)

其中的`ElasticSearch Download Url`是ElasticSearch的tar包下载地址。

ElasticSearch安装包可以是自己修改优化过的版本，或者是已经集成好分词插件版。

常用插件地址：

https://github.com/medcl/elasticsearch-analysis-pinyin

https://github.com/medcl/elasticsearch-analysis-ik

当前可以自己下载对应版本插件，解压到 elasticsearch/plugins 目录下，再打包成自己的 elasticsearch 安装包，其它插件也如此。 后续也会增加自定义插件灵活安装、升级、卸载操作。

### `elasticsearch-site`：ElasticSearch的基本配置

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9pvx5h2j21ei0tqwhq.jpg)

### `elasticsearch-jvm`：ElasticSearch的JVM配置

![](https://tva1.sinaimg.cn/large/703708dcly1gjwqvf73l4j21jw0g0q4l.jpg)

## 完成安装

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9sm64jzj223q100jxu.jpg)

![](https://tva1.sinaimg.cn/large/703708dcly1gjw9tmipz6j226w0mowit.jpg)