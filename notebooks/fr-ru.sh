python3 split_into_small.py fr ru
python3 run.py fr ru ../models/french-gsd-ud-2.3-181115.udpipe
python3 run.py ru fr ../models/russian-syntagrus-ud-2.3-181115.udpipe
sudo chmod -R a+rwx ../languages/*
python3 train_adagram.py fr ru

python3 sense_files.py fr ru /home/dkbrz/lexicography/languages/fr_ru/fr/fr.pkl
python3 sense_files.py ru fr /home/dkbrz/lexicography/languages/en_ru/ru/ru.pkl
python3 join_files.py ru fr
python3 join_files.py fr ru
cd ../languages/fr_ru/
paste fr_align.txt ru_align.txt | pr -t > fr-ru.txt
sed "s/\t/ ||| /" fr-ru.txt > fr-ru-2.txt
~/fast_align/fast_align -i fr-ru-2.txt -d -o -v > forward.align
~/fast_align/fast_align -i fr-ru-2.txt -d -o -v -r > reverse.align
~/fast_align/atools -i forward.align -j reverse.align -c grow-diag-final-and > fr-ru.align
python3 join_token.py fr ru
python3 join_token.py ru fr
sudo tar -zcvf fr_ru.tar.gz fr_ru