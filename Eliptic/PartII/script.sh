#!/bin/bash

# Get date
echo

after=$(openssl x509 -noout -in www-fib-upc-es.pem -startdate) ;
before=$(openssl x509 -noout -in www-fib-upc-es.pem -enddate) ;

echo "Not Before: " $(date -d "${after#*=}" +"%Y-%m-%d %H:%M:%S %Z")
echo "Not After : " $(date -d "${after#*=}" +"%Y-%m-%d %H:%M:%S %Z")

modulus=$(openssl x509 -noout -in www-fib-upc-es.pem -modulus)

echo "Modulus   : " "${modulus#*=}"

echo $(openssl x509 -noout -text -in www-fib-upc-es.pem | grep "Exponent")