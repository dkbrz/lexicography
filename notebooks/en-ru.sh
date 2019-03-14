python3 split_into_small.py en ru
python3 run.py en ru ../models/english-partut-ud-2.3-181115.udpipe
python3 run.py ru en ../models/russian-syntagrus-ud-2.3-181115.udpipe
sudo chmod -R a+rwx ../languages/*
python3 train_adagram.py en ru
python3 train_adagram.py ru en
python3 sense_files.py en ru /home/dkbrz/lexicography/languages/en_ru/en/en.pkl
python3 sense_files.py ru en /home/dkbrz/lexicography/languages/en_ru/ru/ru.pkl
python3 join_files.py ru en
python3 join_files.py en ru
cd ../languages/en_ru/
paste en_align.txt ru_align.txt | pr -t > en-ru.txt
sed "s/\t/ ||| /" en-ru.txt > en-ru-2.txt
~/fast_align/fast_align -i en-ru-2.txt -d -o -v > forward.align
~/fast_align/fast_align -i en-ru-2.txt -d -o -v -r > reverse.align
~/fast_align/atools -i forward.align -j reverse.align -c grow-diag-final-and > en-ru.align
cd ..
sudo tar -zcvf en_ru.tar.gz en_ru