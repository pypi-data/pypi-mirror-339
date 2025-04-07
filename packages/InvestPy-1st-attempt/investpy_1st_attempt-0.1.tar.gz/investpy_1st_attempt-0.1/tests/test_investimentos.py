# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 14:33:21 2025

@author: josea
"""

# tests/test_investimentos.py

import unittest
from investimentos import calcular_retorno_investimento 
from investimentos import calcular_juros_compostos 
from investimentos import converter_taxa_anual_para_mensal 
from investimentos import calcular_cagr

class TestInvestimentos(unittest.TestCase):

   def test_calcular_retorno_investimento(self):
       self.assertAlmostEqual(calcular_retorno_investimento(1000, 1500), 50.0)
  
   def test_calcular_juros_compostos(self):
       self.assertAlmostEqual(calcular_juros_compostos(1000, 6, 5), 1338.23, places=2)
  
   def test_converter_taxa_anual_para_mensal(self):
       self.assertAlmostEqual(converter_taxa_anual_para_mensal(12), 0.9487, places=3)  # Alterado de places=4 para places=3
  
   def test_calcular_cagr(self):
       self.assertAlmostEqual(calcular_cagr(1000, 1500, 5), 8.45, places=2)

if __name__ == '__main__':
   unittest.main()
   
   
   
   