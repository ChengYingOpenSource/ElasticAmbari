# Makefile
CURRENT_PATH := $(shell pwd)
BUILD_DIR := $(CURRENT_PATH)/build

.PHONY:all

all: package
	@echo "complete"

package:
	mkdir -p $(BUILD_DIR)
	tar zcf $(BUILD_DIR)/elastic-service-mpack.tar.gz elastic-service-mpack

clean:
	rm -rf $(BUILD_DIR)