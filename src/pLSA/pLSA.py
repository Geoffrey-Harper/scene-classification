from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
import numpy as np

def create_NMF(ex_histograms, num_topics):

    # num components should be num topics, currently not for debugging purposes
    model = NMF(n_components=num_topics, init='nndsvda')

    document_topic_matrix = model.fit_transform(ex_histograms)
    document_topic_matrix = np.asarray(document_topic_matrix)
    norm_matrix = []
    # normalize !!!!
    print("normalizing document/topic matrix")

    for z_array in document_topic_matrix:
        array_sum = 0
        for element in z_array:
            array_sum += element

        norm_matrix.append(z_array/array_sum)

    return norm_matrix