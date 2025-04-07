# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 14:14:23 2025

@author: josea
"""


# investimento.py


def calcular_retorno_investimento(val_init, val_final):
    """
    Calcula percentual de lucro de investimento

    Parameters
    ----------
    val_init : float
        valor inicial de investimento.
    val_final : float
        valor final após rendimento.

    Returns
    -------
    float
        Percentual de ganho (lucro) de investimento.

    """
    return (val_final - val_init)/val_init * 100



def calcular_juros_compostos(val_init, taxa_juros_anual, tempo):
    """
    Calcula juros compostos ao final de determinado tempo
    para um dado o valor inicial de investimento

    Parameters
    ----------
    val_init : float
        valor inicial de investimento.
    taxa_juros_anual : float
        taxa de juros anual em porcentagem.
    tempo : int
        número de anos de investimento.

    Returns
    -------
    val_final : float
        valor final do investimento.

    """
    taxa_juros_decimal = taxa_juros_anual/100
    val_final = val_init * (1 + taxa_juros_anual)**tempo
    return val_final


def converter_taxa_anual_para_mensal(taxa_anual):
   """
   Converte uma taxa de juros anual para mensal.

   Args:
       taxa_anual (float): Taxa de juros anual em porcentagem.

   Returns:
       float: Taxa de juros mensal em porcentagem.
   """
   taxa_mensal = (1 + taxa_anual / 100) ** (1 / 12) - 1
   return taxa_mensal * 100


def calcular_cagr(valor_inicial, valor_final, anos):
   """
   Calcula a taxa de crescimento anual composta (CAGR).

   Args:
       valor_inicial (float): Valor inicial do investimento.
       valor_final (float): Valor final do investimento.
       anos (int): Número de anos.

   Returns:
       float: CAGR em porcentagem.
   """
   cagr = ((valor_final / valor_inicial) ** (1 / anos) - 1) 
   return cagr * 100


    
    
    
    