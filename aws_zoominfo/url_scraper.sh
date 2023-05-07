#!/bin/bash
# args required start_index end_index  number_of_terminals excel_file
[ -d "./nohup-outs" ] && rm nohup-outs/*
[ ! -d "./nohup-outs" ] && mkdir nohup-outs
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
    nohup python serp_scraper.py $fname "$a" `expr $a + $n` > "nohup-outs/$a-log.out" &
    ((a = a + n))
done

nohup python serp_scraper.py $fname "$a" `expr $b` > "nohup-outs/$a-log.out" &