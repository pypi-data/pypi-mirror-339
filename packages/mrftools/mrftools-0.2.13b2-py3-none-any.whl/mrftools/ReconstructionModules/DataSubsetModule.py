from ..Types import ReconstructionModuleIOType, KspaceData, ImageData
from . import ReconstructionModule, Register
from ..Utilities import dump_tensors
import torch
import gc

@Register
class DataSubsetModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, axis=None, indices=None, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=inputType) 
        self.axis = axis
        self.indices = indices 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device

    def __dict__(self):
        """
        Convert module attributes to a dictionary.

        Returns:
            dict: Dictionary containing module attributes.
        """
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "axis": self.axis,
            "indices": self.indices
        }
        return moduleDict
    

    def GetSubset(self, initialArray, axisToSample, indicesRangeToSample):
        slices = [slice(None)] * initialArray.ndim
        slices[axisToSample] = indicesRangeToSample
        return initialArray[tuple(slices)]

    def ProcessKspaceToKspace(self, inputData):
            outputData = self.GetSubset(inputData, self.axis, self.indices)
            return KspaceData(outputData)
    def ProcessImageToImage(self, inputData):
            outputData = self.GetSubset(inputData, self.axis, self.indices)
            return ImageData(outputData)
    
    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        axis = jsonInput.get("axis")
        indices = jsonInput.get("indices")
        if axis != None and indices != None:
            return DataSubsetModule(reconstructionParameters, inputType, axis, indices)
        else:
            print("DataSubsetModule requires axis and indices")
        