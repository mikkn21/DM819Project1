## First Project of the Course DM819 Computational Geometry

This project was developed together with my fellow student [@Caerullean](https://github.com/Caerullean).

The geometric problem we are solving in this project is problem 2.14 from our course textbook *Computational Geometry: Algorithms and Applications (3rd Edition)*. 

> [!Note]
> For a more detailed description of the project and code, I recommend reading the [rapport](./DM819__Part_1.pdf).


**Problem Description**:

Given a set of $n$ disjoint line segments in the plane and a fixed point $p$ (not lying on any segment), the goal is to determine which segments are visible from $p$. A segment is considered visible if there exists a point on it that can be connected to $p$ by a straight line that does not intersect any other segment. The task is to design an algorithm that solves this problem in $O(n \log n)$ time using a rotating half-line (**sweep-line**) approach pivoting around $p$.


> [!IMPORTANT]
> Please note that the git commit history might not fully reflect the individual contributions, as we pair programmed using the [VS Code Live Share extension](https://marketplace.visualstudio.com/items/?itemName=MS-vsliveshare.vsliveshare).


> **Citation:**  
> de Berg, M., Cheong, O., van Kreveld, M., & Overmars, M. (2008). *Computational Geometry: Algorithms and Applications* (3rd ed.). Springer.



