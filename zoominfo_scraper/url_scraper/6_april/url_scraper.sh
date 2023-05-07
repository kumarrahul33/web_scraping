#!/bin/bash
# args required start_index end_index  number_of_terminals excel_file
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
    gnome-terminal -- bash -c "echo $a `expr $a + $n` $fname; python serp_scraper.py $fname $a `expr $a + $n`"
    ((a = a + n))
done

gnome-terminal -- bash -c "echo $a $b $fname;python serp_scraper.py $fname $a $b"







