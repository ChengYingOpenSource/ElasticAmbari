#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import sys
import os
import glob
import pwd
import grp
import signal
import time
import tarfile
import shutil
import json
import logging
from resource_management import Script
import Utils

class ElasticSearchBaseService(Script):
    def install(self, env):
        import params
        env.set_params(params)

    def __cleanPreviousInstallation(self):
        self.__cleanPreviousInstallation()

        pass

    def __cleanInstallationHome(self):
        import params
        esHome = params.es_home
        esHomeRealPath = os.path.realpath(esHome)
        logging.warn("Remove %s" % esHomeRealPath)
        Utils.remove(esHomeRealPath)
        logging.warn("Remove %s" % esHome)
        Utils.remove(esHome)

    def __cleanLogPath(self, logPath):
        logging.warn("Remove Log Path: %s" % logPath)
        Utils.cleanDir(logPath)

    def __cleanPidFile(self, pidFile):
        logging.warn("Remove PID file: %s" % pidFile)
        Utils.remove(pidFile)

