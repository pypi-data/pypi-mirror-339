Performance improvements for k-point creation of matrices

The internal Cython code was restructured for much better
performance.
This yields a significant performance improvement for DFT
matrices (many couplings) but a very minor perf. hit
for small TB matrices (few couplings + few rows).
