from qiskit import IBMQ

def activateAcc():
    APITOKEN = 'YOUR KEY'
    APIURL = 'https://auth.de.quantum-computing.ibm.com/api'
    IBMQ.save_account('4a36ee0b4d47cc33b3dfa767373e5011da597ce184e8b3bb292aa2c18b841e1e99486aaa3a2fb410cd4dfa894bcba564db0490a612ea996f2c05ff1e69014532', overwrite=True)
    IBMQ.enable_account(APITOKEN, APIURL)