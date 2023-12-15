#!/bin/bash

# Get date
echo

after=$(openssl x509 -noout -in www-fib-upc-es.pem -startdate) ;
before=$(openssl x509 -noout -in www-fib-upc-es.pem -enddate) ;

echo "Not Before: " $(date -d "${after#*=}" +"%Y-%m-%d %H:%M:%S %Z")
echo "Not After : " $(date -d "${before#*=}" +"%Y-%m-%d %H:%M:%S %Z")

modulus=$(openssl x509 -noout -in www-fib-upc-es.pem -modulus)

echo "Modulus   : " "${modulus#*=}"

echo $(openssl x509 -noout -text -in www-fib-upc-es.pem | grep "Exponent")

echo $(openssl x509 -noout -text -in www-fib-upc-es.pem | grep "CPS")
echo
echo "CRL Distribution Point :"
echo $(openssl x509 -noout -text -in www-fib-upc-es.pem | grep -A 3 "CRL" | awk 'NR==3 {print}')
echo "Number of Revoked Certificates:" $(openssl crl -in GEANTOVRSACA4.crl -text | grep "Serial Number" | wc -l)
echo
echo "Online Certificate Status Protocol:"
echo $(openssl x509 -noout -text -in www-fib-upc-es.pem | grep "OCSP")
echo
echo "Certificate status for www-fib-upc-es:"
echo $(openssl ocsp -issuer GEANTOVRSACA4.pem -cert www-fib-upc-es.pem -text -url http://GEANT.ocsp.sectigo.com | tail -3)