for i in $(seq 133 488)
do
    <Inputs/$i.csv wc -l >> count.csv
done
