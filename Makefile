CURRENT_PATH := $(shell pwd)
BUILD_DIR := $(CURRENT_PATH)/build
ifndef ELASTIC_VERSION
ELASTIC_VERSION := $(shell bash $(CURRENT_PATH)/get-latest-elastic-version.sh)
endif
DEFAULT_VERSION := x.y.z
SRC_PKG_NAME := elastic-service-mpack
DEST_PKG_DIR := $(BUILD_DIR)/$(SRC_PKG_NAME)
PYYAML_DIR := $(BUILD_DIR)/pyyaml

.PHONY:all

all: clean package
	@echo "completed"

prepare: prepare-build prepare-elasticsearch prepare-kibana
	sed -s -i 's#$(DEFAULT_VERSION)#$(ELASTIC_VERSION)#g' $(DEST_PKG_DIR)/mpack.json
	@echo "prepare completed"

prepare-build:
	mkdir -p $(BUILD_DIR)
	cp -rf $(SRC_PKG_NAME) $(BUILD_DIR)
	git clone https://github.com/yaml/pyyaml.git $(PYYAML_DIR) && cd $(PYYAML_DIR) && git checkout tags/5.4.1.1 && python setup.py --without-libyaml build 


prepare-elasticsearch:
	mv -v $(DEST_PKG_DIR)/addon-services/ELASTICSEARCH/$(DEFAULT_VERSION) $(DEST_PKG_DIR)/addon-services/ELASTICSEARCH/$(ELASTIC_VERSION)
	mv -v $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(DEFAULT_VERSION) $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(ELASTIC_VERSION)
	xmlstarlet ed --inplace -u /metainfo/services/service/version -v $(ELASTIC_VERSION) -u /metainfo/services/service/extends -v common-services/ELASTICSEARCH/$(ELASTIC_VERSION) $(DEST_PKG_DIR)/addon-services/ELASTICSEARCH/$(ELASTIC_VERSION)/metainfo.xml 
	xmlstarlet ed --inplace -u /metainfo/services/service/version -v $(ELASTIC_VERSION) -u /metainfo/services/service/osSpecifics/osSpecific/packages/package/name -v elasticsearch-$(ELASTIC_VERSION) $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(ELASTIC_VERSION)/metainfo.xml 
	xmlstarlet ed --inplace -u "/configuration/property[@name='elasticsearch.download.url']/value" -v "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-$(ELASTIC_VERSION)-linux-x86_64.tar.gz" $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(ELASTIC_VERSION)/configuration/elasticsearch-env.xml
	cp -rp $(PYYAML_DIR)/build/*/yaml $(DEST_PKG_DIR)/common-services/ELASTICSEARCH/$(ELASTIC_VERSION)/package/scripts/

prepare-kibana:
	mv -v $(DEST_PKG_DIR)/addon-services/KIBANA/$(DEFAULT_VERSION) $(DEST_PKG_DIR)/addon-services/KIBANA/$(ELASTIC_VERSION)
	mv -v $(DEST_PKG_DIR)/common-services/KIBANA/$(DEFAULT_VERSION) $(DEST_PKG_DIR)/common-services/KIBANA/$(ELASTIC_VERSION)
	xmlstarlet ed --inplace -u /metainfo/services/service/version -v $(ELASTIC_VERSION) -u /metainfo/services/service/extends -v common-services/KIBANA/$(ELASTIC_VERSION) $(DEST_PKG_DIR)/addon-services/KIBANA/$(ELASTIC_VERSION)/metainfo.xml 
	xmlstarlet ed --inplace -u /metainfo/services/service/version -v $(ELASTIC_VERSION) -u /metainfo/services/service/osSpecifics/osSpecific/packages/package/name -v kibana-$(ELASTIC_VERSION) $(DEST_PKG_DIR)/common-services/KIBANA/$(ELASTIC_VERSION)/metainfo.xml 
	xmlstarlet ed --inplace -u "/configuration/property[@name='kibana.download.url']/value" -v "https://artifacts.elastic.co/downloads/kibana/kibana-$(ELASTIC_VERSION)-linux-x86_64.tar.gz" $(DEST_PKG_DIR)/common-services/KIBANA/$(ELASTIC_VERSION)/configuration/kibana-env.xml
	cp -rp $(PYYAML_DIR)/build/*/yaml $(DEST_PKG_DIR)/common-services/KIBANA/$(ELASTIC_VERSION)/package/scripts/
	
package: prepare
	cd $(BUILD_DIR) && tar zcf $(BUILD_DIR)/$(SRC_PKG_NAME).tar.gz $(SRC_PKG_NAME)
	rm -rf $(PYYAML_DIR)
	@echo "package completed"

clean:
	@rm -rf $(BUILD_DIR)

help:
	@echo "do make build release mpack tar"
	@echo "do ELASTIC_VERSION=custom version build release mpack tar"
