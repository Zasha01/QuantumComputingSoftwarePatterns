# QuantumComputingSoftwarePatterns
 
## Setup
In order to run the experiments the necessary python packages have to be installed. This can be done using ```pip -r install requirements.txt```. 

Additionally if the experiments are to be run on the same backend as we did in the paper one has to provide a valid IBM access for the quantum device. This is encapsulated in the file activateAcc.py. Normally this file should contain code similar to the following: 
```
from qiskit import IBMQ

def activateAcc():
    APITOKEN = 'token'
    APIURL = 'https://auth.de.quantum-computing.ibm.com/api'
    IBMQ.enable_account(APITOKEN, APIURL)
```

where token is your IBMQ token. 


## Run
The experiments are provided by the python script "voterPatternEval.py". To run new experiments call "python VoterPattern.py". The results are printed in the terminal. Several options are available in order to configure the output and the experiment setup. To view all options open the experiments.cfg file and change it according to your needs.