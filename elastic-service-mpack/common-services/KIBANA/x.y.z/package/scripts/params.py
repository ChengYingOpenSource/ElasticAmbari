#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import os

from resource_management import Script

config = Script.get_config()
hostname = config['agentLevelParams']['hostname']
elasticSearchMasterHosts = config["clusterHostInfo"]["elasticsearch_master_hosts"]
elasticSearchPort = config["configurations"]["elasticsearch-site"]["http.port"]

kibanaEnv = config["configurations"]["kibana-env"]
kibanaDownloadUrl = kibanaEnv["kibana.download.url"]
kibanaUser = kibanaEnv["kibana_user"]
kibanaGroup = kibanaEnv["kibana_group"]
kibanaHome = kibanaEnv["kibana.home"]
kibanaLogPath = kibanaEnv["kibana.log.path"]
kibanaLogFile = os.path.join(kibanaLogPath, "kibana.log")
kibanaPidFile = kibanaEnv["kibana.pid.file"]

kibanaConfigDir = os.path.join(kibanaHome, "config")
kibanaConfigFile = os.path.join(kibanaConfigDir, "kibana.yml")
kibanaBinDir = os.path.join(kibanaHome, "bin")
kibanaBinFile = os.path.join(kibanaBinDir, "kibana")

kibanaSite = config["configurations"]["kibana-site"]
kibanaServerPort = config["server.port"]
