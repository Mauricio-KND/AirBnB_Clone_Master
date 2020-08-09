#!/usr/bin/env bash

if [ $# -lt 1 ]
then
	echo "Usage: ./run_web_dynamic.sh <module file name>"
else

	module=$(echo $1 | tr '/' '.')
	module="${module:0:-3}"
	echo $module

	HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m "$module"
fi