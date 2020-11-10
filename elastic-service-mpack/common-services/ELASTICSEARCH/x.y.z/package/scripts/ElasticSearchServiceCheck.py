#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import time
import sys
import urllib2
import json

from resource_management import Script
from resource_management.core.logger import Logger

class ElasticSearchServiceCheck(Script):

    def service_check(self, env):
        import params
        env.set_params(params)
        time.sleep(5)

        health_url = "http://{0}:{1}/_cluster/health?wait_for_status=green&timeout=120s".format(params.hostname, params.elasticSearchHttpPort)
        fd = urllib2.urlopen(health_url)
        content = fd.read()
        fd.close()
        result = json.loads(content)
        status = result["status"] == u"green"
        if not status:
            Logger.warning("Elasticsearch service check failed")
            sys.exit(1)
        else:
            Logger.info("Elasticsearch service check successful")
            sys.exit(0)

if __name__ == "__main__":
    ElasticSearchServiceCheck().execute()
