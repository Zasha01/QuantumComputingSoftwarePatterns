import sys
from tokenize import String
from tabulate import tabulate
from qiskit.circuit.random import random_circuit
import warnings
warnings.filterwarnings('ignore')
from qiskit.test.mock import FakeProvider
import pandas as pd
import random
from expsuite import PyExperimentSuite
from ExperimentResult import ExperimentResult
from DataPreparation import processResults, loadResult, saveResult, processResultAdapter
from VoterPatternVariants import runOnSimulator, tryBackends, tryOptimizations, tryTranspilations
from PlotResults import plotCircuitDistribution

class VoterPatternEval(PyExperimentSuite):
    def reset(self, params, rep):
        self.N = params["amount"]
        if(self.N % 25 == 1):
            print("Due to technical details runs with circuits % 25 == 1 are not allowed")
            sys.exit(1)
        #runExperiment
        self.resultsDir = params["outputdir"]
        #activate your IBMQ account here. You need that to run circuits on real backends
        #if you want to run on a simulator provide this here
        #activateAcc()
    
        provider = FakeProvider()
        if params["backend"] != "ibmq_ehningen":
            self.backend = provider.get_backend(params["backend"])
        else:
            self.backend = provider.get_backend("fake_boeblingen")
        self.res = []
        self.results = []
        self.allCircuits = []
        self.numBatches = 0
        self.transJobs = []
        self.optJobs = []
        self.filter = params["filter"]
        if (self.filter == "None"):
            self.filter = None

    def iterate(self, params, rep, n):
        
        
        self.createCircuits()
      
        
        for i in range(self.numBatches):
            # get ground truth
            groundTruth = runOnSimulator(self.allCircuits[i])
            self.results.append(ExperimentResult(groundTruth, None, None, None))

            #get results
            self.results[i].backendResults = tryBackends(self.allCircuits[i])
            self.transJobs.append(tryTranspilations(self.backend, self.allCircuits[i]))
            self.optJobs.append(tryOptimizations(self.backend, self.allCircuits[i]))

            

        for i in range(self.numBatches):
            print("Trying to retrieve results from backend.")
            try:
                self.results[i].transpilationResults = self.transJobs[i].result().get_counts()
                self.results[i].optimizationResults = self.optJobs[i].result().get_counts()
                self.res.append(saveResult(self.results[i], self.resultsDir))
            except Exception as e:
                print("retrieving one experiment result was unsuccessful. Trying next.")
                print("Exception: ", e)
                continue
        fileNames = self.res

        res = ExperimentResult([], [], [], [])
        for fileName in fileNames:
            res = res.combine(loadResult(fileName))

        transpilationResults = processResults(res.transpilationResults, res.groundTruth, self.filter, "seed")
        optimizationResults = processResults(res.optimizationResults, res.groundTruth, self.filter, "opt")
        backendResults = processResults(res.backendResults, res.groundTruth, self.filter, "back")

        df = []
        df.extend(processResults(transpilationResults))
        df.extend(processResults(optimizationResults))
        df.extend(processResults(backendResults))

        df = pd.DataFrame(df, columns=["Appr.", "View", "numT1", "numT10%", "comparison"])
        df = df.round(decimals=1)
        table = tabulate(df, headers='keys', tablefmt='pretty', showindex=False)
        print(table)
        latex = df.to_latex(index=False)
        if(params["printlatex"]):
            print(latex)
        if(params["showplot"]):
            plotCircuitDistribution(
                processResultAdapter(transpilationResults, self.N), 
                processResultAdapter(optimizationResults, self.N), 
                processResultAdapter(backendResults, self.N),

                )
        



        # return current repetition and iteration number and the 2 parameters
        ret = {"rep": rep, "iter": n, "table": table}
        return ret
    
    def createCircuits(self):
        while self.N > 0:
            #number of randomized circuits to consider
            numCircuits = 25 if self.N >= 25 else self.N 
            self.N -= numCircuits
            self.numBatches += 1
            maxNumQubits = 10 
            maxDepth = 40

            circuits = []
            for i in range(numCircuits):
                circuit = random_circuit(random.randint(2, maxNumQubits), random.randint(5, maxDepth), measure=True)
                circuits.append(circuit)
    
            self.allCircuits.append(circuits)

if __name__ == "__main__":

    # run experiment
    suite = VoterPatternEval()
    suite.start()
    

