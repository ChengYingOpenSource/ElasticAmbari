#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import os
import shutil
import urllib2

def chown(path, uid, gid):
    if os.path.isdir(path):
        for root, dirnames, filenames in os.walk(path):
            for dirname in dirnames:
                os.chown(os.path.join(root, dirname), uid, gid)
            for filename in filenames:
                os.chown(os.path.join(root, filename), uid, gid)
    elif os.path.isfile(path):
        os.chown(path, uid, gid)

def remove(path):
    if os.path.exists(path):
        if os.path.islink(path) or os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def cleanDir(path):
    if os.path.exists(path):
        for x in os.listdir(path):
            remove(os.path.join(path, x))
        