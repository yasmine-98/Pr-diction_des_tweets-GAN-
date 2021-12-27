import string
import unidecode

class data_loader():
    def nettoyer_data(data):
         list_listword=[]#liste des listes des mots de chaque tweet
         list_tweets=data.split('\n')
         l=[]
         for text in list_tweets:
             text = text.translate(str.maketrans('', '', string.punctuation))
             text = re.sub(r'http\S+', '', text)   # Remove URLs
             text = re.sub(r'—', ' ', text)
             text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions
             text = text.strip(" ")   # Remove whitespace resulting from above
             text = re.sub(r' +', ' ', text)   # Remove redundant spaces
             text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com').replace('=', '').replace('>', '')
             text= re.sub(r"\ [A-Za-z]*\.com", " ", text)
             pattern = re.compile(r'\s+') 
             text = re.sub(pattern, ' ', text)
             text = text.replace('?', ' ? ').replace(')', ') ')
             text = unidecode.unidecode(text)
             text = text.lower()
             Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
             text = Pattern_alpha.sub(r"\1\1", text) 
             Pattern_Punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
             text= Pattern_Punct.sub(r'\1', text)
             text = re.sub(' {2,}',' ', text)
             text = re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', text)
             l.append(text)
         return l
    def tokenizer_data(list_tweets, tokenizer):
        tokenizer.fit_on_texts(list_tweets)
        sequences = tokenizer.texts_to_sequences(list_tweets)
        vocab_size=len(tokenizer.word_index)
        return sequences, vocab_size

    def max_tweet(sequences):
        max_length=0
        for i in range(len(sequences)):
            if(len(sequences[i])>max_length):
                max_length=len(sequences[i])
        return max_length
    def preparer_data(sequences, vocab_size, size_batch):
        sequences=sequences[:len(sequences)-2]
        nb_tweet = len(sequences)
        nb=int(nb_tweet/2)
        X = sequences[:nb]
        y = sequences[nb:]
        X_train = pad_sequences(X, maxlen=size_batch, padding='post')
        y_train = pad_sequences(y, maxlen=size_batch, padding='post')
        print(X_train)
        print(y_train)
        X_train = X_train.reshape(nb, size_batch, 1)
        y_train = y_train.reshape(nb, size_batch, 1)
        return X_train, y_train, nb_tweet
