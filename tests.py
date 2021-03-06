import unittest

from find_factors import find_factors
from lattice import lattice
from naive_concepts import all_repeat, for_given_combinations_do_fuzzy_implication, naive_formal_concepts
from next_neighbours import next_neighbours
from object_intersection import object_intersection
from rice_siff import fuzzyfy, rice_siff
from utils.base_methods import load_fuzzy


# Vsetky testy su na datach z clankov
class UserModelCase(unittest.TestCase):

    def test_verifyNaiveConcepts(self):
        expected = {((0.5, 0.5, 0.0), (1, 1.0, 1.0, 1, 1)),
                    ((0.5, 0.5, 0.5), (0.5, 0.5, 1.0, 1, 1)),
                    ((0.5, 1, 0.0), (1, 1.0, 1.0, 1, 0.5)),
                    ((0.5, 1, 0.5), (0.5, 0.5, 1.0, 1, 0.5)),
                    ((1.0, 0.5, 0.0), (1.0, 0.5, 0.5, 1.0, 1.0)),
                    ((1, 0.5, 0.5), (0.5, 0.5, 0.5, 1.0, 1.0)),
                    ((1, 0.5, 1.0), (0.0, 0.0, 0.5, 0.5, 1.0)),
                    ((1.0, 1.0, 0.0), (1.0, 0.5, 0.5, 1.0, 0.5)),
                    ((1, 1, 0.5), (0.5, 0.5, 0.5, 1.0, 0.5)),
                    ((1, 1, 1.0), (0.0, 0.0, 0.5, 0.5, 0.5))}

        possible_Y_values = [0.0, 0.5, 1.0]
        data = load_fuzzy("data_files/data_from_article.csv")
        formal_concepts = naive_formal_concepts(data, possible_Y_values)
        self.assertSetEqual(formal_concepts, expected)

    def test_lattice_of_fuzzy_operator(self):
        expected_concepts = {(0.0, 0.0, 0.5, 0.5, 0.5),
                             (0.0, 0.0, 0.5, 0.5, 1.0),
                             (0.5, 0.5, 0.5, 1.0, 0.5),
                             (0.5, 0.5, 0.5, 1.0, 1.0),
                             (0.5, 0.5, 1.0, 1, 0.5),
                             (0.5, 0.5, 1.0, 1, 1),
                             (1.0, 0.5, 0.5, 1.0, 0.5),
                             (1.0, 0.5, 0.5, 1.0, 1.0),
                             (1, 1.0, 1.0, 1, 0.5),
                             (1, 1.0, 1.0, 1, 1)}

        expected_lattice = {(0.0, 0.0, 0.5, 0.5, 0.5): {(0.0, 0.0, 0.5, 0.5, 1.0),
                                                        (0.5, 0.5, 0.5, 1.0, 0.5)},
                            (0.0, 0.0, 0.5, 0.5, 1.0): {(0.5, 0.5, 0.5, 1.0, 1.0)},
                            (0.5, 0.5, 0.5, 1.0, 1.0): {(1.0, 0.5, 0.5, 1.0, 1.0), (0.5, 0.5, 1.0, 1, 1)},
                            (1.0, 0.5, 0.5, 1.0, 1.0): {(1, 1.0, 1.0, 1, 1)},
                            (1, 1.0, 1.0, 1, 1): set(),
                            (0.5, 0.5, 1.0, 1, 1): {(1, 1.0, 1.0, 1, 1)},
                            (0.5, 0.5, 0.5, 1.0, 0.5): {(0.5, 0.5, 0.5, 1.0, 1.0),
                                                        (0.5, 0.5, 1.0, 1, 0.5),
                                                        (1.0, 0.5, 0.5, 1.0, 0.5)},
                            (1.0, 0.5, 0.5, 1.0, 0.5): {(1, 1.0, 1.0, 1, 0.5), (1.0, 0.5, 0.5, 1.0, 1.0)},
                            (1, 1.0, 1.0, 1, 0.5): {(1, 1.0, 1.0, 1, 1)},
                            (0.5, 0.5, 1.0, 1, 0.5): {(1, 1.0, 1.0, 1, 0.5), (0.5, 0.5, 1.0, 1, 1)}}

        data = load_fuzzy("data_files/data_from_article.csv")
        possible_Y_val = [0, 0.5, 1]
        concepts1, lattice1 = lattice(data, possible_Y_val)

        self.assertDictEqual(lattice1, expected_lattice)
        self.assertSetEqual(concepts1, expected_concepts)

    def test_verifyNextNeighbours(self):
        expected_vertices = {((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                             ((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1)),
                             ((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
                             ((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
                             ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0)),
                             ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
                             ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0)),
                             ((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0)),
                             ((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
                             ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
                             ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0)),
                             ((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
                             ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0)),
                             ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0)),
                             ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0)),
                             ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))}

        expected_edges = {(((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1))),
                          (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0))),
                          (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0))),
                          (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0))),
                          (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                           ((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0))),
                          (((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1)),
                           ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
                           ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
                           ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0))),
                          (((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
                           ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
                           ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0)),
                           ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
                           ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0))),
                          (((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
                           ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0))),
                          (((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0)),
                           ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
                          (((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0)),
                           ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0))),
                          (((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
                           ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0))),
                          (((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
                           ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0))),
                          (((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
                           ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0))),
                          (((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
                           ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0))),
                          (((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0)),
                           ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
                          (((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
                           ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0))),
                          (((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
                           ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0))),
                          (((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0)),
                           ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
                          (((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0)),
                           ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0))),
                          (((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0)),
                           ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0)))}

        data = load_fuzzy("data_files/intersection.csv")
        vertices, edges = next_neighbours(data)
        self.assertSetEqual(vertices, expected_vertices)
        self.assertSetEqual(edges, expected_edges)

    def test_object_Intersection(self):
        expected = [((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
                    ((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
                    ((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
                    ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0)),
                    ((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0)),
                    ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0)),
                    ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0)),
                    ((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
                    ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0)),
                    ((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
                    ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0)),
                    ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
                    ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
                    ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0)),
                    ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0)),
                    ((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1))]

        data = load_fuzzy("data_files/intersection.csv")
        result = object_intersection(data)
        self.assertListEqual(result, expected)

    def test_find_factors(self):
        expected = {((0.5, 1.0, 1.0, 0.5, 0.75),
                     (1.0, 1, 0.75, 0.75, 0.5, 1, 0.5, 0.25, 0.25, 0.5)),
                    ((0.75, 0.5, 0.75, 1.0, 0.5),
                     (0.5, 0.5, 0.75, 1, 0.75, 0.5, 0.75, 0.25, 0.5, 1.0)),
                    ((0.75, 0.5, 1, 0.75, 0.75),
                     (0.75, 0.75, 0.75, 0.75, 1.0, 0.75, 0.5, 0.25, 0.25, 0.75)),
                    ((0.75, 0.75, 1, 0.75, 0.25),
                     (0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 1.0, 0.25, 0.25, 0.75)),
                    ((1.0, 0.75, 0.25, 0.5, 0.25),
                     (0.5, 1.0, 1.0, 1.0, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75)),
                    ((1.0, 0.75, 0.75, 0.5, 1),
                     (0.5, 0.75, 0.5, 0.5, 0.75, 1.0, 0.25, 0.5, 0.25, 0.75)),
                    ((1.0, 1, 0.25, 0.5, 0.25),
                     (0.5, 1.0, 0.75, 0.75, 0.5, 1.0, 0.75, 0.5, 1.0, 0.5))}

        data = load_fuzzy("data_files/olympic.csv")
        possible_fuzzy_values = [0, 0.25, 0.5, 0.75, 1]
        concepts = find_factors(data, possible_fuzzy_values)
        self.assertSetEqual(concepts, expected)

    # takes 113.061s
    def test_rice_siff(self):
        expected = {
            ('D06', 'D09'),
            ('D10', 'D03'),
            ('Ch23', 'Ch07', 'Ch03'),
            ('Ch03',),
            ('Ch22', 'Ch01', 'Ch05', 'Ch18'),
            ('Ch05',),
            ('D01', 'D06', 'D02', 'D09'),
            ('Ch22',),
            ('Ch06', 'Ch10', 'Ch02'),
            ('D08', 'D03'),
            ('D02',),
            ('D04',),
            ('Ch14',),
            ('Ch01',),
            ('D01', 'D06'),
            ('Ch15',),
            ('Ch08', 'Ch16'),
            ('Ch23', 'Ch07', 'Ch12', 'Ch03'),
            ('Ch18', 'Ch01', 'Ch05', 'Ch08', 'Ch16', 'Ch22'),
            ('Ch21', 'Ch14', 'D11'),
            ('D09', 'Ch05', 'D03', 'D08', 'Ch11', 'D01', 'Ch21', 'D07', 'D06', 'D10', 'D02', 'Ch17', 'Ch22', 'Ch09',
             'Ch07', 'Ch18', 'Ch23', 'Ch16', 'D04', 'Ch01', 'Ch08', 'D05', 'D11', 'Ch14'),
            ('Ch23',),
            ('Ch23', 'Ch07'),
            ('D06',),
            ('Ch04', 'Ch20'),
            ('Ch21',),
            ('Ch16',),
            ('Ch21', 'Ch22', 'Ch07', 'Ch18', 'D10', 'Ch01', 'Ch05', 'Ch08', 'Ch16', 'D11', 'Ch11', 'Ch09', 'Ch14'),
            ('Ch21', 'Ch07', 'Ch10', 'Ch12', 'Ch03', 'Ch02', 'Ch15', 'D10', 'Ch23', 'Ch05', 'Ch13', 'Ch06', 'Ch14'),
            ('Ch10', 'Ch12', 'Ch03', 'D09', 'Ch05', 'D03', 'D08', 'Ch11', 'Ch06', 'D01', 'Ch21', 'D07', 'D06', 'D10',
             'D02', 'Ch17', 'Ch22', 'Ch09', 'Ch04', 'Ch07', 'Ch02', 'Ch18', 'Ch23', 'Ch16', 'D04', 'Ch20', 'Ch15',
             'Ch01', 'Ch08', 'D05', 'Ch13', 'D11', 'Ch19', 'Ch14'),
            ('Ch09',),
            ('D07', 'D06', 'D09', 'D10', 'D02', 'D05', 'D04', 'D01'),
            ('D09', 'Ch05', 'D03', 'D08', 'Ch11', 'D01', 'Ch21', 'D07', 'D06', 'D10', 'D02', 'Ch22', 'Ch09', 'Ch07',
             'Ch18', 'Ch23', 'Ch16', 'D04', 'Ch01', 'Ch08', 'D05', 'D11', 'Ch14'),
            ('Ch11',),
            ('Ch20',),
            ('Ch11', 'Ch17'),
            ('D10',),
            ('Ch21', 'Ch14'),
            ('Ch10',),
            ('D07', 'D06', 'D09', 'D10', 'D02', 'D03', 'D05', 'D04', 'D08', 'D01'),
            ('Ch05', 'Ch18'),
            ('Ch07', 'Ch12', 'Ch03', 'Ch23', 'Ch13'),
            ('Ch01', 'Ch05', 'Ch18'),
            ('D10', 'D08', 'D03'),
            ('Ch04', 'Ch19', 'Ch20'),
            ('Ch21', 'Ch07', 'D11', 'Ch11', 'Ch09', 'Ch14'),
            ('Ch08',),
            ('D01', 'D06', 'D09'),
            ('Ch02',),
            ('Ch06',),
            ('D05', 'D07', 'D10', 'D04'),
            ('Ch03', 'D09', 'Ch05', 'D03', 'D08', 'Ch11', 'D01', 'Ch21', 'D07', 'D06', 'D10', 'D02', 'Ch17', 'Ch22',
             'Ch09', 'Ch04', 'Ch07', 'Ch02', 'Ch18', 'Ch23', 'Ch16', 'D04', 'Ch20', 'Ch01', 'Ch08', 'D05', 'D11',
             'Ch19', 'Ch14'),
            ('Ch13',),
            ('Ch04',),
            ('D03',),
            ('Ch18',),
            ('Ch21', 'Ch07', 'D11', 'Ch09', 'Ch14'),
            ('D11',),
            ('D05', 'D07'),
            ('Ch07', 'Ch10', 'Ch12', 'Ch03', 'Ch02', 'Ch23', 'Ch13', 'Ch06'),
            ('Ch07',),
            ('Ch12',),
            ('D07',),
        }

        data = load_fuzzy("data_files/ziaci.csv")
        data = data.applymap(fuzzyfy)
        result = rice_siff(data)

        sortset_expected = set()
        for expect in expected:
            sortset_expected.add(tuple(sorted(expect)))

        sortset_result = set()
        for res in result:
            sortset_result.add(tuple(sorted(res)))

        self.assertSetEqual(sortset_result, sortset_expected)


if __name__ == '__main__':
    unittest.main(verbosity=1)
