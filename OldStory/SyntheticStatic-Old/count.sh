for i in $(seq 133 488)
do
    <InputsEqualized/$i.csv wc -l >> CountEqualized.csv
done
