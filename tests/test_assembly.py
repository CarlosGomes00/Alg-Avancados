# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest

from genomeassembly.genomeassembly import *

class TestAssemblyGraph(unittest.TestCase):
    """
    Conjunto de testes para a classe AssemblyGraph que lida com o processo de montagem de genomas.
    """
    def test_k_merify(self):
        """
        Testa a função k_merify para garantir que as sequências são divididas corretamente em k-mers.

        """
        seq = 'ACGT'
        k = 3
        self.assertEqual(k_merify(seq, k), ['ACG', 'CGT'])

    def test_valid_path(self):
        """
        Testa o método valid_path da classe AssemblyGraph.
        """
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        grafo = AssemblyGraph(frags)
        path = 'ACC-2 CCA-8 CAT-5 ATG-3'.split()
        path2 = 'ACC-2 CCA-8 CAT-5 ATG-3 TGG-13 GGC-10 GCA-9 CAT-6 ATT-4 TTT-15 TTC-14 TCA-12 CAT-7 ATA-1 TAA-11'.split()
        self.assertTrue(grafo.valid_path(path))
        self.assertTrue(grafo.valid_path(path2))

    def test_is_hamiltonian(self):
        """
        Testa o método is_hamiltonian da classe AssemblyGraph.
        """
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        grafo = AssemblyGraph(frags)
        path = 'ACC-2 CCA-8 CAT-5 ATG-3'.split()
        path2 = 'ACC-2 CCA-8 CAT-5 ATG-3 TGG-13 GGC-10 GCA-9 CAT-6 ATT-4 TTT-15 TTC-14 TCA-12 CAT-7 ATA-1 TAA-11'.split()
        self.assertFalse(grafo.is_hamiltonian(path))
        self.assertTrue(grafo.is_hamiltonian(path2))

    def test_hamiltonian_reconstruction(self):
        """
        Testa o método hamiltonian_reconstruction da classe AssemblyGraph.
        """
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        grafo = AssemblyGraph(frags)
        path = 'ACC-2 CCA-8 CAT-5 ATG-3'.split()
        path2 = 'ACC-2 CCA-8 CAT-5 ATG-3 TGG-13 GGC-10 GCA-9 CAT-6 ATT-4 TTT-15 TTC-14 TCA-12 CAT-7 ATA-1 TAA-11'.split()
        self.assertIsNone(grafo.hamiltonian_reconstruction(path))
        self.assertEqual(grafo.hamiltonian_reconstruction(path2), 'ACCATGGCATTTCATAA')

    def test_get_hamiltonian_paths(self):
        """
        Testa o método get_hamiltonian_paths da classe AssemblyGraph.
        """
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        grafo = AssemblyGraph(frags)
        paths = grafo.get_hamiltonian_paths()
        self.assertTrue(isinstance(paths, list))

    def test_full_reconstruction(self):
        """"
        Testa o processo completo de reconstrução do genoma.
        """
        seq = "CAATCATGATGATGATC"
        frags = k_merify(seq, 3)
        teste = AssemblyGraph(frags)
        paths = teste.get_hamiltonian_paths()
        recons = []
        if isinstance(paths, list) and len(paths) > 1:
            for path in paths:
                recons.append(teste.hamiltonian_reconstruction(path))
        else:
            recons.append(teste.hamiltonian_reconstruction(paths))
        self.assertIn(seq, recons)

if __name__ == '__main__':
    unittest.main(verbosity=2)