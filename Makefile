PROJECT = ftc_scraper
VIRTUAL_ENV = venv_temp
FUNCTION_NAME = ftc_scraper
AWS_REGION = us-west-2
FUNCTION_HANDLER = lambda_handler
LAMBDA_ROLE = arn:aws:iam::889200810732:role/service-role/basic-role

KEY_ID = arn:aws:kms:us-west-2:889200810732:key/ffed0d5a-4984-4c4a-a3f1-b2ab46e6bae7

#Commands
build: clean_package build_package_tmp copy_python remove_unused zip 
update: build lambda_delete lambda_create lambda_run 

clean_package: #delete everything 
	rm -rf ./package/*

virtual: 
	@echo "--> Setup and activate virtualenv"
	if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv $(VIRTUAL_ENV); \
	fi
	@echo ""

others_installs: 
	pip install awscli

build_package_tmp: #copy over project 
	mkdir -p ./package/tmp/lib 
	cp -a ./$(PROJECT)/. ./package/tmp

copy_python: 
	if test -d $(VIRTUAL_ENV)/lib; then \
		cp -a $(VIRTUAL_ENV)/lib/python2.7/site-packages/. ./package/tmp; \
	fi 
	if test -d $(VIRTUAL_ENV)/lib64; then \
		cp -a $(VIRTUAL_ENV)/lib64/python2.7/site-packages/. ./package/tmp; \
	fi 

remove_unused: #gets rid of python files/dirs that we don't need to thin out lambda fn 
	rm -rf ./package/tmp/wheel*
	rm -rf ./package/tmp/easy_install*
	rm -rf ./package/tmp/setuptools*
	rm -rf ./package/tmp/pkg_resources*
	rm -rf ./package/tmp/pip*
	rm -rf ./package/tmp/dateutil*
	rm -rf ./package/tmp/jmespath*
	rm -rf ./package/tmp/oauth2client*
	rm -rf ./package/tmp/aws_encryption*
	rm -rf ./package/tmp/asn1crypto*
	rm -rf ./package/tmp/botocore*
	rm -rf ./package/tmp/docutils*
	rm -rf ./package/tmp/httplib2/*
	rm -rf ./package/tmp/google*
	rm -rf ./package/tmp/cryptography*
	rm -rf ./package/tmp/ipaddress*
	rm -rf ./package/tmp/pyasn*
	rm -rf ./package/tmp/rsa*
	rm -rf ./package/tmp/s3*
	rm -rf ./package/tmp/pycparser*
	rm -rf ./package/tmp/python_dateutil*
	rm -rf ./package/tmp/wrapt*
	rm -rf ./package/tmp/idna*
	rm -rf ./package/tmp/cffi*
	rm -rf ./package/tmp/attr*
	rm -rf ./package/tmp/uri*
	rm -rf ./package/tmp/six*
	rm -rf ./package/tmp/concurrent*
	rm -rf ./package/tmp/enumerate*
	rm -rf ./package/tmp/futures*
	rm -rf ./package/tmp/apiclient*
	rm -rf ./package/tmp/enum*
	rm -rf ./package/tmp/beautifulsoup*
	rm -rf ./package/tmp/httplib2*

zip: 
	cd ./package/tmp && zip -r ../$(PROJECT).zip .

lambda_delete: 
	aws lambda delete-function \
		--function-name $(FUNCTION_NAME)

# Creates a customer master key (CMK) in the caller's AWS account.
# Only called once 
create_key: 
	aws kms create-key \
		--description "Key used to encrypt and decrypt sensitive PAN data"

lambda_create: 
	aws lambda create-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://./package/$(PROJECT).zip \
		--role $(LAMBDA_ROLE) \
		--handler $(PROJECT).$(FUNCTION_HANDLER) \
		--runtime python2.7 \
		--timeout 15 \
		--memory-size 128 \

	aws lambda update-function-configuration \
		--function-name $(FUNCTION_NAME) \
		--kms-key-arn $(KEY_ID) \
		--environment Variables={SpreadsheetId=$(SPREADSHEET_ID), EmailKey = $(EMAIL_KEY))} \
		# You cannot use the default Lambda service key for 
		# encrypting sensitive information on the client side. 
		# For more information, see Environment Variable Encryption.

lambda_run: 
	aws lambda invoke \
		--invocation-type RequestResponse \
		--function-name $(PROJECT) \
		--region $(AWS_REGION) \
		--log-type Tail \
		--payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' \
		outputfile.txt 

