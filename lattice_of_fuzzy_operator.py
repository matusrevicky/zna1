# Uloha podla clanku https://www.inf.upol.cz/downloads/BeDeOuVy_Claffco.pdf, naprogramovat algoritmus na lattice

# Poznamka: kody su pisane tak, aby sa lahko debugovali a boli co najnazornejsie, nie najoptimalnejsie
# Poznamka2: v funguje s fuzzy, najde aj lattice

# B su atributy napr. B={0/y1, 0/y2, 0.5/y3, 0.5/y4, 1/y5}
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from utils.base_methods import arrowUp, arrowDown, load_fuzzy

def neighbors(df, B, possible_Y_values):
    B_smaller_than_1_elements = []
    U = set()
    Min = set()
    for idx, attribute_value in enumerate(B):
        if attribute_value < 1.0:
            Min.add((idx, attribute_value))
            B_smaller_than_1_elements.append((idx, attribute_value))
    for y in B_smaller_than_1_elements:
        D = y_in_square_brackets_C_B(df, B, possible_Y_values, y)
        Increased = smaller_than_D_diff_from_y(D, B, y)
        c = Min.intersection(Increased)
        # is intersection empty?
        if not bool(c):
            U.add(tuple(D))
        else:
            Min.remove(y)
        # print(D, Increased)
    return U


# napr B=[0/y1, 0/y2, 0.5/y3, 0.5/y4, 1/y5], D=[0.5, 0.5, 0.5, 1.0, 1.0]
def smaller_than_D_diff_from_y(D, B, y):
    Inc = set()
    index = 0
    for b, d in zip(B, D):
        if index != y[0] and b < d:
            Inc.add((index, b))
        index = index + 1
    return Inc


# pole B sa upravi tak, ze na danom indexe sa nahradi prvkom s nasledujucou pravdivostnou hodnotou
# napr. B=[0/y1, 0/y2, 0.5/y3, 0.5/y4, 1/y5] a y=(idx=2,hodnota=0.5) tak B=[0/y1, 0/y2, 1/y3, 0.5/y4, 1/y5]
# Y je usporiadana mnozina pravdivostnych hodnot [0, 0.5, 1]
# dalsia hodnota od 0.5 je uz 1
def y_in_square_brackets_C_B(df, B, possible_Y_val, y):
    B_copy = []
    for element in B:
        B_copy.append(element)
    index_of_old_value = possible_Y_val.index(B_copy[y[0]])
    B_copy[y[0]] = possible_Y_val[index_of_old_value + 1]
    minimum_for_every_row = arrowDown(df, B_copy)
    minimum_for_every_column = arrowUp(df, minimum_for_every_row)
    return tuple(minimum_for_every_column)


def generate_from(df, B, Y, F, D_bottom_current, dictionary, possible_Y_values):

    D_bottom_next = set();

    # v  slovniku si mozem pamatat nasledovnikov pre kazdy uzol
    key = tuple(B)

    # pre toho kto uz nema nasledovnika vytvorim iba prazdny set
    dictionary[key] = set()

    while B != tuple(Y):
        B_star = neighbors(df, B, possible_Y_values)

        # v slovniku si mozem pamatat nasledovnikov pre kazdy uzol
        key = tuple(B)
        if key in dictionary:
            dictionary[key] = dictionary[key].union(B_star)
        else:
            dictionary[key] = B_star

        N = B_star - F
        for D in B_star:
            D_bottom_next.add(tuple(B))
            if D in N:
                F.add(D)
        for D in N:
            generate_from(df, D, Y, F, D_bottom_next, dictionary, possible_Y_values)
        # tato cast sice v clanku chyba, ale bez nej nikdy neskonci
        if not bool(N):
            break
    return


def lattice(df, Y, possible_Y_values):
    F = set()
    # ma byt prazdna mnozina, teda vsetky 0
    only_zeroes_rows = [0 for i in range(len(df.columns))]
    B = arrowUp(df, arrowDown(df, only_zeroes_rows))
    F.add(tuple(B))

    D_bottom_current = set()

    lattice_dict = dict()
    generate_from(df, B, Y, F, D_bottom_current, lattice_dict, possible_Y_values)
    return F, lattice_dict


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    data = load_fuzzy("data_files/data_from_article.csv")

    #  ked sa meni dataset, treba skontrolovat ake su tam fuzzy hodnoty
    possible_Y_val = [0, 0.5, 1]
    Y = [1 for i in range(len(data.columns))]

    concepts, lattice = lattice(data, Y, possible_Y_val)

    print("Formalne koncepty:")
    pp.pprint(concepts)
    print("Lattice (uzol:nasledovnici):")
    pp.pprint(lattice)

    # interaktivny graf
    from networkx_viewer import Viewer
    G = nx.Graph(lattice)
    # funguje vo verzii decorator 4.4.2
    nx.draw(G, with_labels=True)
    plt.show()
    # app = Viewer(G)
    # app.mainloop()

    # Formalne koncepty:
    # {(0.0, 0.0, 0.5, 0.5, 0.5),
    #  (0.0, 0.0, 0.5, 0.5, 1.0),
    #  (0.5, 0.5, 0.5, 1.0, 0.5),
    #  (0.5, 0.5, 0.5, 1.0, 1.0),
    #  (0.5, 0.5, 1.0, 1, 0.5),
    #  (0.5, 0.5, 1.0, 1, 1),
    #  (1.0, 0.5, 0.5, 1.0, 0.5),
    #  (1.0, 0.5, 0.5, 1.0, 1.0),
    #  (1, 1.0, 1.0, 1, 0.5),
    #  (1, 1.0, 1.0, 1, 1)}
    # Lattice(uzol: nasledovnici):
    # {(0.0, 0.0, 0.5, 0.5, 0.5): {(0.0, 0.0, 0.5, 0.5, 1.0),
    #                              (0.5, 0.5, 0.5, 1.0, 0.5)},
    #  (0.0, 0.0, 0.5, 0.5, 1.0): {(0.5, 0.5, 0.5, 1.0, 1.0)},
    #  (0.5, 0.5, 0.5, 1.0, 1.0): {(1.0, 0.5, 0.5, 1.0, 1.0), (0.5, 0.5, 1.0, 1, 1)},
    #  (1.0, 0.5, 0.5, 1.0, 1.0): {(1, 1.0, 1.0, 1, 1)},
    #  (1, 1.0, 1.0, 1, 1): set(),
    #  (0.5, 0.5, 1.0, 1, 1): {(1, 1.0, 1.0, 1, 1)},
    #  (0.5, 0.5, 0.5, 1.0, 0.5): {(0.5, 0.5, 0.5, 1.0, 1.0),
    #                              (0.5, 0.5, 1.0, 1, 0.5),
    #                              (1.0, 0.5, 0.5, 1.0, 0.5)},
    #  (1.0, 0.5, 0.5, 1.0, 0.5): {(1, 1.0, 1.0, 1, 0.5), (1.0, 0.5, 0.5, 1.0, 1.0)},
    #  (1, 1.0, 1.0, 1, 0.5): {(1, 1.0, 1.0, 1, 1)},
    #  (0.5, 0.5, 1.0, 1, 0.5): {(1, 1.0, 1.0, 1, 0.5), (0.5, 0.5, 1.0, 1, 1)}}



