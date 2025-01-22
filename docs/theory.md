# Theory: Convergence of the Chaos Game to the Sierpinski Triangle

> Copyright (c) 2025. Licensed under MIT License.

## Introduction

The chaos game is a simple iterative process that remarkably generates the Sierpinski triangle. This document provides a formal mathematical proof of why this occurs.

## Definitions

### Definition 1: The Chaos Game
Let T be an equilateral triangle with vertices v₁, v₂, v₃. The chaos game consists of:
1. Selecting an initial point p₀
2. Iteratively generating points pₙ by:
   - Randomly selecting a vertex vᵢ
   - Setting pₙ as the midpoint between pₙ₋₁ and vᵢ

### Definition 2: Sub-triangle at Prefix x
For a ternary string x, a sub-triangle T(x) with vertices {v₁(x), v₂(x), v₃(x)} is defined recursively:
- T(ε) is the base triangle (empty prefix)
- T(x‖i) is the triangle formed by vᵢ(x) and the midpoints of its adjacent edges

### Definition 3: Sierpinski Triangle
The Sierpinski triangle S(x) at prefix x is defined recursively as:
S(x) = T(x) ∪ S(x‖1) ∪ S(x‖2) ∪ S(x‖3)

## Mathematical Representation

### Tridrant Notation
Any Sierpinski sub-triangle can be uniquely identified using a ternary string representing its path:
- Each digit (1,2,3) represents which tridrant was chosen
- Empty string ε represents the base triangle
- String concatenation (x‖i) represents selecting tridrant i in sub-triangle x

For example: "132" represents:
1. First tridrant of base triangle
2. Third tridrant of resulting sub-triangle
3. Second tridrant of that sub-triangle

## Core Lemmas

### Lemma 1: Invariance Property
For any point p ∈ S and vertex v chosen by the chaos game, the resulting point p' also lies in S.

*Proof:*
Let x be the shortest prefix such that p ∈ S(x). When moving halfway to vertex v:
1. T(x) maps to T(v‖x)
2. By definition, T(v‖x) ⊂ S
∴ p' ∈ S

*Example:*
Consider a point p = (0.25, 0.25) in the Sierpinski triangle:
- If v₁ = (0, 0) is chosen, p' = (0.125, 0.125)
- If v₂ = (1, 0) is chosen, p' = (0.625, 0.125)
- If v₃ = (0.5, 0.866) is chosen, p' = (0.375, 0.558)
All resulting points remain within the fractal.

### Lemma 2: Distance Convergence
For any point p ∉ S, let p* be its closest point in S. After n steps:
d(pₙ, pₙ*) ≤ (1/2)ⁿ d(p₀, p₀*)

*Proof:*
Each iteration halves the distance between corresponding points:
d(pₙ₊₁, pₙ₊₁*) = ∥(pₙ + v)/2 - (pₙ* + v)/2∥ = d(pₙ, pₙ*)/2

*Example:*
Start with p₀ = (0.4, 0.4) ∉ S
- Initially d₀ = 0.1 (distance to nearest point in S)
- After 3 iterations: d₃ ≤ 0.0125
- After 10 iterations: d₁₀ ≤ 0.0001

### Lemma 3: Complete Coverage
For any point q ∈ S and ε > 0, the probability of the chaos game visiting a point within ε of q approaches 1.

*Proof Sketch:*
1. Any point in S can be represented by an infinite ternary sequence
2. The chaos game generates random ternary sequences
3. By the law of large numbers, all finite prefixes occur with probability 1

*Example:*
To reach point q = (0.333, 0.289) ∈ S within ε = 0.01:
1. Need sequence: v₁, v₃, v₂, v₁, v₃
2. Probability ≈ (1/3)⁵ for this exact sequence
3. Multiple sequences lead to ε-neighborhood

## Convergence Properties

### Rate of Convergence
For a point p₀ starting distance d from S:
- After n steps: d_n ≤ d/2ⁿ
- To reach within ε: need approximately log₂(d/ε) steps
- Typical convergence in 600 steps for ε ≈ 10⁻³

## Additional Theoretical Results

### Hausdorff Dimension
The Sierpinski triangle has Hausdorff dimension:
D = log(3)/log(2) ≈ 1.585

*Proof Outline:*
1. Triangle splits into 3 self-similar copies
2. Each copy scaled by factor 1/2
3. D satisfies: 3 = (2)ᴰ

## Extended Properties

### Non-equilateral Triangles
The proof holds for any triangle because:
- Arguments are topological, not geometric
- Only relative positions matter
- Result is topologically equivalent but geometrically skewed

### Modified Ratios
For ratio λ ≠ 1/2:
- New fractal shapes emerge
- Convergence still occurs but to different attractors
- λ > 1/2: More "stretched" towards vertices
- λ < 1/2: More "compressed" towards center

## Conclusion

The chaos game converges to the Sierpinski triangle because:
1. Points on S remain on S (Lemma 1)
2. Points off S converge exponentially to S (Lemma 2)
3. All points in S are eventually approximated (Lemma 3)

## Extensions

The proof framework extends to:
- Non-equilateral triangles (via topological equivalence)
- Different ratios λ ≠ 1/2 (producing modified fractals)
- Other polygons (generating different recursive structures)

## Implementation Notes

### Numerical Considerations
- Due to floating-point arithmetic, points should be considered equal if their distance is below a small epsilon (typically 1e-10)
- After approximately 20 iterations, points off S become visually indistinguishable from points on S

### Interactive Demonstrations
The theoretical results can be verified using our interactive tools:
- Use `chaos_game.py` to visualize Lemma 1's invariance property
- `convergence_visualizer.py` demonstrates the exponential convergence from Lemma 2
- `coverage_analyzer.py` provides empirical evidence for Lemma 3

## Numerical Analysis

### Convergence Rate
For practical implementations:
- First 10 iterations: Rapid convergence towards S
- Next 100 iterations: Fine structure development
- Beyond 1000 iterations: Detail refinement

### Error Bounds
For a starting point p₀ with distance d₀ from S:
- After n iterations: dₙ ≤ d₀/2ⁿ
- To achieve precision ε: n ≥ log₂(d₀/ε)


## References

1. Barnsley, M. F. (1988). Fractals Everywhere. Academic Press.
2. Chaganty, A. T. (2020). "Why does the chaos game converge to the Sierpinski triangle?" Retrieved from https://arun.chagantys.org/technical/2020/04/28/chaos-game.html
3. Gleick, J. (1987). Chaos: Making a New Science. Viking Press.
4. Sierpiński, W. (1915). "Sur une courbe dont tout point est un point de ramification." Comptes Rendus de l'Académie des Sciences, 160, 302-305.
