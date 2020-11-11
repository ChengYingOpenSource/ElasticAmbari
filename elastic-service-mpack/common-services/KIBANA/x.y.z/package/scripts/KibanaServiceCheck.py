#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import time
import sys
import urllib2
import json

from resource_management import Script
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status

class KibanaServiceCheck(Script):

    def service_check(self, env):
        import params
        env.set_params(params)
        time.sleep(5)
        check_process_status(params.kibanaPidFile)
        Logger.info("Kibana service check successful")
        sys.exit(0)

if __name__ == "__main__":
    service = KibanaServiceCheck()
    service.execute()
