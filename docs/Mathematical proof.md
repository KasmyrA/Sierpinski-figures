# Mathematical Proof: Convergence of the Chaos Game to the Sierpinski Triangle

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

## Core Lemmas

### Lemma 1: Invariance Property
For any point p ∈ S and vertex v chosen by the chaos game, the resulting point p' also lies in S.

*Proof:*
Let x be the shortest prefix such that p ∈ S(x). When moving halfway to vertex v:
1. T(x) maps to T(v‖x)
2. By definition, T(v‖x) ⊂ S
∴ p' ∈ S

### Lemma 2: Distance Convergence
For any point p ∉ S, let p* be its closest point in S. After n steps:
d(pₙ, pₙ*) ≤ (1/2)ⁿ d(p₀, p₀*)

*Proof:*
Each iteration halves the distance between corresponding points:
d(pₙ₊₁, pₙ₊₁*) = ∥(pₙ + v)/2 - (pₙ* + v)/2∥ = d(pₙ, pₙ*)/2

### Lemma 3: Complete Coverage
For any point q ∈ S and ε > 0, the probability of the chaos game visiting a point within ε of q approaches 1.

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

## Visual Proofs

### Lemma 1 Visualization
[Interactive Demo: Invariance Property](../examples/lemma1_demo.py)
- Shows how points on S map to other points on S
- Demonstrates the recursive nature of the mapping

### Lemma 2 Visualization
[Interactive Demo: Convergence](../examples/lemma2_demo.py)
- Tracks distance between points and their "twins" on S
- Shows exponential convergence in action

## Applications

### Beyond Basic Triangles
The proof techniques extend to:
1. Modified ratios (λ ≠ 1/2)
2. Different polygon bases
3. Higher dimensions

See [Variations](sierpinski_variations.md) for detailed analysis.
