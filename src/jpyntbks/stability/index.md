---
nav_order: 2
title: Stability of Linear Systems
subtitle: 
summary: Module 2
---
## Link to Notebook

[Stability of Linear Systems Notebook](/jpyntbks/stability/Stability.ipynb)

## Notebook Content

This notebook explores the Lyapunov equation and stability of linear systems. 

Again, we use the linearized pendulum dynamics as an example, and design a
proportional-derivative (PD) controller and assess the performance using the
Lyapunov equation. 

<img src="https://latex.codecogs.com/gif.latex?\dot{\theta}=\phi " />
<img
src="https://latex.codecogs.com/gif.latex?\dot{\phi}=-\frac{g}{\ell}\sin(\theta) " />

!!! info 
    You will need to make sure you append to your path
    the directory where you have the notebooks and utils folder so that you can use 
    the utils functions in '_547utils.py'. You may also want to install
    [seaborn](https://seaborn.pydata.org/) for nice plotting style.
