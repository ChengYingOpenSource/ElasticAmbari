#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

from resource_management import Script
import os
import json
import socket

config = Script.get_config()
javaHome = config["ambariLevelParams"]["java_home"]

elasticSearchEnv = config["elasticsearch-env"]
elasticSearchDownloadUrl = elasticSearchEnv["elasticsearch_download_url"]
elasticSearchUser = elasticSearchEnv["elasticsearch_user"]
elasticSearchGroup = elasticSearchEnv["elasticsearch_group"]
elasticSearchHome = elasticSearchEnv["elasticsearch_home"]
elasticSearchDataPath = elasticSearchEnv["elasticsearch_data_path"]
elasticSearchLogPath = elasticSearchEnv["elasticsearch_log_path"]
elasticSearchPidFile = elasticSearchEnv["elasticsearch_pid_file"]

