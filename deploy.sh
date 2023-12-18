# aws --profile sandbox s3 cp index.html s3://tass-musicgeoanalyser/
rm -rf function.zip
zip -r function.zip package.json index.js node_modules 
aws --profile sandbox lambda update-function-code --function-name app --zip-file fileb://./function.zip