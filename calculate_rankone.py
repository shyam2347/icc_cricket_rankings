import operator
from os import listdir
from os.path import isfile, join
import sys

def getFirstRank(filename):
    with open(filename) as f:
        l = f.readline().split(',')
        if len(l) != 3 or l[0] is not '1':
            print('Bad file format: ', filename)
            return None
        return l[2].strip()

def calculate(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    #print(onlyfiles)
    mydict = {}
    for filename in onlyfiles:
        name = getFirstRank(path + '/' + filename)
        if name is None:
            continue
        if name in mydict:
            mydict[name] = mydict[name] + 1
        else:
            mydict[name] = 1
    sorted_dict = sorted(mydict.items(), key=operator.itemgetter(1))
    print(sorted_dict)

def main():
    calculate('csv')

if __name__ == '__main__':
     main()
