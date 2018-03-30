PROJECT = ftc_scraper
VIRTUAL_ENV = venv_temp
FUNCTION_NAME = ftc_scraper
AWS_REGION = us-west-2
FUNCTION_HANDLER = lambda_handler
LAMBDA_ROLE = arn:aws:iam::889200810732:role/service-role/basic-role

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

zip: 
	cd ./package/tmp && zip -r ../$(PROJECT).zip .

lambda_delete: 
	aws lambda delete-function \
		--function-name $(FUNCTION_NAME)

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
		--environment Variables={Example=Success} \

lambda_run: 
	aws lambda invoke \
		--invocation-type RequestResponse \
		--function-name $(PROJECT) \
		--region $(AWS_REGION) \
		--log-type Tail \
		--payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' \
		outputfile.txt 