#!/usr/bin/env bash
wget --no-check-certificate -qO- https://api.github.com/repos/elastic/elasticsearch/releases/latest | grep 'tag_name' | cut -d\" -f4 | tr -d 'a-zA-Z' | head -1
