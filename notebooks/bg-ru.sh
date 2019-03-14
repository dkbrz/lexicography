python3 split_into_small.py bg ru
python3 run.py bg ru ../models/bulgarian-btb-ud-2.3-181115.udpipe
python3 run.py ru bg ../models/russian-taiga-ud-2.3-181115.udpipe
sudo chmod -R a+rwx ../languages/*
python3 train_adagram.py bg ru

python3 sense_files.py bg ru /home/dkbrz/lexicography/languages/bg_ru/bg/bg.pkl
python3 sense_files.py ru bg /home/dkbrz/lexicography/languages/en_ru/ru/ru.pkl
python3 join_files.py ru bg
python3 join_files.py bg ru
cd ../languages/bg_ru/
paste bg_align.txt ru_align.txt | pr -t > bg-ru.txt
sed "s/\t/ ||| /" bg-ru.txt > bg-ru-2.txt
~/fast_align/fast_align -i bg-ru-2.txt -d -o -v > forward.align
~/fast_align/fast_align -i bg-ru-2.txt -d -o -v -r > reverse.align
~/fast_align/atools -i forward.align -j reverse.align -c grow-diag-final-and > bg-ru.align
python3 join_token.py bg ru
python3 join_token.py ru bg
sudo tar -zcvf bg_ru.tar.gz bg_ru