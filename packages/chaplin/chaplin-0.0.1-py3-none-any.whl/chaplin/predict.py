from chaplin.src import NNWrappers
from chaplin.src import parse
def run_prediction(seqs,printPreds=False):
    wrapper = NNWrappers.NNwrapper()
    wrapper.load()
    if type(seqs) is list:

        return wrapper.predict(seqs, scale_output=False)

    elif type(seqs) is str:
        seqs = parse.leggifasta(seqs)

    if type(seqs) is dict:
        names = []
        x = []
        for prot in seqs.keys():
            names += [prot]
            x += [[seqs[prot][i:i + 3] for i in range(0, len(seqs[prot]), 3)]]

    preds = wrapper.predict(x, scale_output=False)
    diz={}
    for k in range(len(names)):
        diz[names[k]] = preds[k]

    if printPreds:
        print("###########")
        print("# RESULTS #")
        for k in diz.keys():
            print(k,diz[k])
        print("###########")
    return diz