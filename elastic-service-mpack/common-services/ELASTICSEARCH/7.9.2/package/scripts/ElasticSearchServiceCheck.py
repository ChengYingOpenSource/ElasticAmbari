#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import time

from resource_management import check_process_status, Script

class ServiceCheck(Script):
    
    def service_check(self, env):
        import params
        env.set_params(params)
        time.sleep(5)
        check_process_status(params.elasticSearchPidFile)
        
if __name__ == "__main__":
    ServiceCheck().execute()
