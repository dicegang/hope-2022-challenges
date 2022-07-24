#!/usr/local/bin/python

import torch
import pickle
import base64
import secrets
import os

class UnpicklerWrapper:
    def find_class(self, module, name):
        if module+"."+name in (
            "builtins.set",
            "collections.OrderedDict",
            "torch.nn.modules.activation.LogSigmoid",
            "torch.nn.modules.activation.LogSoftmax",
            "torch.nn.modules.activation.ReLU",
            "torch.nn.modules.activation.Sigmoid",
            "torch.nn.modules.activation.Softmax",
            "torch.nn.modules.batchnorm.BatchNorm1d",
            "torch.nn.modules.batchnorm.BatchNorm2d",
            "torch.nn.modules.batchnorm.BatchNorm3d",
            "torch.nn.modules.conv.Conv1d",
            "torch.nn.modules.conv.Conv2d",
            "torch.nn.modules.conv.ConvTranspose1d",
            "torch.nn.modules.conv.ConvTranspose2d",
            "torch.nn.modules.dropout.Dropout2d",
            "torch.nn.modules.dropout.Dropout3d",
            "torch.nn.modules.flatten.Flatten",
            "torch.nn.modules.linear.Linear",
            "torch.nn.modules.loss.BCELoss",
            "torch.nn.modules.loss.BCEWithLogitsLoss",
            "torch.nn.modules.loss.CrossEntropyLoss",
            "torch.nn.modules.loss.L1Loss",
            "torch.nn.modules.loss.MSELoss",
            "torch.nn.modules.pooling.AvgPool2d",
            "torch.nn.modules.pooling.MaxPool2d",
            "torch._utils._rebuild_parameter",
            "torch._utils._rebuild_tensor_v2",
            "torch.Size",
            "torch.BFloat16Storage",
            "torch.BoolStorage",
            "torch.CharStorage",
            "torch.ComplexDoubleStorage",
            "torch.ComplexFloatStorage",
            "torch.HalfStorage",
            "torch.IntStorage",
            "torch.LongStorage",
            "torch.QInt32Storage",
            "torch.QInt8Storage",
            "torch.QUInt8Storage",
            "torch.ShortStorage",
            "torch.storage._StorageBase",
            "torch.ByteStorage",
            "torch.DoubleStorage",
            "torch.FloatStorage",
            "torch._C.HalfStorageBase",
            "torch._C.QInt32StorageBase",
            "torch._C.QInt8StorageBase",
            "torch.storage._TypedStorage",
        ):
            return super().find_class(module, name)
        else:
            raise Exception("Hacking detected!")

# replace find_class with our safe one
_load_co_consts = list(torch.serialization._load.__code__.co_consts)
unpickler_co_consts = list(_load_co_consts[7].co_consts)
unpickler_co_consts[1] = UnpicklerWrapper.find_class.__code__
_load_co_consts[7] = _load_co_consts[7].replace(co_consts=tuple(unpickler_co_consts))
torch.serialization._load.__code__ = torch.serialization._load.__code__.replace(co_consts=tuple(_load_co_consts))

# old stuff is dangerous
torch.serialization._legacy_load = None

try:
    with open(filename := "/tmp/"+secrets.token_hex(), "wb") as f:
        data = base64.b64decode(input("Enter base64-encoded model: "))
        if len(data) > 1000000: raise Exception("Model too big")
        f.write(data)

    model = torch.load(filename)

    # Machine learning is magic!
    model.solve_world_hunger()
finally:
    os.remove(filename)
