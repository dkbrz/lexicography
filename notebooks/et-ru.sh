python3 split_into_small.py et ru
python3 run.py et ru ../models/estonian-edt-ud-2.3-181115.udpipe
python3 run.py ru et ../models/russian-syntagrus-ud-2.3-181115.udpipe
sudo chmod -R a+rwx ../languages/*
python3 train_adagram.py et ru --augment

python3 sense_files.py et ru /home/dkbrz/lexicography/languages/et_ru/et/et.pkl
python3 sense_files.py ru et /home/dkbrz/lexicography/languages/en_ru/ru/ru.pkl
python3 join_files.py ru et
python3 join_files.py et ru
cd ../languages/et_ru/
paste et_align.txt ru_align.txt | pr -t > et-ru.txt
sed "s/\t/ ||| /" et-ru.txt > et-ru-2.txt
~/fast_align/fast_align -i et-ru-2.txt -d -o -v > forward.align
~/fast_align/fast_align -i et-ru-2.txt -d -o -v -r > reverse.align
~/fast_align/atools -i forward.align -j reverse.align -c grow-diag-final-and > et-ru.align
python3 join_token.py et ru
python3 join_token.py ru et
sudo tar -zcvf et_ru.tar.gz et_ru