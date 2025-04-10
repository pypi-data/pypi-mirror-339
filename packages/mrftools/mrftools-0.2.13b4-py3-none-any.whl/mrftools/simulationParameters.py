import numpy as np
import h5py
from matplotlib import pyplot as plt
import torch
from tqdm import tqdm
from . import DictionaryParameters, SequenceParameters
from importlib.metadata import version  
import json as json
from scipy.signal import convolve
import torch.nn.functional as F # TODO move up

class SimulationParameters:
    """
    A class to represent simulation parameters and methods.
    """

    def __init__(self,sequenceParameters, dictionaryParameters, name="", version="dev", numSpins=1, times=[], timeDomainResults=[], results=[], truncationMatrix=[], truncatedResults=[], singularValues=[]):
        """
        Initialize SimulationParameters.

        Args:
            sequenceParameters (SequenceParameters): The sequence parameters.
            dictionaryParameters (DictionaryParameters): The dictionary parameters.
            name (str, optional): Name of the simulation. If not provided, a default name will be generated.
            version (str, optional): Version of the simulation.
            numSpins (int, optional): Number of spins.
            times (list, optional): List of simulation times.
            timeDomainResults (list, optional): Results in the time domain.
            results (list, optional): Simulation results.
            truncationMatrix (list, optional): Truncation matrix.
            truncatedResults (list, optional): Truncated simulation results.
            singularValues (list, optional): Singular values of the simulation.
        """
        self.sequenceParameters = sequenceParameters
        self.dictionaryParameters = dictionaryParameters
        self.numSpins = numSpins
        self.times = times
        self.timeDomainResults = timeDomainResults
        self.results = results
        self.truncationMatrix = truncationMatrix
        self.truncatedResults = truncatedResults
        self.singularValues = singularValues
        if not name:
            self.name = sequenceParameters.name + "_" + dictionaryParameters.name + "_" + str(numSpins)
        else:
            self.name = name
        self.version = version
        #print("Simulation Parameter set '"+ self.name + "' initialized (Sequence: '" + self.sequenceParameters.name + "',  Dictionary: '" + self.dictionaryParameters.name + "') with " + str(self.numSpins) + " spins")
    
    def __dict__(self):
        """
        Returns a dictionary representation of the SimulationParameter object for the purposes of JSON serialization.

        Returns:
            dict: A dictionary representation of the object.
        """
        mrftools_version = version("mrftools")
        sequenceDict = self.sequenceParameters.__dict__().get("sequence")
        dictionaryDict = self.dictionaryParameters.__dict__().get("dictionary")
        truncationMatrixDict = {
            "real": self.truncationMatrix.real.tolist(), 
            "imag": self.truncationMatrix.imag.tolist()
        }
        truncatedResultsDict = {
            "real": self.truncatedResults.real.tolist(), 
            "imag": self.truncatedResults.imag.tolist()
        }
        singularValuesDict = {
            "real": self.singularValues.real.tolist(), 
            "imag": self.singularValues.imag.tolist()
        }
        simulationDict  = {
            "name": self.name,
            "version": self.version,
            "sequence": sequenceDict,
            "dictionary": dictionaryDict,
            "numSpins": self.numSpins, 
            "truncationMatrix": truncationMatrixDict, 
            "truncatedResults": truncatedResultsDict, 
            "singularValues": singularValuesDict
        }
        simulationParametersDict = {
            "mrftools_version": mrftools_version,
            "simulation": simulationDict
        }
        return simulationParametersDict

    def ExportToJson(self, baseFilepath=""):
        """
        Export simulation parameters to a JSON file.

        Args:
            baseFilepath (str, optional): Base filepath for the JSON file.

        Returns:
            None
        """
        simulationFilename = baseFilepath+self.name+"_"+self.version+".simulation"
        with open(simulationFilename, 'w') as outfile:
            json.dump(self.__dict__(), outfile, indent=2)

    @staticmethod
    def FromJson(inputJson):
        """
        Create a SimulationParameters instance from a JSON string input.

        Args:
            inputJson (dict): JSON data containing simulation parameters.

        Returns:
            SimulationParameters: The created SimulationParameters instance.
        """
        mrftoolsVersion = inputJson.get("mrftools_version")
        if(mrftoolsVersion != None):
            #print("Input file mrttools Version:", mrftoolsVersion)
            simulationJson = inputJson.get("simulation")
        else:
            simulationJson = inputJson
        name = simulationJson.get("name")
        version = simulationJson.get("version")
        sequenceJson = simulationJson.get("sequence")
        sequenceParameters = SequenceParameters.FromJson(sequenceJson)
        dictionaryJson = simulationJson.get("dictionary")
        dictionaryParameters = DictionaryParameters.FromJson(dictionaryJson)
        numSpins = simulationJson.get("numSpins")
        truncationMatrixJson = simulationJson.get("truncationMatrix")
        truncationMatrix = np.array(truncationMatrixJson.get("real")) + 1j * np.array(truncationMatrixJson.get("imag"))
        truncatedResultsJson = simulationJson.get("truncatedResults")
        truncatedResults = np.array(truncatedResultsJson.get("real")) + 1j * np.array(truncatedResultsJson.get("imag"))
        singularValuesJson = simulationJson.get("singularValues")
        singularValues = np.array(singularValuesJson.get("real")) + 1j * np.array(singularValuesJson.get("imag"))
        if(name != None and sequenceJson != None and dictionaryJson != None):
            return SimulationParameters(sequenceParameters, dictionaryParameters, name, version, numSpins, None, None, None, truncationMatrix, truncatedResults, singularValues)
        else:
            print("SimulationParameters requires name, sequence, and dictionary")

    @staticmethod
    def FromFile(path):
        """
        Create a SimulationParameters instance from a JSON file.

        Args:
            path (str): Path to the JSON file.

        Returns:
            SimulationParameters: The created SimulationParameters instance.
        """
        with open(path) as inputFile:
            inputJson = json.load(inputFile)
            return SimulationParameters.FromJson(inputJson)
        
    def Execute(self, numBatches=1, device=None):
        """
        Execute the simulation.

        Args:
            numBatches (int, optional): Number of batches.
            device: (str, optional): Device for execution.

        Returns:
            numpy.ndarray: Simulation results.
        """
        if(device==None):
            if torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")
        dictEntriesPerBatch = int(len(self.dictionaryParameters.entries)/numBatches)
        print("Simulating " + str(numBatches) + " batch(s) of ~" + str(dictEntriesPerBatch) + " dictionary entries")
        singleResult = self.sequenceParameters.Simulate(self.dictionaryParameters.entries[0], 1)
        self.numTimepoints = np.shape(singleResult[1][0])[0]
        self.numReadoutPoints = np.shape(singleResult[2][0])[0]
        Mxy = np.zeros((self.numTimepoints, len(self.dictionaryParameters.entries)), np.complex128)
        ReadoutMxy = np.zeros((self.numReadoutPoints, len(self.dictionaryParameters.entries)), np.complex128)
        with tqdm(total=numBatches) as pbar:
            for i in range(numBatches):
                firstDictEntry = i*dictEntriesPerBatch
                if i == (numBatches-1):
                    lastDictEntry = len(self.dictionaryParameters.entries)
                else:
                    lastDictEntry = firstDictEntry+dictEntriesPerBatch
                batchDictionaryEntries = self.dictionaryParameters.entries[firstDictEntry:lastDictEntry]
                allResults = self.sequenceParameters.Simulate(batchDictionaryEntries, self.numSpins, device=device)
                Mx = torch.mean(allResults[1][0], axis=1)
                My = torch.mean(allResults[1][1], axis=1)
                Mxy[:,firstDictEntry:lastDictEntry] = Mx+(My*1j) 
                ReadoutMx = torch.mean(allResults[2][0], axis=1)
                ReadoutMy = torch.mean(allResults[2][1], axis=1)
                ReadoutMxy[:,firstDictEntry:lastDictEntry] = ReadoutMx+(ReadoutMy*1j)
                pbar.update(1)
        self.times = allResults[0]
        self.timeDomainResults = Mxy
        self.results = np.delete(ReadoutMxy,0,axis=0)
        return self.results
    
    def ExecuteWrSVD(self, numBatches=1, dictPercent4rSVD=100, partialdB0StepSize=4, dB0StepSize=1, truncationNumber=20, numPowerIterations=0, device=None):
        """
        Execute the partial simulation. Calculate randomized SVD (rSVD). Execute the full simulation and compress. 

        Args:
            numBatches (int, optional): Number of batches.
            dictUndersampling (int, optional): Undersampling factor for T1/T2/T2*/dB0 dimension for the partial simulation.
            device: (str, optional): Device for execution.

        Returns:
            numpy.ndarray: Simulation results.
        """
        if(device==None):
            if torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")

        #### partial dictionary simulation ###

        # Create dictionary ranges from the self
        t1Range = [np.min(self.dictionaryParameters.entries['T1']),np.max(self.dictionaryParameters.entries['T1'])]
        t2Range = [np.min(self.dictionaryParameters.entries['T2']),np.max(self.dictionaryParameters.entries['T2'])]
        t2StarRange = [np.min(self.dictionaryParameters.entries['T2star']),np.max(self.dictionaryParameters.entries['T2star'])]
        #dB0Range = [np.min(self.dictionaryParameters.entries['dB0']),partialdB0StepSize,np.max(self.dictionaryParameters.entries['dB0'])]
        uniquedB0s = np.unique(self.dictionaryParameters.entries['dB0'])
        dB0step = uniquedB0s[1] - uniquedB0s[0] 
        dB0Range = [np.min(self.dictionaryParameters.entries['dB0']),partialdB0StepSize*dB0step,np.max(self.dictionaryParameters.entries['dB0'])]

        # Lorentzian window parameters
        winSpanHz = 20
        win = int(winSpanHz/dB0step)
        points = torch.arange(-win,win,1)
        points = torch.cat((points,torch.Tensor([win]))).to(device)
        points_ones = torch.ones(points.shape).to(device)

        T1s = []
        T2s = []
        T2stars = []
        t1 = t1Range[0]
        t2 = t2Range[0]
        t2Star = t2StarRange[0]
        while t1 <= t1Range[1]:
            T1s.append(t1)
            t1 = t1*(1+(dictPercent4rSVD/100))
        while t2 <= t2Range[1]:
            T2s.append(t2)
            t2 = t2*(1+(dictPercent4rSVD/100))
        while t2Star <= t2StarRange[1]:
            T2stars.append(t2Star)
            t2Star = t2Star*(1+(dictPercent4rSVD/100))
        pairs = []
        for t1Val in T1s:
            for t2Val in T2s:
                if(t1Val>t2Val): # Don't include pairs with T2 longer than T1
                    for t2StarVal in T2stars:
                        if (t2Val>t2StarVal):
                            pairs.append((t1Val,t2Val,t2StarVal))

        dB0s = np.arange(dB0Range[0], dB0Range[2]+1e-5, dB0Range[1])
        B1s = [1]

        T2starsTemp = []
        T2starsTemp.append(0.0015)

        dictionaryRSVD = DictionaryParameters("rSVD")
        dictionaryRSVD.InitializeFromUnique(T1s, T2s, T2starsTemp, dB0s)

        simulationRSVD = SimulationParameters(self.sequenceParameters, dictionaryRSVD, "Example", numSpins=1)
        simulationRSVD.Execute(device=device,numBatches=2)

        # rSVD parameters
        dictionaryShapeRSVD = np.shape(simulationRSVD.results)
        full_matrices = False
        seed=2147483647
        Y = torch.zeros(dictionaryShapeRSVD[0],truncationNumber)
        Z = torch.zeros(dictionaryShapeRSVD[0],dictionaryShapeRSVD[0])

        partialDict = []
        partialDictT2star = []

        # Get RSVD results into a tensor
        rsvdResults = torch.tensor(simulationRSVD.results)
        for t1Val in T1s:
            for t2Val in T2s:
                if(t1Val>t2Val): # Don't include pairs with T2 longer than T1
                    dictMask = ((simulationRSVD.dictionaryParameters.entries['T1'] == t1Val) & (simulationRSVD.dictionaryParameters.entries['T2'] == t2Val)) # get the T1/T2 matching dict
                    dictTmp = rsvdResults[:,dictMask].to(device)
                    for t2StarVal in T2stars:
                        if (t2Val>t2StarVal):
                            FWHM = (1/t2StarVal-1/t2Val)/torch.pi # make the Lorentzian window
                            alpha = winSpanHz*2*0.5*2.35482004503/FWHM
                            FWHM0 = 2*win*torch.sqrt(-2*torch.log(torch.tensor(0.5)))/alpha
                            lorentzWindowTmp = torch.square((0.5*FWHM0*points_ones)) / (torch.square(points) + torch.square((0.5*FWHM0*points_ones)))
                            lorentzWindowTmp = lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0Range[1])].to(torch.complex128)
                            #lorentzWindowTmp = (lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0Range[1])]/torch.norm(lorentzWindowTmp)).to(torch.complex128) # also normalize the lorentizan window
                            convDict = F.conv1d(dictTmp.unsqueeze(1), lorentzWindowTmp.view(1, 1, -1)).squeeze(1)
                            convDictNorm = torch.sqrt(torch.sum(torch.pow(torch.abs(convDict[:,:]),2),0))
                            normalizedDictionary = convDict / convDictNorm
                            partialDictT2star.append(normalizedDictionary.cpu().numpy())
                            partialDict.append(normalizedDictionary.cpu().numpy())
                            del lorentzWindowTmp, normalizedDictionary, convDict, convDictNorm
                    del dictTmp
            partialDictT2star = np.reshape(np.swapaxes(partialDictT2star,0,1),[np.shape(partialDictT2star)[1],np.shape(partialDictT2star)[0]*np.shape(partialDictT2star)[2]])
            randGen = torch.Generator(); randGen.manual_seed(seed) # update Y
            # Omega = torch.randn(np.shape(partialDictT2star)[1], truncationNumber, generator=randGen, dtype=torch.complex64)
            Omega = torch.complex(torch.randn(np.shape(partialDictT2star)[1], truncationNumber, dtype=torch.float32),torch.randn(np.shape(partialDictT2star)[1], truncationNumber, dtype=torch.float32)*0)
            A = torch.complex(torch.Tensor(np.real(partialDictT2star)),torch.Tensor(np.imag(partialDictT2star))) 
            Ytmp = torch.matmul(A,Omega)
            Ztmp = torch.matmul(A ,A.H)
            #for q in range(numPowerIterations):
            #    Ytmp = torch.matmul(torch.matmul(A ,A.H), Ytmp)
            Y = Y + Ytmp
            Z = Z + Ztmp
            partialDictT2star = []
        #OmegaAll = torch.complex(torch.randn(np.shape(partialDict)[1], truncationNumber, dtype=torch.float32),torch.randn(np.shape(partialDict)[1], truncationNumber, dtype=torch.float32)*0)
        #Aall = torch.complex(torch.Tensor(np.real(partialDict)),torch.Tensor(np.imag(partialDict))) 
        #Yall = torch.matmul(A,Omega)
        #Q, _ = torch.linalg.qr(Yall) # calculate rSVD
        #Q, _ = torch.linalg.qr(Y) # calculate rSVD
        Q, _ = torch.linalg.qr(torch.matmul(torch.linalg.matrix_power(Z,numPowerIterations),Y)) # calculate rSVD
        A = np.reshape(np.swapaxes(partialDict,0,1),[np.shape(partialDict)[1],np.shape(partialDict)[0]*np.shape(partialDict)[2]])
        A = torch.complex(torch.Tensor(np.real(A)),torch.Tensor(np.imag(A))) 
        B = torch.matmul(Q.H, A)
        #v, s, u_tilde = torch.linalg.svd(B.H, full_matrices=full_matrices)
        u_tilde, s, v = torch.linalg.svd(B, full_matrices=full_matrices)
        u = torch.matmul(Q, u_tilde)
        self.u = u
        #uT = torch.transpose(u,0,1)
        uT = u.H
        self.uT = uT
        print('randomized SVD calculated')

        ### make the full and compressed dictionary
        dictionaryB0 = DictionaryParameters("B0")
        dictionaryT2star = DictionaryParameters("T2star")

        T1s = np.unique(self.dictionaryParameters.entries['T1']) # get from the initialized dict
        T2s = np.unique(self.dictionaryParameters.entries['T2'])
        T2stars = np.unique(self.dictionaryParameters.entries['T2star'])

        pairs = []
        for t1Val in T1s:
            for t2Val in T2s:
                if(t1Val>t2Val): # Don't include pairs with T2 longer than T1
                    for t2StarVal in T2stars:
                        if (t2Val>t2StarVal):
                            pairs.append((t1Val,t2Val,t2StarVal))

        T1sFromPairs = []
        T2sFromPairs = []
        T2starsFromPairs = []
        for pair in pairs:
            T1sFromPairs.append(pair[0])
            T2sFromPairs.append(pair[1])
            T2starsFromPairs.append(pair[2])
        dB0Range = [np.min(self.dictionaryParameters.entries['dB0']),dB0step*dB0StepSize,np.max(self.dictionaryParameters.entries['dB0'])]
        dB0sWoT2star = np.arange(dB0Range[0], dB0Range[2]+1e-5, dB0step)
        dB0sWT2star = np.arange(dB0Range[0], dB0Range[2]+1e-5, dB0Range[1])

        dictionaryB0.InitializeFromUnique(T1s, T2s, T2starsTemp, dB0sWoT2star)
        dictionaryT2star.InitializeFromUnique(T1s, T2s, T2stars, dB0sWT2star[int(winSpanHz/(dB0StepSize*dB0step)):-int(winSpanHz/(dB0StepSize*dB0step))])
        simulationB0 = SimulationParameters(self.sequenceParameters, dictionaryB0, "Example", numSpins=1)
        simulationT2star = SimulationParameters(self.sequenceParameters, dictionaryT2star, "Example", numSpins=1)
        results_temp = torch.zeros((truncationNumber, len(simulationT2star.dictionaryParameters.entries)), dtype=torch.complex128).to(device)
        simulationB0.Execute(device=device,numBatches=4)
        print('full T1/T2/dB0 dictionary calculated')

        simulationB0Results = torch.tensor(simulationB0.results).to(device)
        uTDev = uT.to(torch.complex128).to(device)

        for t1Val in T1s:
            print("Processing T2* dimension for T1:", t1Val)
            for t2Val in T2s:
                if(t1Val>t2Val): # Don't include pairs with T2 longer than T1
                    dictMask = ((simulationB0.dictionaryParameters.entries['T1'] == t1Val) & (simulationB0.dictionaryParameters.entries['T2'] == t2Val)) # get the T1/T2 matching dict
                    dictTmp = simulationB0Results[:,dictMask]#.to(device)
                    for t2StarVal in T2stars:
                        if (t2Val>t2StarVal):
                            FWHM = (1/t2StarVal-1/t2Val)/torch.pi # make the Lorentzian window
                            alpha = winSpanHz*2*0.5*2.35482004503/FWHM
                            FWHM0 = 2*win*torch.sqrt(-2*torch.log(torch.tensor(0.5)))/alpha
                            lorentzWindowTmp = torch.square((0.5*FWHM0*points_ones)) / (torch.square(points) + torch.square((0.5*FWHM0*points_ones)))
                            #lorentzWindowTmp = lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0step)].to(torch.complex128)
                            lorentzWindowTmp = lorentzWindowTmp.to(torch.complex128)
                            #lorentzWindowTmp = (lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0Range[1])]/torch.norm(lorentzWindowTmp)).to(torch.complex128) # also normalize the lorentizan window
                            convDict = F.conv1d(dictTmp.unsqueeze(1), lorentzWindowTmp.view(1, 1, -1)).squeeze(1)
                            convDictNorm = torch.sqrt(torch.sum(torch.pow(torch.abs(convDict[:,:]),2),0))
                            normalizedDictionary = convDict / convDictNorm
                            dictMaskB0 = ((simulationT2star.dictionaryParameters.entries['T1'] == t1Val) & (simulationT2star.dictionaryParameters.entries['T2'] == t2Val) & (simulationT2star.dictionaryParameters.entries['T2star'] == t2StarVal)) # get the T1/T2/T2* matching dict indices
                            #normalizedDictionary = torch.complex(torch.Tensor(np.real(normalizedDictionary)),torch.Tensor(np.imag(normalizedDictionary))) 
                            # simulationT2star.results[:,dictMaskB0] = torch.matmul(uTDev, normalizedDictionary).cpu().numpy()
                            results_temp[:,dictMaskB0] = torch.matmul(uTDev, normalizedDictionary[:,0::int(win/winSpanHz*dB0step*dB0StepSize)])
                            del lorentzWindowTmp, normalizedDictionary, convDict, convDictNorm
                    del dictTmp
        self.results = results_temp.cpu().numpy()
        del uTDev, simulationB0Results, results_temp
        # del uTDev
        # self.results = simulationT2star.results
        self.dictionaryParameters = simulationT2star.dictionaryParameters
        return (self.results, self.dictionaryParameters, self.u, self.uT)
    
        """ for t2Val in T2s:
            print("Processing T2* dimension for T2:", t2Val)
            for t2StarVal in T2stars:
                if (t2Val>t2StarVal):
                    dictMask = ((simulationB0.dictionaryParameters.entries['T2'] == t2Val)) # get the T2/T2* matching dict
                    T1sTmp = T1s[T1s>t2Val]
                    dictTmp = torch.reshape(simulationB0Results[:,dictMask],(dictionaryShapeRSVD[0],len(T1sTmp),len(dB0s)))#.to(device)
                    FWHM = (1/t2StarVal-1/t2Val)/torch.pi # make the Lorentzian window
                    alpha = winSpanHz*2*0.5*2.35482004503/FWHM
                    FWHM0 = 2*win*torch.sqrt(-2*torch.log(torch.tensor(0.5)))/alpha
                    lorentzWindowTmp = torch.square((0.5*FWHM0*points_ones)) / (torch.square(points) + torch.square((0.5*FWHM0*points_ones)))
                    lorentzWindowTmp = lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0Range[1])].to(torch.complex128)
                    convDict = F.conv1d(dictTmp, lorentzWindowTmp.view(1, 1, -1).expand(len(T1sTmp), -1, -1), groups=dictTmp.shape[1])
                    convDict = torch.reshape(convDict,(dictionaryShapeRSVD[0],len(T1sTmp)*len(dB0s[int(winSpanHz/dB0StepSize):-int(winSpanHz/dB0StepSize)+1]))) # back to 2D
                    convDictNorm = torch.sqrt(torch.sum(torch.pow(torch.abs(convDict[:,:]),2),0))
                    normalizedDictionary = convDict / convDictNorm
                    dictMaskB0 = ((simulationT2star.dictionaryParameters.entries['T2'] == t2Val) & (simulationT2star.dictionaryParameters.entries['T2star'] == t2StarVal)) # get the T1/T2/T2* matching dict indices
                    #normalizedDictionary = torch.complex(torch.Tensor(np.real(normalizedDictionary)),torch.Tensor(np.imag(normalizedDictionary))) 
                    results_temp[:,dictMaskB0] = torch.matmul(uTDev, normalizedDictionary)
                    del lorentzWindowTmp, normalizedDictionary, convDict, convDictNorm, dictTmp
        self.results = results_temp.cpu().numpy()
        del uTDev, simulationB0Results, results_temp
        self.dictionaryParameters = simulationT2star.dictionaryParameters
        return (self.results, self.dictionaryParameters, self.u, self.uT)

        for t1Val in T1s:
            print("Processing T2* dimension for T1:", t1Val)
            for t2Val in T2s:
                if(t1Val>t2Val): # Don't include pairs with T2 longer than T1
                    dictMask = ((simulationB0.dictionaryParameters.entries['T1'] == t1Val) & (simulationB0.dictionaryParameters.entries['T2'] == t2Val)) # get the T1/T2 matching dict
                    dictTmp = simulationB0Results[:,dictMask].to(device)
                    for t2StarVal in T2stars:
                        if (t2Val>t2StarVal):
                            FWHM = (1/t2StarVal-1/t2Val)/torch.pi # make the Lorentzian window
                            alpha = winSpanHz*2*0.5*2.35482004503/FWHM
                            FWHM0 = 2*win*torch.sqrt(-2*torch.log(torch.tensor(0.5)))/alpha
                            lorentzWindowTmp = torch.square((0.5*FWHM0*points_ones)) / (torch.square(points) + torch.square((0.5*FWHM0*points_ones)))
                            lorentzWindowTmp = lorentzWindowTmp[1:len(lorentzWindowTmp):int(win/winSpanHz*dB0Range[1])].to(torch.complex128)
                            convDict = F.conv1d(dictTmp.unsqueeze(1), lorentzWindowTmp.view(1, 1, -1)).squeeze(1)
                            convDictNorm = torch.sqrt(torch.sum(torch.pow(torch.abs(convDict[:,:]),2),0))
                            normalizedDictionary = convDict / convDictNorm
                            dictMaskB0 = ((simulationT2star.dictionaryParameters.entries['T1'] == t1Val) & (simulationT2star.dictionaryParameters.entries['T2'] == t2Val) & (simulationT2star.dictionaryParameters.entries['T2star'] == t2StarVal)) # get the T1/T2/T2* matching dict indices
                            #normalizedDictionary = torch.complex(torch.Tensor(np.real(normalizedDictionary)),torch.Tensor(np.imag(normalizedDictionary))) 
                            simulationT2star.results[:,dictMaskB0] = torch.matmul(uTDev, normalizedDictionary).cpu().numpy()
                            del lorentzWindowTmp, normalizedDictionary, convDict, convDictNorm
                    del dictTmp
        del uTDev
        self.results = simulationT2star.results
        self.dictionaryParameters = simulationT2star.dictionaryParameters
        return (self.results, self.dictionaryParameters, self.u, self.uT) """
    
    @staticmethod
    def GetInnerProducts(querySignals, dictionarySignals):  
        """
        Calculate inner products between query and dictionary signals.

        Args:
            querySignals (numpy.ndarray): Query signals.
            dictionarySignals (numpy.ndarray): Dictionary signals.

        Returns:
            numpy.ndarray: Inner products between signals.
        """
        querySignalsTransposed = querySignals.transpose()
        normalizedQuerySignals = querySignalsTransposed / np.linalg.norm(querySignalsTransposed, axis=1)[:,None]
        simulationResultsTransposed = dictionarySignals.transpose()
        normalizedSimulationResultsTransposed = simulationResultsTransposed / np.linalg.norm(simulationResultsTransposed, axis=1)[:,None]
        innerProducts = np.inner(normalizedQuerySignals, normalizedSimulationResultsTransposed)
        return innerProducts

    def CalculateSVD(self, desiredSVDPower=0.99, truncationNumberOverride=None, clearUncompressedResults=False):
        """
        Perform Singular Value Decomposition (SVD) on simulation results.

        Args:
            desiredSVDPower (float, optional): Desired SVD power.
            truncationNumberOverride (int, optional): Override for truncation number.
            clearUncompressedResults (bool, optional): Clear uncompressed results.

        Returns:
            tuple: Truncation number and total SVD power.
        """
        dictionary = self.results.transpose()
        dictionaryNorm = np.sqrt(np.sum(np.power(np.abs(dictionary[:,:]),2),1))
        dictionaryShape = np.shape(dictionary)
        normalizedDictionary = np.zeros_like(dictionary)
        for i in range(dictionaryShape[0]):
            normalizedDictionary[i,:] = dictionary[i,:]/dictionaryNorm[i]
        (u,s,v) = np.linalg.svd(normalizedDictionary, full_matrices=False)
        self.singularValues = s
        if truncationNumberOverride == None:
            (truncationNumber, totalSVDPower) = self.GetTruncationNumberFromDesiredPower(desiredSVDPower)
        else:
            truncationNumber = truncationNumberOverride
            totalSVDPower = self.GetPowerFromDesiredTruncationNumber(truncationNumber)
        vt = np.transpose(v)
        self.truncationMatrix = vt[:,0:truncationNumber]
        self.truncatedResults = np.matmul(normalizedDictionary,self.truncationMatrix).transpose()
        if clearUncompressedResults:
            del self.results, self.times, self.timeDomainResults
        return (truncationNumber, totalSVDPower)

    def GetTruncationNumberFromDesiredPower(self, desiredSVDPower):
        """
        Get truncation number based on desired SVD power.

        Args:
            desiredSVDPower (float): Desired SVD power.

        Returns:
            tuple: Truncation number and total SVD power.
        """
        singularVectorPowers = self.singularValues/np.sum(self.singularValues)
        totalSVDPower=0; numSVDComponents=0
        for singularVectorPower in singularVectorPowers:
            totalSVDPower += singularVectorPower
            numSVDComponents += 1
            if totalSVDPower > desiredSVDPower:
                break
        return numSVDComponents, totalSVDPower

    def GetPowerFromDesiredTruncationNumber(self, desiredTruncationNumber):
        """
        Get total SVD power from desired truncation number.

        Args:
            desiredTruncationNumber (int): Desired truncation number.

        Returns:
            float: Total power.
        """
        singularVectorPowers = self.singularValues/np.sum(self.singularValues)
        totalSVDPower=np.sum(singularVectorPowers[0:desiredTruncationNumber])
        return totalSVDPower

    def Plot(self, dictionaryEntryNumbers=[], plotTruncated=False, plotTimeDomain=False):
        """
        Plot simulation results.

        Args:
            dictionaryEntryNumbers (list, optional): List of dictionary entry numbers.
            plotTruncated (bool, optional): Plot truncated results.
            plotTimeDomain (bool, optional): Plot in the time domain.

        Returns:
            None
        """
        if dictionaryEntryNumbers == []:
            dictionaryEntryNumbers = [int(len(self.dictionaryParameters.entries)/2)]
        ax = plt.subplot(1,1,1)
        if not plotTimeDomain:
            if not plotTruncated:
                for entry in dictionaryEntryNumbers:
                    plt.plot(abs(self.results[:,entry]), label=str(self.dictionaryParameters.entries[entry]))
            else:
                for entry in dictionaryEntryNumbers:
                    plt.plot(abs(self.truncatedResults[:,entry]), label=str(self.dictionaryParameters.entries[entry]))
        else:
            for entry in dictionaryEntryNumbers:
                plt.plot(self.times, abs(self.timeDomainResults[:,entry]), label=str(self.dictionaryParameters.entries[entry]))
        ax.legend()

    def GetAverageResult(self, indices):
        """
        Get the average result over specified indices.

        Args:
            indices (list): List of indices.

        Returns:
            numpy.ndarray: Average result.
        """
        return np.average(self.results[:,indices], 1)

    def FindPatternMatches(self, querySignals, useSVD=False, truncationNumber=25):
        """
        Find pattern matches in the simulation.

        Args:
            querySignals (numpy.ndarray): Query signals.
            useSVD (bool, optional): Use SVD for matching.
            truncationNumber (int, optional): Truncation number.

        Returns:
            numpy.ndarray: Indices of matched patterns.
        """
        if querySignals.ndim == 1:
            querySignals = querySignals[:,None]
        if not useSVD:
            querySignalsTransposed = querySignals.transpose()
            normalizedQuerySignal = querySignalsTransposed / np.linalg.norm(querySignalsTransposed, axis=1)[:,None]
            simulationResultsTransposed = self.results.transpose()
            normalizedSimulationResultsTransposed = simulationResultsTransposed / np.linalg.norm(simulationResultsTransposed, axis=1)[:,None]
            innerProducts = np.inner(normalizedQuerySignal, normalizedSimulationResultsTransposed)
            return np.argmax(abs(innerProducts), axis=1)
        else:
            if self.truncatedResults[:] == []:
                self.CalculateSVD(truncationNumber)
            signalsTransposed = querySignals.transpose()
            signalSVDs = np.matmul(signalsTransposed, self.truncationMatrix)
            normalizedQuerySignalSVDs = signalSVDs / np.linalg.norm(signalSVDs, axis=1)[:,None]
            simulationResultsTransposed = self.truncatedResults.transpose()
            normalizedSimulationResultsTransposed = simulationResultsTransposed / np.linalg.norm(simulationResultsTransposed, axis=1)[:,None]
            innerProducts = np.inner(normalizedQuerySignalSVDs, normalizedSimulationResultsTransposed)
            return np.argmax(abs(innerProducts), axis=1)