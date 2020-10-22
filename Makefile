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


.PHONY:all

all: package
	@echo "complete"

prepare:
	@echo "prepare..."
	rm -rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)
	cp -rf elastic-service-mpack $(BUILD_DIR)/
	cd $(BUILD_DIR)/
	if [ $(DEFAULT_VER) != $(VERSION) ];then mv  elastic-service-mpack/addon-services/ELASTICSEARCH/$(DEFAULT_VER) elastic-service-mpack/addon-services/ELASTICSEARCH/$(VERSION); fi 
	if [ $(DEFAULT_VER) != $(VERSION) ];then mv  elastic-service-mpack/common-services/ELASTICSEARCH/$(DEFAULT_VER) elastic-service-mpack/common-services/ELASTICSEARCH/$(VERSION); fi 
	find . -name "metainfo.xml" |xargs sed -i 's/<displayName>ElasticSearch<\/displayName>/<displayName>$(NAME)<\/displayName>/g'

package: prepare
	@echo "package..."
	cd $(BUILD_DIR)/
	tar zcf $(BUILD_DIR)/elastic-service-mpack.tar.gz elastic-service-mpack

clean:
	rm -rf $(BUILD_DIR)
help:
	@echo "do make build release mpack tar"
	@echo "do make NAME=custom service name build release mpack tar"
	@echo "do make VERSION=custom version build release mpack tar"
	@echo "do make NAME=custom service name VERSION=custom version build release mpack tar"
