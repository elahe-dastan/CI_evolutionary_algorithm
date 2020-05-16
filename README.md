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

## Structure
The first structure idea that pops to my and any one else's mind is using inheritance and that looks more appropriate<br/>
but the goal of this code is to get familiar with evolution and some algorithms frequently used in this field so to <br/>
show these objectives better I decided to have a class that just shows the evolution process and another class that<br/>
has the implementations of the algorithms I mentioned

## knapsack problem representation 
I think binary representation can be a good choice, the length of the chromosomes is equal to the number of weights,<br/>
each gene in the chromosome shows if its corresponding weight is selected or not by being zero or one.