#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import Utils
import grp
import os
import pwd
import signal
import socket
import tarfile
import tempfile
import time
import urllib2
import yaml
from resource_management import Script, User, Group, Execute
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status


class ElasticSearchService(Script):
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
        Logger.info("ElasticSearch install completed")
        # configure
        self.configure(env)

    def start(self, env, upgrade_type=None):
        import params
        if env is not None:
            env.set_params(params)
        # configure
        self.configure(env)
        cmd = "%s -d -p %s" % (params.elasticSearchMainCmd, params.elasticSearchPidFile)
        Logger.info("Start: %s" % cmd)
        Execute(cmd, user=params.elasticSearchUser)
        time.sleep(10)

    def stop(self, env, upgrade_type=None):
        import params
        if env is not None:
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

    def status(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        time.sleep(5)
        check_process_status(params.elasticSearchPidFile)

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        if env is not None:
            env.set_params(params)
        self.__createSiteConfig()
        self.__createJvmOptionFile()
        self.__prepareDirectory()
        Logger.info("configure over")

    def __cleanPreviousInstallation(self):
        self.__cleanLogPath()
        self.__cleanPidFile()
        self.__cleanInstallationHome()

    def __cleanInstallationHome(self):
        import params
        esHome = params.elasticSearchHome
        esHomeRealPath = os.path.realpath(esHome)
        Logger.info("Remove %s" % esHomeRealPath)
        if os.path.exists(esHome):
            os.unlink(esHome)
        Utils.remove(esHomeRealPath)
        Logger.info("Remove %s" % esHome)
        Utils.remove(esHome)

    def __cleanLogPath(self):
        import params
        Logger.info("Remove Log Path: %s" % params.elasticSearchLogPath)
        Utils.cleanDir(params.elasticSearchLogPath)

    def __cleanPidFile(self):
        import params
        Logger.info("Remove PID file: %s" % params.elasticSearchPidFile)
        Utils.remove(params.elasticSearchPidFile)

    def __createGroupIfNotExist(self):
        import params
        try:
            grp.getgrnam(params.elasticSearchGroup)
        except Exception:
            Logger.info(
                "Group: %s not existed, create it" % params.elasticSearchGroup)
            Group(params.elasticSearchGroup)
            Logger.info(
                "Group: %s create successful" % params.elasticSearchGroup)

    def __createUserIfNotExist(self):
        import params
        try:
            pwd.getpwnam(params.elasticSearchUser)
        except Exception:
            Logger.info(
                "User: %s not existed, create it" % params.elasticSearchUser)
            User(params.elasticSearchUser,
                 gid=params.elasticSearchGroup,
                 groups=[params.elasticSearchGroup],
                 ignore_failures=True
                 )
            Logger.info(
                "User: %s create successful" % params.elasticSearchUser)

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
            tar.extract(name, path=os.path.dirname(elasticSearchRealPath))
        tar.close()
        if os.path.exists(params.elasticSearchHome):
            os.unlink(params.elasticSearchHome)
        os.symlink(elasticSearchRealPath, params.elasticSearchHome)
        Logger.info("Extract installation file: %s" % params.elasticSearchHome)
        Utils.remove(installationFile)
        for x in [elasticSearchRealPath, params.elasticSearchHome]:
            Utils.chown(x, params.elasticSearchUser, params.elasticSearchGroup)

    def __prepareDirectory(self):
        import params
        for name in [params.elasticSearchDataPath, params.elasticSearchLogPath,
                     os.path.dirname(params.elasticSearchPidFile)]:
            if not os.path.exists(name):
                os.makedirs(name, mode=0o755)
            Utils.chown(name, params.elasticSearchUser,
                        params.elasticSearchGroup)

    def __createSiteConfig(self):
        import params

        configs = {}
        for k, v in params.elasticSearchSite.iteritems():
            if Utils.isBooleanString(v):
                configs[k] = Utils.toBoolean(v)
            else:
                configs[k] = v
        hostname = socket.gethostname()
        isMasterNode = hostname in params.elasticSearchMasterHosts
        configs["node.name"] = hostname
        if isMasterNode:
            if params.masterIsDatanode:
                configs["node.roles"] = ['data','master']
                
        else:
            configs["node.roles"] = ['data']
        configs["path.data"] = params.elasticSearchDataPath
        configs["path.logs"] = params.elasticSearchLogPath
        elastic_search_data_hosts = params.elasticSearchDataHosts if hasattr(params, 'elasticSearchDataHosts') else []
        if elastic_search_data_hosts and len(elastic_search_data_hosts) > 0:
            configs["discovery.seed_hosts"] = list(
                set(params.elasticSearchMasterHosts + elastic_search_data_hosts))
        else:
            configs["discovery.seed_hosts"] = list(set(params.elasticSearchMasterHosts))
        if params.serviceVersion and params.serviceVersion >= "7.0.0":
            configs["cluster.initial_master_nodes"] = params.elasticSearchMasterHosts
        fin = open(params.elasticSearchConfigFile, "w")
        fin.write(yaml.safe_dump(configs, encoding='utf-8', allow_unicode=True, default_flow_style=False,
                                 explicit_start=True))
        fin.close()
        Utils.chown(params.elasticSearchConfigFile, params.elasticSearchUser, params.elasticSearchGroup)

    def __createJvmOptionFile(self):
        import params
        configs = {}
        for k, v in params.elasticSearchJvm.iteritems():
            configs[k] = v
        for k, v in params.elasticSearchEnv.iteritems():
            configs[k] = v
        content = params.elasticSearchJvmTemplateContent
        for k, v in configs.iteritems():
            content = content.replace("{{%s}}" % k, v)
        fin = open(params.elasticSearchJvmOptionsFile, "w")
        fin.write(content)
        fin.close()
        Utils.chown(params.elasticSearchConfigFile, params.elasticSearchUser,
                    params.elasticSearchGroup)
        
if __name__ == "__main__":
    service = ElasticSearchService()
    service.execute()
