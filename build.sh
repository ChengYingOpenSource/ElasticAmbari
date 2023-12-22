#!/usr/bin/env bash
set -e
SERVICE_VERSION=${1:-""}
CURRENT_PATH="$( cd "$( dirname "$0"  )" && pwd  )"
echo "Current path: $CURRENT_PATH"
BUILD_DIR=${CURRENT_PATH}/build
DIST_DIR=${CURRENT_PATH}/dist
if [[ -z "${SERVICE_VERSION}" ]]; then 
    LATEST_VERSION="$(bash get-latest-elastic-version.sh)"
    SERVICE_VERSION=${SERVICE_VERSION:-"${LATEST_VERSION}"}
fi

if [[ -z "${SERVICE_VERSION}" ]]; then 
    echo "SERVICE_VERSION is empty, please specify it to the SERVICE_VERSION"
    exit 1;
fi
echo "SERVICE_VERSION:${SERVICE_VERSION} LATEST_VERSION:${LATEST_VERSION}"
DEFAULT_VERSION=x.y.z
SRC_PKG_NAME=elastic-service-mpack
DEST_PKG_DIR=${BUILD_DIR}/${SRC_PKG_NAME}

echo "prepare..."
rm -rf ${BUILD_DIR} && mkdir -p ${BUILD_DIR}
cp -rf ${SRC_PKG_NAME} ${BUILD_DIR}
echo "${DEST_PKG_DIR} prepare completed"
mv ${DEST_PKG_DIR}/addon-services/ELASTICSEARCH/${DEFAULT_VERSION} ${DEST_PKG_DIR}/addon-services/ELASTICSEARCH/${SERVICE_VERSION}
mv ${DEST_PKG_DIR}/common-services/ELASTICSEARCH/${DEFAULT_VERSION} ${DEST_PKG_DIR}/common-services/ELASTICSEARCH/${SERVICE_VERSION}
mv ${DEST_PKG_DIR}/addon-services/KIBANA/${DEFAULT_VERSION} ${DEST_PKG_DIR}/addon-services/KIBANA/${SERVICE_VERSION}
mv ${DEST_PKG_DIR}/common-services/KIBANA/${DEFAULT_VERSION} ${DEST_PKG_DIR}/common-services/KIBANA/${SERVICE_VERSION}
# mac需要添加空格
#sed -i ‘’ 's/${DEFAULT_VERSION}/${SERVICE_VERSION}/g' `grep ${DEFAULT_VERSION} -rl ${DEST_PKG_DIR}/*`
#sed -i 's/${DEFAULT_VERSION}/${SERVICE_VERSION}/g' `grep ${DEFAULT_VERSION} -rl ${DEST_PKG_DIR}/*`
#find ${DEST_PKG_DIR} -type f -exec sed -i 's/${DEFAULT_VERSION}/${SERVICE_VERSION}/g' {} \;
find ${DEST_PKG_DIR} -type f -exec perl -pi -e 's/${DEFAULT_VERSION}/${SERVICE_VERSION}/g' {} \;

cd ${BUILD_DIR} && tar zcf ${BUILD_DIR}/${SRC_PKG_NAME}.tar.gz ${SRC_PKG_NAME}
rm -rf ${DIST_DIR} && mkdir -p ${DIST_DIR} && mv ${BUILD_DIR}/${SRC_PKG_NAME}.tar.gz ${DIST_DIR}
rm -rf ${BUILD_DIR}
echo "${SRC_PKG_NAME}-${SERVICE_VERSION} package completed"