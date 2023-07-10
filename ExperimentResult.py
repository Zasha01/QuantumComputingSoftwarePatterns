import json
import sys



resultsDir = "results"

class ExperimentResult:
    groundTruth = None
    transpilationResults = None
    optimizationResults = None
    backendResults = None

    def __init__(self, groundTruth) -> None:
        self.groundTruth = groundTruth

    def __init__(self, groundTruth, transpilationResults, optimizationResults, backendResults) -> None:
        self.groundTruth = groundTruth
        self.optimizationResults = optimizationResults
        self.transpilationResults = transpilationResults
        self.backendResults = backendResults

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def combine(self, other):
        if(len(self.transpilationResults) != 0 and len(self.transpilationResults)/len(self.groundTruth) != len(other.transpilationResults)/len(other.groundTruth)):
            print("Error combining results. Each result must have the same number of transpilation variants")
            sys.exit(1)
        if(len(self.optimizationResults) != 0 and len(self.optimizationResults)/len(self.groundTruth) != len(other.optimizationResults)/len(other.groundTruth)):
            print("Error combining results. Each result must have the same number of optimization variants")
            sys.exit(1)
        if(len(self.backendResults) != 0 and len(self.backendResults)/len(self.groundTruth) != len(other.backendResults)/len(other.groundTruth)):
            print("Error combining results. Each result must have the same number of backend variants")
            sys.exit(1)
        self.groundTruth.extend(other.groundTruth)
        self.transpilationResults.extend(other.transpilationResults)
        self.optimizationResults.extend(other.optimizationResults)
        self.backendResults.extend(other.backendResults)
        return self