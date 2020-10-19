#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

from resource_management import Script
import os
import json
import logging

config = Script.get_config()
logging.info(json.dumps(config))
elasticSearchMasterHosts = config["clusterHostInfo"]["elasticsearch_master_hosts"]
elasticSearchDataHosts = config["clusterHostInfo"]["elasticsearch_data_hosts"]
javaHome = config["ambariLevelParams"]["java_home"]

elasticSearchEnv = config["configurations"]["elasticsearch-env"]
elasticSearchSite = config["configurations"]["elasticsearch-site"]
elasticSearchJvm = config["configurations"]["elasticsearch-jvm"]
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
