from mrftools.Types import AcquisitionType, Timepoint
from mrftools.SequenceModules import SequenceModule, AcquisitionModule, Register
import numpy as np
import torch

@Register
class TRUEFISPAcquisitionModuleQRF(AcquisitionModule):
    """
    Class representing a TRUEFISP acquisition module.

    Args:
        timepoints (np.array, optional): Array of timepoints. Defaults to [].
        units (SequenceUnits, optional): The units of the module. Defaults to None.
    """
    def __init__(self, timepoints=[], units=None):
        """
        Initialize a TRUEFISPAcquisitionModule instance.

        Args:
            timepoints (np.array, optional): Array of timepoints. Defaults to [].
            units (SequenceUnits, optional): The units of the module. Defaults to None.
        """
        AcquisitionModule.__init__(self, acquisitionType=AcquisitionType.TRUEFISP, timepoints=timepoints, units=units) 

    def __str__(self):
        """
        Generate a string representation of the module.

        Returns:
            str: The string representation of the module.
        """
        return SequenceModule.__str__(self) + " || Acquisition Type: " + self.acquisitionType.name + " || Timepoints: \n" + str(self.timepoints)
    
    def __dict__(self):
        """
        Generate a dictionary representation of the module.

        Returns:
            dict: The dictionary representation of the module.
        """
        timepointDict = [dict(zip(self.timepoints.dtype.names,x.tolist())) for x in self.timepoints]
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "timepoints": timepointDict
        }
        return moduleDict
    
    @staticmethod
    def FromJson(jsonInput):
        """
        Create an instance of TRUEFISPAcquisitionModule from JSON input.

        Args:
            jsonInput (dict): The JSON input data.

        Returns:
            TRUEFISPAcquisitionModule: An instance of TRUEFISPAcquisitionModule.
        """
        timepointsJson = jsonInput.get("timepoints")
        if(timepointsJson != None):
            timepoints = []
            for timepointJson in timepointsJson:
                timepoints.append(tuple(timepointJson.values()))
            timepoints = np.array(timepoints, dtype=Timepoint)         
            return TRUEFISPAcquisitionModuleQRF(timepoints) 
        else:
            print("TRUEFISPAcquisitionModule requires timepoints")
    
    
    def Simulate(self, dictionaryEntries, numSpins, device=None, inputMx=None, inputMy=None, inputMz=None): 
        """
        Simulate the TRUEFISP acquisition module.

        Args:
            dictionaryEntries (dict): Dictionary containing relaxation parameters.
            numSpins (int): not necessary, to be removed or can be set to one
            device (torch.device, optional): The device for simulation. Defaults to None.
            inputMx (torch.Tensor, optional): Input magnetization in x direction. Defaults to None.
            inputMy (torch.Tensor, optional): Input magnetization in y direction. Defaults to None.
            inputMz (torch.Tensor, optional): Input magnetization in z direction. Defaults to None.

        Returns:
            tuple: A tuple containing simulation time and magnetization tensors.
        """
        print("Simulating QRF TrueFisp")
        if(device==None):
            if torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")    
        T1s = torch.tensor(dictionaryEntries['T1']).to(device)
        T2s = torch.tensor(dictionaryEntries['T2']).to(device)
        dB0 = torch.tensor(dictionaryEntries['dB0']).to(device)
        B1s = torch.tensor(dictionaryEntries['B1']).to(device)
        TRs = torch.tensor(self.timepoints['TR'].copy()).to(device)
        TEs = torch.tensor(self.timepoints['TE'].copy()).to(device)
        FAs = torch.tensor(self.timepoints['FA'].copy()).to(device)
        PHs = torch.tensor(self.timepoints['PH'].copy()).to(device)

        numTimepoints = len(self.timepoints); numDictionaryEntries = len(dictionaryEntries)
        Mx0 = torch.zeros((numTimepoints, numSpins, numDictionaryEntries))
        My0 = torch.zeros((numTimepoints, numSpins, numDictionaryEntries))
        Mz0 = torch.zeros((numTimepoints, numSpins, numDictionaryEntries))
        Time = torch.zeros((numTimepoints))

        Mx = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        My = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        Mz = torch.zeros((numSpins, numDictionaryEntries)).to(device)    
        FAs = torch.deg2rad(FAs)
        PHs = torch.deg2rad(PHs)
        
        if(inputMx is not None):
            if(torch.numel(inputMx) == numSpins*numDictionaryEntries and torch.numel(inputMy) == numSpins*numDictionaryEntries and torch.numel(inputMz) == numSpins*numDictionaryEntries):
                Mx = inputMx
                My = inputMy
                Mz = inputMz
            else:
                if(torch.numel(inputMx) == 1 and torch.numel(inputMy) == 1 and torch.numel(inputMz) == 1 ):
                    Mx = torch.ones(numSpins, numDictionaryEntries) * inputMx
                    My = torch.ones(numSpins, numDictionaryEntries) * inputMy
                    Mz = torch.ones(numSpins, numDictionaryEntries) * inputMz
                else: 
                    print("Simulation Failed: Number of input magnetization states doesn't equal number of requested spins to simulate.")
                    return
        Mx = Mx.to(device);  My = My.to(device); Mz = Mz.to(device); 

        with torch.no_grad():
            accumulatedTime = 0
            for iTimepoint in range(numTimepoints):
                fa = FAs[iTimepoint] * B1s
                tr = TRs[iTimepoint]
                te = TEs[iTimepoint]
                ph = PHs[iTimepoint]
                tre = tr-te
                
                Time[iTimepoint] = accumulatedTime
                accumulatedTime = accumulatedTime + tr

                At2te = torch.exp(-1*te/T2s)
                At1te = torch.exp(-1*te/T1s)
                Bt1te = 1-At1te
                
                At2tr = torch.exp(-1*tre/T2s)
                At1tr = torch.exp(-1*tre/T1s)
                Bt1tr = 1-At1tr

                At2trFull = torch.exp(-1*tr/T2s)
                At1trFull = torch.exp(-1*tr/T1s)
                Bt1trFull = 1-At1trFull

                # M2 = Rphasep*Rflip*Rphasem*M1;       % RF effect  

                # Applying Rphasem = [cos(-iph) -sin(-iph) 0; sin(-iph) cos(-iph) 0; 0 0 1];  
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = torch.multiply(torch.cos(-ph),Mxi) - torch.multiply(torch.sin(-ph), Myi)
                My = torch.multiply(torch.sin(-ph),Mxi) + torch.multiply(torch.cos(-ph), Myi)
                Mz = Mzi

                # Applying flip angle = [1 0 0; 0 cos(randflip(ii)) -sin(randflip(ii)); 0 sin(randflip(ii)) cos(randflip(ii))];
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = Mxi
                My = torch.multiply(torch.cos(fa),Myi)-torch.multiply(torch.sin(fa),Mzi)
                Mz = torch.multiply(torch.sin(fa),Myi)+torch.multiply(torch.cos(fa),Mzi)

                # Applying Rphasep = [cos(iph) -sin(iph) 0; sin(iph) cos(iph) 0; 0 0 1];  
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = torch.multiply(torch.cos(ph),Mxi) - torch.multiply(torch.sin(ph), Myi)
                My = torch.multiply(torch.sin(ph),Mxi) + torch.multiply(torch.cos(ph), Myi)
                Mz = Mzi

                MxTR = Mx; MyTR = My; MzTR = Mz

                # Relaxation over TE
                Mx = torch.multiply(Mx, At2te)
                My = torch.multiply(My, At2te)
                Mz = torch.multiply(Mz, At1te)+Bt1te

                # dephasing over TE
                Mxi = Mx; Myi = My; Mzi = Mz
                phite = 2*np.pi*dB0*te
                Mx = torch.multiply(torch.cos(phite),Mxi) - torch.multiply(torch.sin(phite), Myi)
                My = torch.multiply(torch.sin(phite),Mxi) + torch.multiply(torch.cos(phite), Myi)
                Mz = Mzi
                
                # phite = 2*pi*df*te(ii)/1000;  % phase accumulation during TE due to off-resonance 
                # zrotdfte = [cos(phite) -sin(phite) 0; sin(phite) cos(phite) 0; 0 0 1]; % rotation around Z

                Mxyi = Mx + 1j*My
                Mxy = torch.multiply(Mxyi, torch.exp(-1j*ph))
                Mxi = torch.real(Mxy)
                Myi = torch.imag(Mxy) 
                # print("ADC phase offset.")

                # Reading value after TE and before TRE 
                Mx0[iTimepoint,:,:]=Mxi.cpu()
                My0[iTimepoint,:,:]=Myi.cpu()
                Mz0[iTimepoint,:,:]=Mz.cpu()

                # Relaxation over TRE (TR-TE) 
                Mx = MxTR*At2trFull
                My = MyTR*At2trFull
                Mz = MzTR*At1trFull+Bt1trFull

                # dephasing over TRE (TR-TE)
                Mxi = Mx; Myi = My; Mzi = Mz
                #phitr = 2*np.pi*dB0*tre
                phitr = 2*np.pi*dB0*tr
                Mx = torch.multiply(torch.cos(phitr),Mxi) - torch.multiply(torch.sin(phitr), Myi)
                My = torch.multiply(torch.sin(phitr),Mxi) + torch.multiply(torch.cos(phitr), Myi)
                Mz = Mzi

                # phitr = 2*pi*df*tr(ii)/1000;  % phase accumulation during TR due to off-resonance 
                # zrotdftr = [cos(phitr) -sin(phitr) 0; sin(phitr) cos(phitr) 0; 0 0 1]; % rotation around Z 

                del fa, tr, te, tre, At2te, At1te, Bt1te, At2tr, At1tr, Bt1tr, Mxi, Myi, Mzi
        del T1s, T2s, B1s, dB0, FAs, PHs, Mx, My, Mz
        return Time,Mx0,My0,Mz0