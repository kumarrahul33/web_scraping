#!/bin/bash
# args required start_index end_index  number_of_terminals excel_file
[ -d "./nohup-outs-serp" ] && rm nohup-outs-serp/*
[ ! -d "./nohup-outs-serp" ] && mkdir nohup-outs-serp
a=$1
b=$2
t=$3
fname=$4
n=`expr  $b - $a`
n=`expr $n / $t`
echo $n

# for i in {$a..$b}
# do
#     echo "hello $i"
# done

while ((a+n < b))
do
    nohup "echo $a `expr $a + $n` $fname; python serp_scraper.py $fname $a `expr $a + $n` > nohup-outs-serp/$a-log.out" &
    ((a = a + n))
done

nohup "echo $a $b $fname;python serp_scraper.py $fname $a $b > nohup-outs-serp/$a-log.out"







