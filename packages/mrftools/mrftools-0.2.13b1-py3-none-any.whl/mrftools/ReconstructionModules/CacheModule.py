from ..Types import ReconstructionModuleIOType, KspaceData, ImageData, MapData
from . import ReconstructionModule, Register
from ..Utilities import dump_tensors
import torch
import gc

@Register
class CacheModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
        if inputType == ReconstructionModuleIOType.KSPACE:
            self.cache = KspaceData(torch.empty(0))
        elif inputType == ReconstructionModuleIOType.IMAGE:
            self.cache = ImageData(torch.empty(0))
        elif inputType == ReconstructionModuleIOType.MAP:
            self.cache = MapData(torch.empty(0))
        else:
            raise ValueError("Unknown input type")

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
        }
        return moduleDict

    def ProcessKspaceToKspace(self, inputData):
            self.cache = KspaceData(torch.clone(inputData));
            return KspaceData(inputData)
    def ProcessImageToImage(self, inputData):
            self.cache = ImageData(torch.clone(inputData));
            return ImageData(inputData)
    def ProcessMapToMap(self, inputData):
            self.cache = MapData(torch.clone(inputData));
            return MapData(inputData)
     
    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        return CacheModule(reconstructionParameters, inputType, outputType)
        