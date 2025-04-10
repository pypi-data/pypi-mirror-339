from ..Types import ReconstructionModuleIOType, KspaceData, ImageData, MapData
from . import ReconstructionModule, Register
from ..Utilities import dump_tensors
import torch
import gc
import numpy as np

@Register
class RecallModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, saveIncomingToOutputs=True, sourceModuleIndex=None, device=None):
        self.sourceModuleIndex = sourceModuleIndex
        self.saveIncomingToOutputs = saveIncomingToOutputs
        if self.sourceModuleIndex is not None:
            cached_module = reconstructionParameters.modules[self.sourceModuleIndex]
            output_cache = cached_module.cache
            if isinstance(output_cache, KspaceData):
                outputType = ReconstructionModuleIOType.KSPACE
            elif isinstance(output_cache, ImageData):
                outputType = ReconstructionModuleIOType.IMAGE
            elif isinstance(output_cache, MapData):
                outputType = ReconstructionModuleIOType.MAP
            else:
                raise ValueError("Unknown cached data type")
        else:
            outputType = ReconstructionModuleIOType.IMAGE  # Default output type if no sourceModuleIndex is provided
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType)
        
        if device is None:
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device

    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "saveIncomingToOutputs": self.saveIncomingToOutputs,
            "sourceModuleIndex": self.sourceModuleIndex,
        }
        return moduleDict

    def ProcessKspaceToKspace(self, inputData):
        if self.saveIncomingToOutputs:
            self.reconstructionParameters.outputs.append(KspaceData(torch.clone(torch.tensor(inputData))))
        output = self.reconstructionParameters.modules[self.sourceModuleIndex].cache
        print("Kspace", output.data.shape)
        return KspaceData(output.data)

    def ProcessImageToImage(self, inputData):
        if self.saveIncomingToOutputs:
            self.reconstructionParameters.outputs.append(ImageData(torch.clone(torch.tensor(inputData))))
        output = self.reconstructionParameters.modules[self.sourceModuleIndex].cache
        print("Image", output.data.shape)
        return ImageData(output.data)

    def ProcessMapToMap(self, inputData):
        if self.saveIncomingToOutputs:
            self.reconstructionParameters.outputs.append(MapData(np.array(inputData)))
        output = self.reconstructionParameters.modules[self.sourceModuleIndex].cache
        print("Map", output.data.shape)
        return MapData(output.data)

    def ProcessMapToImage(self, inputData):
        if self.saveIncomingToOutputs:
            self.reconstructionParameters.outputs.append(MapData(np.array(inputData)))
        output = self.reconstructionParameters.modules[self.sourceModuleIndex].cache
        print("MaptoImage", output.data.shape)
        return ImageData(output.data)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType): 
        saveIncomingToOutputs = jsonInput.get("saveIncomingToOutputs")
        sourceModuleIndex = jsonInput.get("sourceModuleIndex")
        if saveIncomingToOutputs is not None and sourceModuleIndex is not None:
            return RecallModule(reconstructionParameters, inputType, saveIncomingToOutputs, sourceModuleIndex)
        else:
            print("RecallModule requires saveIncomingToOutputs and sourceModuleIndex")
