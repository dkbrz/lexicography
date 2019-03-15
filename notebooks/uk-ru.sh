python3 split_into_small.py uk ru
python3 run.py uk ru ../models/ukrainian-iu-ud-2.3-181115.udpipe
python3 run.py ru uk ../models/russian-syntagrus-ud-2.3-181115.udpipe
sudo chmod -R a+rwx ../languages/*
python3 train_adagram.py uk ru

python3 sense_files.py uk ru /home/dkbrz/lexicography/languages/uk_ru/uk/uk.pkl
python3 sense_files.py ru uk /home/dkbrz/lexicography/languages/en_ru/ru/ru.pkl
python3 join_files.py ru uk
python3 join_files.py uk ru
cd ../languages/uk_ru/
paste uk_align.txt ru_align.txt | pr -t > uk-ru.txt
sed "s/\t/ ||| /" uk-ru.txt > uk-ru-2.txt
~/fast_align/fast_align -i uk-ru-2.txt -d -o -v > forward.align
~/fast_align/fast_align -i uk-ru-2.txt -d -o -v -r > reverse.align
~/fast_align/atools -i forward.align -j reverse.align -c grow-diag-final-and > uk-ru.align
python3 join_token.py uk ru
python3 join_token.py ru uk
sudo tar -zcvf uk_ru.tar.gz uk_ru