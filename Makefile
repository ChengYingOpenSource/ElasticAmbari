# Makefile
CURRENT_PATH := $(shell pwd)
BUILD_DIR := $(CURRENT_PATH)/build
DEFAULT_VER=7.9.2
ifndef NAME
NAME = ElasticSearch
endif
ifndef VERSION
VERSION = ${DEFAULT_VER}
endif
SRC_PKG_NAME := elastic-service-mpack
DEST_PKG_DIR := $(BUILD_DIR)/$(SRC_PKG_NAME)
PYYAML_DIR := $(BUILD_DIR)/pyyaml

.PHONY:all

all: package
	@echo "complete"

prepare:
	@echo "prepare..."
	rm -rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)
	cp -rf $(SRC_PKG_NAME) $(BUILD_DIR)/
	if [ $(DEFAULT_VER) != $(VERSION) ];then mv $(DEST_PKG_DIR)/addon-services/ELASTICSEARCH/$(DEFAULT_VER) $(DEST_PKG_DIR)/ELASTICSEARCH/$(VERSION); fi 
	if [ $(DEFAULT_VER) != $(VERSION) ];then mv $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(DEFAULT_VER) $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(VERSION); fi 
	if [ $(DEFAULT_VER) != $(VERSION) ];then find $(BUILD_DIR) -name "metainfo.xml" |xargs sed -i 's/$(DEFAULT_VER)/$(VERSION)/g'; fi 
	if [ $(DEFAULT_VER) != $(VERSION) ];then find $(BUILD_DIR) -name "mpack.json" |xargs sed -i 's/"service_version": "$(DEFAULT_VER)"/"service_version": "$(VERSION)"/g'; fi 
	find $(BUILD_DIR) -name "metainfo.xml" |xargs sed -i 's/<displayName>ElasticSearch<\/displayName>/<displayName>$(NAME)<\/displayName>/g'
	# download pyyaml
	git clone https://github.com/yaml/pyyaml.git $(PYYAML_DIR) && cd $(PYYAML_DIR) && python setup.py --without-libyaml build && cp -rp $(PYYAML_DIR)/build/*/yaml $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(VERSION)/package/scripts/

package: prepare
	@echo "package ..."
	cd $(BUILD_DIR) && tar zcf $(BUILD_DIR)/$(SRC_PKG_NAME).tar.gz $(SRC_PKG_NAME)

clean:
	rm -rf $(BUILD_DIR)

help:
	@echo "do make build release mpack tar"
	@echo "do make NAME=custom service name build release mpack tar"
	@echo "do make VERSION=custom version build release mpack tar"
	@echo "do make NAME=custom service name VERSION=custom version build release mpack tar"
