# Algoritmo de atribuição de resistência a erros

## Sumário
 - [Resumo](#resumo)
 - [Hamming](#hamming)
 - [Organização do código](#organização-e-funcionamento-do-código)
   - [Diretórios](#diretórios)

## Resumo
 Este repositório se trata de um trabalho da disciplina Fundamentos de Informática do curso de Bacharelado em Ciência da Computação do Instituto Federal Catarinense Campus Blumenau. <br>

 O trabalho envolve um algoritmo que atribui, a um dado arquivo, resistência a erros por meio do Código de Hamming. <br>

## Hamming
 ![](img/quadro-hamming.png)

 Para mais informações, acesse a [página da Wikipedia](https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Hamming) que descreve o Código de Hamming

## Organização e funcionamento do código

 ### Diretórios
 * `files`: Armazena os arquivos manueados pelo algoritmo.
 * `source`: Possui o código-fonte do algoritmo.

 ### Sender
 Caminho: `source\sender.py`
 Módulo que aplica codificação de Hamming a um arquivo qualquer e o converte para um arquivo de texto em binário. O arquivo de texto gerado é cerca de 12 vezes maior que o arquivo orginal.

 ### Receiver
 Caminho: `source\receiver.py`
 Lê um arquivo de texto codificado, decodifica e converte de volta para o arquivo original. <br>
 Ao converter o arquivo de texto codificado de volta para o arquivo original, ao ler cada quadro o algoritmo:
 - Extrai os bits de dados do quadro e os escreve se não houver erros.
 - Corrige o quadro, extrai os bits de dados e os escreve se houver 1 erro.
 - Escreve uma sequência de 11 bits desligados ('00000000000') se o quadro tiver 2 erros ou mais.

 Limitações: 
 - Se o algoritmo detectar uma quantidade de erros ímpar diferente de 1, ele tentará corrigir o quadro e escreverá seus bits de dados na conversão para o arquivo original. Desta forma, o arquivo original se corrompe.
 - 