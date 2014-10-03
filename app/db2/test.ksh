#!/bin/ksh

> big.sql
for i in {1..100}
do
    cat test.sql >> big.sql
done
