# Uloha2. najst si dataset, upravit na fuzzy(0,0.25,0.5,0.75,1), naprogramovat rice siff podla
# http://www.dataznalosti.cz/historie/2008/download/articles/znalosti2008-Krajci.pdf
import pandas as pd
import numpy as np

from utils.base_methods import load_fuzzy

# pre dane riadky, hladam minimum pre kazdy stlpec
def arrowUpRS(df, rowsId):
    final_min_array = []
    min = 1000
    for j, column in enumerate(df.columns):
        for i, row in enumerate(rowsId):
            current_min = df.loc[row][column]
            if current_min < min:
                min = current_min
        final_min_array.append(min)
        min = 1000
    return final_min_array


# dane su stlpce a hranicne hodnoty pre vsetky stlpce a hladam riadky, ktore su nad hranicnou hodnotou
def arrowDownRS(df, treshold_array):
    if len(treshold_array) != len(df.columns):
        print("amount of columns does not match amount of suplied treshold values!!!")
        return
    final_row_ids = set()
    for i, row in enumerate(df.index):
        are_all_bigger = True
        for j, column in enumerate(df.columns):
            if df.loc[row][column] < treshold_array[j]:
                are_all_bigger = False
                break
        if are_all_bigger:
            final_row_ids.add(row)
    return final_row_ids


def ro(df, rowIds1, rowIds2):
    # print(arrowUp(df,rowIds1))
    # print(arrowUp(df,rowIds2))
    arrowupVectorIds1 = arrowUpRS(df, rowIds1)
    arrowupVectorIds2 = arrowUpRS(df, rowIds2)

    minVector = np.minimum(arrowupVectorIds1, arrowupVectorIds2)
    maxVector = np.maximum(arrowupVectorIds1, arrowupVectorIds2)

    numerator = sum(minVector)
    denominator = sum(maxVector)
    # print(numerator, denominator)
    result = 1.0 - (numerator / denominator)
    return result


def generate_pairs(array):
    array = list(array)
    result = []
    for p1 in range(len(array)):
        for p2 in range(p1 + 1, len(array)):
            result.append([array[p1], array[p2]])
    return result


def cl(df, rows):
    return arrowDownRS(df, arrowUpRS(df, rows))


def findNearestNeighbour(df, allPairs):
    min = 1000
    for pair in allPairs:
        current_min = ro(df, list(pair[0]), list(pair[1]))
        if current_min < min:
            min = current_min

    edges_with_min_distance = []
    vertices = set()
    for pair in allPairs:
        if ro(df, list(pair[0]), list(pair[1])) == min:
            edges_with_min_distance.append(list(pair))
            vertices.add(pair[0])
            vertices.add(pair[1])

    return min, edges_with_min_distance, vertices


def multiUnion(df, E):
    resultset = set()
    for edge in E:
        setX1 = set(edge[0])
        setX2 = set(edge[1])
        setX1X2 = set().union(setX1).union(setX2)
        resultset.add(tuple(cl(df, list(setX1X2))))
    return resultset


def rice_siff(df):
    D = set()
    for row in df.index:
        D.add(tuple(cl(df, [row])))
    C = D.copy()
    while len(D) > 1:
        m, E, V = findNearestNeighbour(df, generate_pairs(D))
        N = multiUnion(df, E)
        difference = (D.difference(V))
        D = difference.union(N)
        C = C.union(N)
    return C

def fuzzyfy(x):
    return (x+3)/6

if __name__ == "__main__":
    # data = load_and_change_to_fuzzy(amount_of_rows=3)
    data = load_fuzzy("ziaci.csv")
    data = data.applymap(fuzzyfy)
    # print(arrowUp(data, [1233350, 572744]))
    # print(arrowDown(data, [0.4, 0.5, 0.6, 0.7, 0.7]))
    #
    # print(arrowDown(data, arrowUp(data, [1233350])))
    # print(ro(data, [1233350], [572744]))
    # print(generate_pairs(arrowDown(data, arrowUp(data, [1233350]))))
    result = rice_siff(data)
    print("Vysledok Rice-Siff algoritmu je mnozina vyslednych zhlukov {")
    for zhluk in result:
        print(zhluk,',')
    print("}")

    # Vysledok Rice-Siff algoritmu je mnozina vyslednych zhlukov {
    # (949504, 655300, 474212, 1233350, 388164, 572744, 680044, 1191504, 381330, 866584, 545918) ,
    # (949504, 680044) ,
    # (133536, 191854, 265960, 923616) ,
    # (866584,) ,
    # (949504, 741898, 381330, 866584, 133536, 388164, 655300, 1233350, 572744, 771276, 1191504, 724062, 923616, 889824, 474212, 265960, 680044, 191854, 471546, 545918) ,
    # (133536, 191854) ,
    # (949504, 1233350, 572744, 680044, 381330, 866584, 545918) ,
    # (133536,) ,
    # (572744, 866584) ,
    # (133536, 265960, 191854) ,
    # (949504, 866584, 381330, 680044) ,
    # }
    #
    # Process finished with exit code 0
