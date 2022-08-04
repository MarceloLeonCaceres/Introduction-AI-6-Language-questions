import nltk
import sys
import os
import math
# nltk.download('stopwords')
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    
    # files = load_files(sys.argv[1])
    files = load_files('corpus')
    # print(files.keys())
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    # for archivo in file_words.keys():
    #     print(f"archivo: {archivo} tiene {len(file_words[archivo])} palabras")
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)    

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    print("Loading data...")
    files = dict()
    for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        # print(filePath)
        with open(filePath, encoding='utf-8') as f:        
            files[file] = f.read()
    return files
    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # with open('english') as f:
    #     stopWords = set(f.read().splitlines())

    stopWords = nltk.corpus.stopwords.words("english")
    # print(stopWords)

    # for signo in string.punctuation:
    #     print(signo)

    lista = []
    for palabra in nltk.word_tokenize(document.lower()):
        if (not all(caracteres in string.punctuation for caracteres in palabra)) and (palabra not in stopWords):
            lista.append(palabra.lower()) 
           
    return lista
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_dict = {}
    for doc in documents.keys():
        setPalUnicas = set(documents[doc])
        lstPalUnicas = list(setPalUnicas)
        for palabra in lstPalUnicas:
            if palabra not in idf_dict:
                idf_dict[palabra] = 1
            else:
                idf_dict[palabra] += 1
    
    for palabra in idf_dict.keys():
        idf_dict[palabra] = math.log10(len(documents)/idf_dict[palabra])
    return idf_dict
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """     

    tf_idf = dict()
    for file in files.keys():
        value = 0.0
        for word in query: 
            value += idfs[word] * files[file].count(word)
        tf_idf[file] = value
    
    dict_Ordered = dict(sorted(tf_idf.items(), key=lambda item: item[1], reverse=True))
    print()
    # print(dict_Ordered)

    listaArchivos = []
    listaArchivos = list(dict_Ordered.keys())[:n]    
    # print(listaArchivos)
    return listaArchivos     
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    valorOraciones = list()
    for parrafo in sentences:
        valor = 0.0
        frecuencia = 0
        for palabra in query:
            if palabra in sentences[parrafo]:
                valor += idfs[palabra]
                frecuencia += sentences[parrafo].count(palabra)
        frecuencia = frecuencia /len(sentences[parrafo])
        valorOraciones.append([parrafo, valor, frecuencia])

    listaOrdenada1 = sorted(valorOraciones, key=lambda val: (val[1], val[2]), reverse=True)    
    
    return [item[0] for item in listaOrdenada1[:n]]

if __name__ == "__main__":
    main()
