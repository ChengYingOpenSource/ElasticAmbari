#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import os
import signal
import socket
import tarfile
import tempfile
import time

import Utils
import grp
import pwd
import urllib2
import yaml
from resource_management import Script, User, Group, Execute
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status


class KibanaService(Script):
    def install(self, env):
        import params
        if env is not None:
            env.set_params(params)
        # do some clean     
        self.__cleanPreviousInstallation()
        # check and create group and user
        self.__createGroupIfNotExist()
        self.__createUserIfNotExist()
        self.__prepareDirectory()
        self.__extractInstallationFile(self.__downloadInstallationFile())
        Logger.info("Kibana install completed")
        # configure
        self.configure(env)

    def start(self, env, upgrade_type=None):
        import params
        if env is not None:
            env.set_params(params)
        # configure
        self.configure(env)
        if os.path.exists(params.kibanaLogFile):
            Utils.remove(params.kibanaLogFile)
        cmd = "nohup %s > /dev/null 2>&1 < /dev/null &" % (params.kibanaBinFile, )
        Logger.info("Start: %s" % cmd)
        Execute(cmd, user=params.kibanaUser)
        time.sleep(10)

    def stop(self, env, upgrade_type=None):
        import params
        if env is not None:
            env.set_params(params)
        if os.path.exists(params.kibanaPidFile):
            fin = open(params.kibanaPidFile, "r")
            pid = int(fin.read())
            fin.close()
            os.kill(pid, signal.SIGTERM)
            time.sleep(10)
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception as e:
                pass
            time.sleep(3)
        Utils.remove(params.kibanaPidFile)

    def status(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        time.sleep(5)
        check_process_status(params.kibanaPidFile)

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        if env is not None:
            env.set_params(params)
        self.__createSiteConfig()
        Logger.info("configure over")

    def __cleanPreviousInstallation(self):
        self.__cleanLogPath()
        self.__cleanPidFile()
        self.__cleanInstallationHome()

    def __cleanInstallationHome(self):
        import params
        kibanaHome = params.kibanaHome
        kibanaHomeRealPath = os.path.realpath(kibanaHome)
        Logger.info("Remove %s" % kibanaHomeRealPath)
        Utils.remove(kibanaHomeRealPath)
        Logger.info("Remove %s" % kibanaHome)
        Utils.remove(kibanaHome)

    def __cleanLogPath(self):
        import params
        Logger.info("Remove Log Path: %s" % params.kibanaLogPath)
        Utils.cleanDir(params.kibanaLogPath)

    def __cleanPidFile(self):
        import params
        Logger.info("Remove PID file: %s" % params.kibanaPidFile)
        Utils.remove(params.kibanaPidFile)

    def __createGroupIfNotExist(self):
        import params
        try:
            grp.getgrnam(params.kibanaGroup)
        except Exception:
            Logger.info(
                "Group: %s not existed, create it" % params.kibanaGroup)
            Group(params.kibanaGroup)
            Logger.info(
                "Group: %s create successful" % params.kibanaGroup)

    def __createUserIfNotExist(self):
        import params
        try:
            pwd.getpwnam(params.kibanaUser)
        except Exception:
            Logger.info(
                "User: %s not existed, create it" % params.kibanaUser)
            User(params.kibanaUser,
                 gid=params.kibanaGroup,
                 groups=[params.kibanaGroup],
                 ignore_failures=True
                 )
            Logger.info(
                "User: %s create successful" % params.kibanaUser)

    def __downloadInstallationFile(self):
        import params
        localFile = tempfile.NamedTemporaryFile(delete=False)
        instance = urllib2.urlopen(params.kibanaDownloadUrl)
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
        kibanaName = childNames[0]
        kibanaRealPath = os.path.join(os.path.dirname(params.kibanaHome), os.path.dirname(kibanaName))
        Utils.remove(kibanaRealPath)
        tar.close()
        cmd = "cd %s && tar zxf %s" % (os.path.dirname(params.kibanaHome), installationFile)
        Logger.info(cmd)
        os.system(cmd)
        if os.path.exists(params.kibanaHome):
            os.unlink(params.kibanaHome)
        os.symlink(kibanaRealPath, params.kibanaHome)
        Logger.info("Extract installation file: %s" % params.kibanaHome)
        Utils.remove(installationFile)
        for x in [kibanaRealPath, params.kibanaHome]:
            Utils.chown(x, params.kibanaUser, params.kibanaGroup)

    def __prepareDirectory(self):
        import params
        for name in [params.kibanaLogPath, os.path.dirname(params.kibanaPidFile)]:
            if not os.path.exists(name):
                os.makedirs(name, mode=0o755)
            Utils.chown(name, params.kibanaUser, params.kibanaGroup)

    def __createSiteConfig(self):
        import params

        configs = {}
        for k, v in params.kibanaSite.iteritems():
            if Utils.isBooleanString(v):
                configs[k] = Utils.toBoolean(v)
            else:
                configs[k] = v
        configs["elasticsearch.hosts"] = []
        for x in params.elasticSearchMasterHosts:
            configs["elasticsearch.hosts"].append("http://" + x + ":" + str(params.elasticSearchPort))
        configs["pid.file"] = params.kibanaPidFile
        configs["logging.appenders.file.fileName"] = params.kibanaLogFile
        configs["logging.root.appenders"] = ['default','file']
        fin = open(params.kibanaConfigFile, "w")
        fin.write(yaml.safe_dump(configs, encoding='utf-8', allow_unicode=True, default_flow_style=False,
                                 explicit_start=True))
        fin.close()
        Utils.chown(params.kibanaConfigFile, params.kibanaUser, params.kibanaGroup)

if __name__ == "__main__":
    service = KibanaService()
    service.execute()
