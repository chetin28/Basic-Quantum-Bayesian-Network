#Q2: Bayesian networks, cetin ilhan kaya

from qiskit import QuantumCircuit, Aer, execute, QuantumRegister, ClassicalRegister, IBMQ, assemble, transpile
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as ns
from qiskit.quantum_info.operators.symplectic import Pauli
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from math import *
from IPython.display import display

q = QuantumRegister(2,"q")
c = ClassicalRegister(1,"c")
qc = QuantumCircuit(q,c)

def convert(prob): #converting probability into angle
    angle = 2*asin(sqrt(prob)) #cumulative distribution function, ignore 1/pi term for suitable angle type
    #note that at first, i though we should use probability distr. func: 1/(sqrt(prob*(1-prob)))
    #again ignoring pi, but it gave off-results, so using CDF instead
    return angle
#|1> represents students done all lab hws (@q[0])
#|1> represents students succeeded (@q[1])

#marginal probability
qc.ry(convert(0.6),q[0])
#conditional probability 1
qc.cry(convert(0.9),q[0],q[1]) #if q[0]=|1>, we apply Ry to q[1] since it depends on q[0]
#Ry rotates q[i] in such a way that 90% of the measurements gives |1> state
#conditional probability 2
qc.x(q[0]) #make condition bound to |0> that is students DONT do all lab hws
qc.cry(convert(0.3),q[0],q[1])
qc.x(q[0]) #turn it back
qc.measure(q[1],c)


job = execute(qc,Aer.get_backend("qasm_simulator"),shots=10000)
qcirc = qc.draw(output="mpl",reverse_bits=True)
display(qcirc)
qcirc.savefig("circuit.jpg")
hist = job.result().get_counts(qc)
fig1 = plot_histogram(hist)
fig1.savefig("hist.jpg")


#constructing the error
prob1 = 0.01 #low prob
prob2 = 0.1  # high prob
prob3 = 1-prob2 # since pr2+pr3=1
prob4 = 1-prob1
error1 = ns.phase_damping_error(prob1,2)
error2 = ns.pauli_error([("X",prob2),("I",prob3)])
error3 = ns.pauli_error([("Y",prob2),("I",prob3)])
defnoise = ns.NoiseModel() #defining noise
defnoise.add_all_qubit_quantum_error(error1,["X","I"])
defnoise.add_all_qubit_quantum_error(error2,[]) #leaving instructions empty means defaults: ["I","u3","cx"]
defnoise.add_all_qubit_quantum_error(error3,["Y","I"],warnings=False)


#carrying error simulation
print("simulated with following")
print(defnoise)
noisyjob = execute(qc,Aer.get_backend("qasm_simulator"),noise_model=defnoise, shots=10000)
noisyhist = noisyjob.result().get_counts()
fig2 = plot_histogram(noisyhist)
fig2.savefig("noisy_hist.jpg")

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q-education', group='mid-east-tech-un-1', project='2300343-Intro-Computational-Methods')

# i tried to use the least_busy funct. to call for least busy hardware, but get 404 client error and pc couldn't reach the ibmq-api
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# n=2
# backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n+1) and not x.configuration().simulator and x.status().operational==True))
# print("least busy hardware is", backend)
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# so instead, i ll use directly ibmq-manila with manual selection from https://quantum-computing.ibm.com/services?services=systems&systems=yours
backend = provider.get_backend("ibmq_manila")

trans = transpile(qc, backend, optimization_level=2)
job2 = backend.run(trans)
job_monitor(job2,interval=2)
results = job2.result()
final = results.get_counts()
fig3 = plot_histogram(final)
fig3.savefig("real_hist.jpg")
