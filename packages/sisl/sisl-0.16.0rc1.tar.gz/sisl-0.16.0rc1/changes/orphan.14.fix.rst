Fixed `orbitals=slice(x, None)` arguments

It now correctly uses `geometry.no` instead of `geometry.na`.

Likely nobody used `slice` arguments anyway.
