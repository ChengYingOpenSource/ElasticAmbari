#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python

import os
import shutil
import pwd
import grp
import unicodedata

def chown(path, user, group):
    userMeta = pwd.getpwnam(user)
    uid = userMeta.pw_uid
    groupMeta = grp.getgrnam(group)
    gid = groupMeta.gr_gid
    if os.path.isdir(path):
        os.chown(path, uid, gid)
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
        
def isBooleanString(s):
    return s == "true" or s == "false"

def toBoolean(s):
    if s == "true":
        return True
    else:
        return False

def isNumberic(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def toNumber(s):
    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        pass
    return unicodedata.numeric(s.decode("utf-8"))