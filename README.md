# Basic Quantum Bayesian Network
 
Consider a problem that contains three probabilities:
Two conditional probabilities:
• The student passes the course with a good grade 90% if he/she solves all the lab homework
• The student passes the course with a good grade 30% if he/she DOES NOT solve the lab
homework
one marginal probability:
• 60% of the students solve all the lab homework
In graph representation the problem looks like this:

( Student solves all the lab homework )    --→   ( Student passes the course )

It has two nodes, and an edge that links the nodes
a) Implement a routine that encodes the probability as an angle suitable for implementing as an
input to RY gate.
b) Use the routine in a) and RY gate to implement marginal probability of solving all the lab
homework as a parameter by rotating a single qubit.
c) What gate can you use for conditional probabilities? (tip: very much related to RY). Then, what
is the minimum number of qubits required to implement this problem?
d) Implement this problem as a Quantum Circuit (i.e. implement a Quantum Bayesian Network)
Student
solves all
the lab
homework
Student
passes the
course
e) Run this circuit with at least 10000 shots, and obtain the overall (marginal) probability to pass
the course.
i. Without noise
ii. In a simulator with noise
iii. Using real qubitS
Compare the results.
(bonus: How did we represent the nodes and the vertices in the graph? Can this be generalized?) 
