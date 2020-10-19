#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import os
import pwd
import grp
import signal
import time
import tarfile
import logging
import tempfile
import urllib2
import yaml
from resource_management import Script, User, Group, Execute, Template
import Utils


class ElasticSearchBaseService(Script):
    def install(self, env):
        import params
        env.set_params(params)
        # do some clean     
        self.__cleanPreviousInstallation()
        # check and create group and user
        self.__createGroupIfNotExist()
        self.__createUserIfNotExist()
        self.__prepareDirectory()
        self.__extractInstallationFile(self.__downloadInstallationFile())
        logging.info("ElasticSearch install completed")

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        cmd = "%s -d -p %s" % (
        params.elasticSearchMainCmd, params.elasticSearchPidFile)
        logging.info("Start: %s" % cmd)
        Execute(cmd, user=params.elasticSearchUser)
        time.sleep(10)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        if os.path.exists(params.elasticSearchPidFile):
            fin = open(params.elasticSearchPidFile, "r")
            pid = int(fin.read())
            fin.close()
            os.kill(pid, signal.SIGTERM)
            time.sleep(10)
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception as e:
                pass
            time.sleep(3)
        Utils.remove(params.elasticSearchPidFile)
        
    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)
        self.__createSiteConfig()
        self.__createJvmOptionFile()

    def __cleanPreviousInstallation(self):
        self.__cleanLogPath()
        self.__cleanPidFile()
        self.__cleanInstallationHome()

    def __cleanInstallationHome(self):
        import params
        esHome = params.elasticSearchHome
        esHomeRealPath = os.path.realpath(esHome)
        logging.warn("Remove %s" % esHomeRealPath)
        Utils.remove(esHomeRealPath)
        logging.warn("Remove %s" % esHome)
        Utils.remove(esHome)

    def __cleanLogPath(self):
        import params
        logging.warn("Remove Log Path: %s" % params.elasticSearchLogPath)
        Utils.cleanDir(params.elasticSearchLogPath)

    def __cleanPidFile(self):
        import params
        logging.warn("Remove PID file: %s" % params.elasticSearchPidFile)
        Utils.remove(params.elasticSearchPidFile)

    def __createGroupIfNotExist(self):
        import params
        try:
            grp.getgrnam(params.elasticSearchGroup)
        except Exception:
            logging.info(
                "Group: %s not existed, create it" % params.elasticSearchGroup)
            Group(params.elasticSearchGroup)
            logging.info(
                "Group: %s create successful" % params.elasticSearchGroup)

    def __createUserIfNotExist(self):
        import params
        try:
            pwd.getpwnam(params.elasticSearchUser)
        except Exception:
            logging.info(
                "User: %s not existed, create it" % params.elasticSearchUser)
            User(params.elasticSearchUser,
                 gid=params.elasticSearchGroup,
                 groups=[params.elasticSearchGroup],
                 ignore_failures=True
                 )
            logging.info(
                "User: %s create successful" % params.elasticSearchGroup)

    def __downloadInstallationFile(self):
        import params
        localFile = tempfile.NamedTemporaryFile(delete=False)
        instance = urllib2.urlopen(params.elasticSearchDownloadUrl)
        blockSize = 8192
        while True:
            buffer = instance.read(blockSize)
            if not buffer:
                break
            localFile.write(buffer)
        localFile.close()
        return localFile.name

    def __extractInstallationFile(self, installationFile):
        import params
        tar = tarfile.open(installationFile)
        childNames = tar.getnames()
        elasticSearchName = childNames[0]
        elasticSearchRealPath = os.path.join(os.path.dirname(params.elasticSearchHome), elasticSearchName)
        Utils.remove(elasticSearchRealPath)
        for name in tar.getnames():
            tar.extract(name, path = os.path.dirname(elasticSearchRealPath))
        tar.close()
        os.symlink(elasticSearchRealPath, params.elasticSearchHome)
        logging.info("Extract installation file: %s" % params.elasticSearchHome)
        Utils.remove(installationFile)

    def __prepareDirectory(self):
        import params
        for name in [params.elasticSearchDataPath, params.elasticSearchLogPath]:
            if os.path.exists(name):
                continue
            os.makedirs(name, mode=0755)
            Utils.chown(name, params.elasticSearchUser,
                        params.elasticSearchGroup)
            
    def __createSiteConfig(self):
        import params
        
        configs = {}
        for k, v in params.config["elasticsearch-site"].iteritems():
            configs[k] = v
        configs["path.data"] = params.elasticSearchDataPath
        configs["path.logs"] = params.elasticSearchLogPath
        fin = open(params.elasticSearchConfigFile, "w")
        fin.write(yaml.dump(configs))
        fin.close()
        Utils.chown(params.elasticSearchConfigFile, params.elasticSearchUser, params.elasticSearchGroup)
        
    def __createJvmOptionFile(self):
        import params
        configs = {}
        for k, v in params.elasticSearchJvm.iteritems():
            configs[k] = v
        jvmOptionsContent = Template(params.elasticSearchJvmTemplateContent, configurations = configs)
        fin = open(params.elasticSearchConfigFile, "w")
        fin.write(jvmOptionsContent)
        fin.close()
        Utils.chown(params.elasticSearchConfigFile, params.elasticSearchUser,
                    params.elasticSearchGroup)
        
    

if __name__ == '__main__':
    service = ElasticSearchBaseService()
    service.install(None)
