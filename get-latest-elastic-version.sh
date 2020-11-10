#!/usr/bin/env bash
git -c 'versionsort.suffix=-' ls-remote --tags   https://github.com/elastic/elasticsearch | grep -v { |tail -n 1 | awk -F 'refs/tags/v' '{print $2}'