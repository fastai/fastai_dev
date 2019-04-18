echo "Building 'impractical' notabooks... ;-)"

for file in *.ipynb
do
    python notebook2script.py $file 
done

echo "DONE"
