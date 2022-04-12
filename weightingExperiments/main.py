import collections
import operator

from dataAdapter import *
from CF import *
from AF import *
from TD import *
from bayesian import *
import math

def weight_to_relevance(weights):
    for key in weights:
        if weights[key] != 0:
            weights[key] = -math.log(weights[key])

    # Transform to [0 100] range
    # Code start here
    max_weight = max(weights.items(), key=operator.itemgetter(1))[1]
    min_weight = min(weights.items(), key=operator.itemgetter(1))[1]

    frac = (100 - 1) / (max_weight - min_weight)
    for key in weights:
        weights[key] = int((weights[key] - min_weight) * frac)
    # End








    return weights

if __name__ == '__main__':
    adapter = dataAdapter(table_name="nn_input")
    concepts, data = adapter.load_data(hors_dusage_percentage=30)
    elements = []
    for item in data:
        elements.append(item[1])
    print("Concepts")
    print(concepts)
    af = AF()
    cf = CF()
    td = TD()
    bayes = bayesian()

    af_weights = af.calculate_AF(concepts, elements)
    print("AF Weights")
    print(af_weights)
    cf_weights = cf.calculate_CF(concepts, elements)
    print("CF Weights")
    print(cf_weights)
    td_weights = td.calculate_td()
    print("TD Weights")
    print(td_weights)
    bayesian_weights = bayes.calculate_bayesian()
    print("bayesian Weights")
    print(bayesian_weights)

    print('─' * 10," After nomalization", '─' * 10)
    af_weights = weight_to_relevance(af_weights)
    cf_weights = weight_to_relevance(cf_weights)
    td_weights = weight_to_relevance(td_weights)
    bayesian_weights = weight_to_relevance(bayesian_weights)
    print("AF Weights")
    print(af_weights)
    print("CF Weights")
    print(cf_weights)
    print("TD Weights")
    print(td_weights)
    print("bayesian Weights")
    print(bayesian_weights)
    od1 = collections.OrderedDict(sorted(td_weights.items()))
    od2 = collections.OrderedDict(sorted(bayesian_weights.items()))
    print("TD Weights")
    print(od1)
    print("bayesian Weights")
    print(od2)


