# Report

### Summary
Repo conatins code that implements client-server multiplication of big matrixes AxB (those size is to large to fit into RAM). Algorithm reads a one column of matrix B (that takes a lot more time compared to reading single row) and sequentally calculates dot product of it and all rows of A. Cumputation result then stored within `cols` directory, where `.dat` file's name denotes correspond AxB column.<br>

### Source code layout
`client.py` contains code of worker, performing actual calculations and file manipulation.<br>
`server.py` contains code of server, multiplexing data for workers and keep track of fulfilled computations. <br>
`settings.py` allows one to conviniently change main parameters (such as input/output files).<br>
`utils.py` contains several utility functions.<br>
`manage` is a CLI script for starting/stoping server, progress track and matrix sample generation.<br>
<br>

### Demo
[![alt](https://asciinema.org/a/169408.png)](https://asciinema.org/a/169408)
