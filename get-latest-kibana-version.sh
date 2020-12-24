#!/usr/bin/env bash
wget --no-check-certificate -qO- https://api.github.com/repos/elastic/kibana/releases/latest | grep 'tag_name' | cut -d\" -f4 | tr -d 'a-zA-Z' | head -1
