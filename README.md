# ds-sudoku-solver-ro

Concurrent sudoku solver. Homework in Distributed Systems. Specification can be found at https://courses.cs.ut.ee/MTAT.08.009/2017_fall/uploads/Main/DS_HW2.pdf.

## -- New --
* Uses multicast to broadcast/receive connection URIs.
* Uses Pyro4 Distributed Objects to directly call methods from server instead of custom network protocol.
