# Collision-Probabilities
Quick and dirty script to calculate formulas for probabilities that respect the probabilities of all the states a system could be in and their implications.

# Example usage
```shell
$ python test.py 5

5⋅(v - 4)⋅(v - 3)⋅(v - 2)⋅(v - 1)   40⋅(v - 3)⋅(v - 2)⋅(v - 1)   75⋅(v - 2)⋅(v - 1)   30⋅(v - 1)   1 
───────────────────────────────── + ────────────────────────── + ────────────────── + ────────── + ──
                 5                               5                        5                5        5
                v                               v                        v                v        v 

   4       3       2          
5⋅v  - 10⋅v  + 10⋅v  - 5⋅v + 1
──────────────────────────────
               5              
              v               

Python string: (5*v**4 - 10*v**3 + 10*v**2 - 5*v + 1)/v**5
Wolfram alpha code: (5*v^4 - 10*v^3 + 10*v^2 - 5*v + 1)/v^5
Latex code: \frac{(5 \cdot v^4 - 10 \cdot v^3 + 10 \cdot v^2 - 5 \cdot v + 1)}{v^5}
```
