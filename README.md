# openapi-samples
API samples following given specs. 


## Converting openapi-v3 to openapi-v2

To convert between formats use:

        ./bin/api-spec-converter.sh $INFILE -f openapi_3 -t swagger_2 -s yaml  > $OUTFILE

To convert all v3 files to v2, use:

        find openapi-v3/ -name \*.yaml \
          -exec bash -c 'I="{}"; ./bin/api-spec-converter.sh "$I" -f openapi_3 -t swagger_2 -s yaml > "${I//v3/v2}" ' \; 

