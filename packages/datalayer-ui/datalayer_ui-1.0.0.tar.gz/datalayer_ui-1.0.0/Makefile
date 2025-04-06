# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

.PHONY: clean build dist

default: all ## Default target is all.

help: ## display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: clean install build dist ## Clean Install and Build

clean:
	npm clean

build:
	npm run build

build-tsc:
	npm run build:tsc

deploy-ai: ## deploy-ai
	export S3_BUCKET_NAME=datalayer-ai && \
		export ENTRY="./src/AI" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E2EZCS9JFFV23P && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.ai && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-io: ## deploy-io
	export S3_BUCKET_NAME=datalayer-io && \
		export ENTRY="./src/IO" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E37RU7E3SQ7LVT && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.io && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-app: ## deploy-app
	export S3_BUCKET_NAME=datalayer-app && \
		export ENTRY="./src/App" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E2JXQ17OYDER6B && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.app && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-run: ## deploy-run
	export S3_BUCKET_NAME=datalayer-run && \
		export ENTRY="./src/Run" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E2IF03HLWPTICX && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.run && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-status: ## deploy-status
	export S3_BUCKET_NAME=datalayer-status && \
		export ENTRY="./src/Status" && \
		export CLOUDFRONT_DISTRIBUTION_ID=EVEQ9ZZPSQX98 && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://status.datalayer.run && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-tech: ## deploy-tech
	export S3_BUCKET_NAME=datalayer-tech && \
		export ENTRY="./src/Tech" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E2IF03HLWPTICX && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.tech && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-earth: ## deploy-earth
	export S3_BUCKET_NAME=datalayer-earth && \
		export ENTRY="./src/Earth" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E3SFDFJP489L4U && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.earth && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-bio: ## deploy-bio
	export S3_BUCKET_NAME=datalayer-bio && \
		export ENTRY="./src/Bio" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E3HCJJBIU6HFBQ && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://datalayer.bio && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-dev1: ## deploy-dev1
	export S3_BUCKET_NAME=datalayer-io-dev1 && \
		export ENTRY="./src/App" && \
		export CLOUDFRONT_DISTRIBUTION_ID=EB47GYKBX4PSR && \
		export DATALAYER_RUN_URL=https://dev1.datalayer.run && \
		export DATALAYER_CDN_URL=https://dev1.datalayer.io && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-docs-io: ## deploy-docs-io
	export S3_BUCKET_NAME=datalayer-io-docs && \
		export ENTRY="./src/IODocs" && \
		export CLOUDFRONT_DISTRIBUTION_ID=E2L5DN4UP608Y5 && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://docs.datalayer.io && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-docs-run: ## deploy-docs-run
	export S3_BUCKET_NAME=datalayer-run-docs && \
		export ENTRY="./src/RunDocs" && \
		export CLOUDFRONT_DISTRIBUTION_ID=EX8YQ4EWXHO4I && \
		export DATALAYER_RUN_URL=https://prod1.datalayer.run && \
		export DATALAYER_CDN_URL=https://docs.datalayer.run && \
		${DATALAYER_HOME}/src/landings/datalayer/ui/dev/deploy.sh

deploy-primer-brand-storybook: ## deploy-primer-brand-storybook
#   copy all the build assets into the `brand/storybook` subfolder
	aws s3 rm s3://datalayer-primer-brand-storybook --recursive --profile datalayer	
	aws s3 cp /home/echarles/Content/datalayer-osp/ext/primer-brand/apps/docs/public/storybook s3://datalayer-primer-brand-storybook --recursive --profile datalayer
	aws cloudfront create-invalidation --distribution-id E8FW5YE8MOVN3 --paths "/*" --profile datalayer
	aws s3 ls s3://datalayer-primer-brand-storybook --profile datalayer
	echo open ✨ https://primer-brand-storybook.datalayer.tech

build-storybook: ## build-storybook
	npm run build:storybook

start-storybook: ## start-storybook
	npm storybook

deploy-tech-storybook: build-storybook ## deploy-tech-storybook to s3
	aws s3 rm \
		s3://datalayer-tech-storybook/ \
		--recursive \
		--profile datalayer && \
	aws s3 cp \
		./storybook-static \
		s3://datalayer-tech-storybook/ \
		--recursive \
		--profile datalayer && \
	 aws cloudfront create-invalidation \
		--distribution-id E3CYF4GDN3UVT \
		--paths "/*" \
		--profile datalayer && \
	echo open ✨ https://storybook.datalayer.tech

publish-npm: clean build-tsc ## publish
	npm publish --access public
	echo open https://www.npmjs.com/package/@datalayer/ui

publish-pypi: # publish the pypi package
	git clean -fdx && \
		python -m build
	@exec echo
	@exec echo twine upload ./dist/*-py3-none-any.whl
	@exec echo
	@exec echo https://pypi.org/project/datalayer-ui/#history

publish-conda: # publish the conda package
	@exec echo
	cd ./conda-recipe; ./publish-conda.sh
	@exec echo
	@exec echo https://anaconda.org/datalayer/datalayer-core
	@exec echo conda install datalayer::datalayer-ui
