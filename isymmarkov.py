import random

class ISYMMarkov(object):
    '''
    Class to generate ISYM Markov text using an n-gram model.
    Generalized from a 3-gram model by Shabda Raaj
    http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
    '''
    
    def __init__(self, open_file, chain_length):
        self.chain_length = chain_length
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()
    
    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words
            
    def ngrams(self):
        # Generates an n-gram from the given data string. So if our string were
        if len(self.words) < self.chain_length:
            return
        for i in range(len(self.words) - self.chain_length - 1):
            yield tuple([self.words[i + j] for j in range(self.chain_length)]) 
                    
    def database(self):
        for ngram in self.ngrams():
            key = ngram[:-1]
            if key in self.cache:
                self.cache[key].append(ngram[-1])
            else:
                self.cache[key] = [ngram[-1]]
				
    def generate_markov_isym(self, size=25):
        seed = random.randint(0, self.word_size - self.chain_length)
        n_words = [self.words[seed + i] for i in range(self.chain_length)]
        gen_words = []
        punct = [".", "!", "?"]
        
        for i in xrange(size):
            gen_words.append(n_words[0])
            key = tuple(n_words[1:])
            n_words.append(random.choice(self.cache[key]))
            del n_words[0]
        gen_words.append(n_words[-1])
        gen_words_str = ' '.join(gen_words)
        gen_words_str.replace("&quot;", "")
        isym = "I saw you... " + gen_words_str
        if isym[-1] in punct:
            return isym
        else:
            return isym + random.choice(punct)
