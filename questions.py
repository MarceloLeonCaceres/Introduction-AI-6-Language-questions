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
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    # files = load_files('corpus')
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
    with open('english') as f:
        stopWords = set(f.read().splitlines())
    # print(stopWords)

    lista = []
    for palabra in nltk.word_tokenize(document.lower()):
        if palabra not in string.punctuation and palabra not in stopWords:
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
    listaPalabras = []
    for palabra in query:
        if palabra in idfs:
            if idfs[palabra] > 0.0:
                listaPalabras.append(palabra)
                # print(f"palabra:  {palabra}     idf: {idfs[palabra]}")
    
    tf = dict()
    for file in files.keys():
        frequencies = dict()
        for word in files[file]: 
            if word in listaPalabras:
                if word not in frequencies:
                    frequencies[word] = 1
                else:
                    frequencies[word] += 1
        tf[file] = frequencies
    # print(tf)   

    tf_idf = dict()
    for file in files.keys():
        value = 0.0
        for word in tf[file]: 
            value += idfs[word] * tf[file][word]
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
    valorOraciones = dict()
    for parrafo in sentences:
        valorOraciones[parrafo] = 0.0
        for palabra in query:
            if palabra in sentences[parrafo]:
                valorOraciones[parrafo] += idfs[palabra]

    dict_Ordered = dict(sorted(valorOraciones.items(), key=lambda item: item[1], reverse=True))
    print()

    listaOrdenada1 = list(dict_Ordered.keys())

    listaTemporal = dict()
    listaDefinitiva = []
    i = 0
    
    while len(listaDefinitiva) < n:
        actual = dict_Ordered[listaOrdenada1[i]]
        signte = dict_Ordered[listaOrdenada1[i+1]]
        listaTemporal[listaOrdenada1[i]] = actual
        while signte == actual:
            listaTemporal[listaOrdenada1[i+1]] = signte
            i+=1
            actual = dict_Ordered[listaOrdenada1[i]]
            signte = dict_Ordered[listaOrdenada1[i+1]]
        listaDefinitiva = UneDosListas(listaDefinitiva, listaTemporal, query)
        listaTemporal.clear()
        i+=1
    return listaDefinitiva[:n]
    # listaOrdenada2.append(listaOrdenada1[0])
    # valor = dict_Ordered[listaOrdenada1[0]]
    # valorMax = valor
    # dict_Empates = dict()
    # dict_Empates[listaOrdenada1[0]] = len(query) / len(listaOrdenada1[0])
    # i = 1
    # while valor == valorMax:        
    #     oracion = listaOrdenada1[i]
    #     valor = dict_Ordered[oracion]
    #     if valor == valorMax:            
    #         dict_Empates[oracion] = len(query)/len(oracion)            
    #     else:
    #         listaOrdenada2.append(oracion)
    #     i += 1
    #     if i >= n:
    #         return listaOrdenada2
    # dict_Ordered2 = dict(sorted(dict_Empates.items(), key=lambda item: item[1], reverse=True))
    # listaOrdenada2 = list(dict_Ordered2.keys())    
        
    # print(listaOrdenada2)
    # return listaOrdenada2          
    # raise NotImplementedError

def UneDosListas(sentences, dEmpatadas, query):
    """
    Une dos listas de oraciones, 
    sentences es la lista ordenada previamente, y
    dEmpatadas es el diccionario de oraciones que se debe
    desempatar con el higher query term density
    """
    dictEmpates = dict()
    for oracion in dEmpatadas.keys():
        dictEmpates[oracion] = len(set(query).intersection(set(nltk.word_tokenize(oracion.lower())))) / len(nltk.word_tokenize(oracion.lower()))
    dict_Ordered3 = dict(sorted(dictEmpates.items(), key=lambda item: item[1], reverse=True))
    listaOrdenada3 = list(dict_Ordered3.keys())
    if len(sentences) == 0:
        return listaOrdenada3
    else:
        sentences.extend(listaOrdenada3) 
    return sentences

if __name__ == "__main__":
    main()
