---
nav_order: 1
title: Solutions to LTI Systems in Python
subtitle: 
summary: Module 1
---

## Notebook Content

This notebook has examples of how to compute the matrix exponential and Jordan
form. 

It also implements Forward Euler and explores simulation through a pendulum
example.

```math
\begin{aligned}
\dot{\theta}&=\phi\\
\dot{\phi}&=-\frac{g}{\ell}\sin(\theta)
\end{aligned}
```


!!! info 
    You will need to make sure you append to your path
    the directory where you have the notebooks and utils folder so that you can use 
    the utils functions in '_547utils.py'. You may also want to install
    [seaborn](https://seaborn.pydata.org/) for nice plotting style.
