# lexicography

План:

1)  Препроцессинг - Ира
  лемматизация, токенизация, POS-теггинг с помощью UDPipe
  
2)  Alignment (nltk) - Ира

3)  БД - Женя
  sent: id, sent_1, sent_2
  alignment: id, id_sent, ind_token_1, ind_token_2, id_lemma_1, id_lemma_2
  dictionary_1: id, lemma_1
  dictionary_2: id, lemma_2
  
4)  Группирование переводов по частотности - Женя

5)  Создание сайта - Женя
