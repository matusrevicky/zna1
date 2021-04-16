import pandas as pd
import numpy as np

def load_fuzzy(csv_file_path):
    df = pd.read_csv(csv_file_path, index_col=0)
    return df


def fuzzy_implication(a, b):
    return min(1 - a + b, 1)


def fuzzy_and(a, b):
    return max(0, a + b - 1)


# pre dane riadky, robim implikacie a hladam minimum z tychto implikacii
def arrowUp(df, minimum_for_every_row):
    # df['new_col'] = np.array(minimum_for_every_row)
    final_min_array = []
    minimum = 1000
    for j in range(len(df.columns)):
        # print('column index:', column)
        for i in range(len(df.index)):
            a = minimum_for_every_row[i]
            b = df.iloc[i][j]
            after_implication = fuzzy_implication(a, b)
            if after_implication < minimum:
                minimum = after_implication
            # print('\t', a, '->', b, '=', after_implication)
        final_min_array.append(minimum)
        minimum = 1000
    return final_min_array


# dane su stlpce a hranicne hodnoty pre vsetky stlpce a hladam riadky, ktore su nad hranicnou hodnotou
# funkcia ktora priradi kazdemu objektu hodnoty z intervalu [0,1]
# prechadzame cez vsetky atributy a vyberame minima cez implikaciu
def arrowDown(df, treshold_array):
    if len(treshold_array) != len(df.columns):
        print("amount of columns does not match amount of suplied treshold values!!!")
        return

    list = []
    # pre kazdy riadok sprav implikacie a vyber minimum
    for i in range(len(df.index)):
        minimum = 1000
        # print('row index', row)
        for j in range(len(df.columns)):
            a = treshold_array[j]
            b = df.iloc[i][j]
            # if i > 300:
            #     print("b",  b)
            after_implication = fuzzy_implication(a, b)
            if after_implication < minimum:
                minimum = after_implication
            # print('\t', a, '->', b, '=', after_implication)
        list.append(minimum)

    return list
