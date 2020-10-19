#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

from resource_management import Script
import os
import socket

config = Script.get_config()
config = {
    "ambariLevelParams": {
        "java_home": "/Library/Java/JavaVirtualMachines/jdk1.8.0_162.jdk/Contents/Home/"
    },
    "elasticsearch-env": {
        "elasticsearch.download.url": "http://hdp.cydw.xyz/elasticsearch-7.5.0.tar.gz",
        "elasticsearch.user": "admin",
        "elasticsearch.group": "admin",
        "elasticsearch.home": "/Users/admin/Configuration/elasticsearch",
        "elasticsearch.data.path": "/Users/admin/Configuration/elasticsearch-data",
        "elasticsearch.log.path": "/Users/admin/Configuration/elasticsearch-logs",
        "elasticsearch.pid.file": "/Users/admin/Configuration/elasticsearch.pid"
    },
    "elasticsearch-site": {"transport.bind_host": "0.0.0.0",
                           "discovery.zen.ping.unicast.hosts": [
                               "node1.cydw.xyz"],
                           "cluster.initial_master_nodes": ["node1.cydw.xyz"],
                           "network.host": "0.0.0.0",
                           "transport.host": "0.0.0.0",
                           "path.data": "/mnt/home/admin/cydw-dev/data/es7",
                           "http.cors.allow-origin": "*", "node.master": True,
                           "path.logs": "/mnt/home/admin/cydw-dev/logs/es7",
                           "node.data": True, "http.port": 19700,
                           "cluster.name": "cydw",
                           "transport.tcp.port": "19710-19720",
                           "xpack.security.enabled": False,
                           "transport.tcp.compress": True,
                           "http.cors.enabled": True,
                           "node.name": "node1.cydw.xyz"}
}
elasticSearchMasterHosts = config["clusterHostInfo"]["elasticsearch_master_hosts"]
elasticSearchDataHosts = config["clusterHostInfo"]["elasticsearch_data_hosts"]
javaHome = config["ambariLevelParams"]["java_home"]

elasticSearchEnv = config["elasticsearch-env"]
elasticSearchSite = config["elasticsearch-site"]
elasticSearchJvm = config["elasticsearch-jvm"]
elasticSearchDownloadUrl = elasticSearchEnv["elasticsearch.download.url"]
elasticSearchUser = elasticSearchEnv["elasticsearch.user"]
elasticSearchGroup = elasticSearchEnv["elasticsearch.group"]
elasticSearchHome = elasticSearchEnv["elasticsearch.home"]
elasticSearchDataPath = elasticSearchEnv["elasticsearch.data.path"]
elasticSearchLogPath = elasticSearchEnv["elasticsearch.log.path"]
elasticSearchPidFile = elasticSearchEnv["elasticsearch.pid.file"]
elasticSearchTmpDir = elasticSearchEnv["elasticsearch.tmp.path"]
elasticSearchConfigDir = os.path.join(elasticSearchHome, "config")
elasticSearchConfigFile = os.path.join(elasticSearchConfigDir,
                                       "elasticsearch.yml")
elasticSearchJvmOptionsFile = os.path.join(elasticSearchConfigDir, "jvm.options")
elasticSearchJvmTemplateContent = elasticSearchJvm["jvm.options.template"]
elasticSearchBinDir = os.path.join(elasticSearchHome, "bin")
elasticSearchMainCmd = os.path.join(elasticSearchBinDir, "elasticsearch")
elasticSearchHttpPort = elasticSearchSite["http.port"]