# Introduction
In this repository I tried to solve two optimization problems using evolutionary algorithms.<br/>
The problems are [knapsack ptoblem](https://en.wikipedia.org/wiki/Knapsack_problem) and [traveling salesman](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

## Evolutionary Algorithm
These are the fixed steps in an evolutionary algorithm<br/>
1.define the representation<br/>
2.initiate the population<br/>
3.parent selection<br/>
4.children generation</br/>
5.children evaluation<br/>
6.next generation selection<br/>
7.check the stop condition, if not met repeat from step 3<br/><br/>
![FlowChart](images/Flowchart.png)

## knapsack problem representation 
I think binary representation can be a good choice, the length of the chromosomes is equal to the number of weights,<br/>
each gene in the chromosome shows if its corresponding weight is selected or not by being zero or one.