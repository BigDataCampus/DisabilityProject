import pandas as pd
from sklearn.neighbors import NearestNeighbors

dummy = pd.read_csv('dummy.csv')
dummy.drop('Unnamed: 0', axis=1, inplace=True)
def contentCF(lat, lng):
    X = dummy.iloc[:, 1:]
    nbrs = NearestNeighbors().fit(X)
    t = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,lat, lng]
    print(nbrs.kneighbors([t]))

    return nbrs.kneighbors([t])[1][0]