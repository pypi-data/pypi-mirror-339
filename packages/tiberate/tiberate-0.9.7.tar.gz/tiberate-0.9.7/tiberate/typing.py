import inspect
import pickle
import typing
from collections import defaultdict
from functools import wraps
from typing import Any, Dict, List, Union

import numpy as np
import torch
from loguru import logger
from torch import Tensor
from vdtoys.cache import CachedDict


class DataStruct:
    # data: Union[list, tuple]
    # include_special: bool
    # ntt_state: bool
    # montgomery_state: bool
    # origin: str
    # level: int

    def __init__(
        self,
        data: Union[list, tuple],
        include_special: bool,
        ntt_state: bool,
        montgomery_state: bool,
        level: int,
        description: str = None,
        *args,
        **kwargs,
    ):
        """
        Data structure:
        - data: the data in tensor format
        - include_special: Boolean, including the special prime channels or not.
        - ntt_state: Boolean, whether if the data is ntt transformed or not.
        - montgomery_state: Boolean, whether if the data is in the Montgomery form or not.
        - origin: String, where did this data came from - cipher text, secret key, etc.
        - level: Integer, the current level where this data is situated.
        - version: String, version number.
        """
        # todo might need a engine identifier to know which engine created this data
        self.data = data
        self.include_special = include_special
        self.ntt_state = ntt_state
        self.montgomery_state = montgomery_state
        self.level = level
        self.description = description

    def clone(self):
        """Clone the data structure.

        Returns:
            DataStruct or its subclasses: A new instance of the same class with cloned data.
        """
        cls = self.__class__  # Get the class of the current instance
        return cls(
            data=cls.copy_tensor_to_device_recursive(self.data, self.device),
            include_special=self.include_special,
            ntt_state=self.ntt_state,
            montgomery_state=self.montgomery_state,
            level=self.level,
            description=self.description,
        )

    @classmethod
    def wrap(cls, another: "DataStruct"):
        """Wrap another data structure into a new instance of the same class.
        Args:
            another (DataStruct): The data structure to wrap.
        Returns:
            DataStruct or its subclasses: A new instance of the same class with the same attributes as `another`.
        """
        return cls(
            data=another.data,
            include_special=another.include_special,
            ntt_state=another.ntt_state,
            montgomery_state=another.montgomery_state,
            level=another.level,
            description=another.description,
        )

    @classmethod
    def get_device_of_tensor(cls, data):
        """Get the device of the tensor in the data structure.

        Note: this method only checks the first found tensor of the data structure.
        It assumes that all elements in the data structure are on the same device.

        Args:
            data: The data structure to check.
        Returns:
            The device of the tensor.
        """
        # Recursively get the device of the tensor in the data structure
        if isinstance(data, Tensor):
            return data.device
        elif isinstance(data, list):
            return cls.get_device_of_tensor(data[0]) if data else "cpu"
        elif isinstance(data, tuple):  # legacy datastruct uses tuple
            return cls.get_device_of_tensor(data[0]) if data else "cpu"
        elif isinstance(data, dict):  # plaintext cache
            return (
                cls.get_device_of_tensor(list(data.values())[0])
                if data
                else "cpu"  # if data is empty, return cpu
            )
        elif isinstance(data, DataStruct):
            return cls.get_device_of_tensor(data.data)
        else:
            # logger.warning(
            #     f"Unsupported data type to get device: {type(data)}, will return 'cpu'."
            # )
            return "cpu"

    @property
    def device(self):
        """Get the device of the data structure.
        Returns:
            The device of the data structure.
        """
        return self.get_device_of_tensor(self.data)

    @classmethod
    def copy_tensor_to_device_recursive(cls, data, device: str, non_blocking=True):
        """Recursively move tensors in the data structure to a specified device.
        Args:
            data: The data structure to move.
            device: The target device.
        Returns:
            The data structure moved to the specified device.
        """
        # Recursively move tensors in the data structure to the specified device
        if isinstance(data, Tensor):
            return data.to(device, non_blocking=non_blocking)
        elif isinstance(data, list):
            return [cls.copy_tensor_to_device_recursive(item, device) for item in data]
        elif isinstance(data, tuple):  # legacy datastruct uses tuple
            return tuple(cls.copy_tensor_to_device_recursive(item, device) for item in data)
        elif isinstance(data, dict):  # plaintext cache
            return {
                cls.copy_tensor_to_device_recursive(
                    key, device
                ): cls.copy_tensor_to_device_recursive(value, device)
                for key, value in data.items()
            }
        elif isinstance(data, CachedDict):
            new_instance = data.__class__(data.generator_func)
            new_instance._cache = cls.copy_tensor_to_device_recursive(data._cache, device)
            return new_instance
        elif isinstance(data, DataStruct):
            return data.copy_to(device)
        else:
            # logger.warning(
            #     f"Unsupported data type to move to device: {type(data)}, returning the original data."
            # )
            return data

    def copy_to(self, device: str, non_blocking=True):
        """Copy the data structure to a specified device and return a new instance.
        Args:
            device: The target device.
        Returns:
            DataStruct or its subclasses: A new instance of the same class with data moved to the specified device.
        """
        cls = self.__class__
        return cls(
            data=cls.copy_tensor_to_device_recursive(
                data=self.data, device=device, non_blocking=non_blocking
            ),
            include_special=self.include_special,
            ntt_state=self.ntt_state,
            montgomery_state=self.montgomery_state,
            level=self.level,
            description=self.description,
        )

    def to(self, device: str, non_blocking=True):
        # alias for copy_to
        return self.copy_to(device, non_blocking)

    def dump(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def dumps(self):
        return pickle.dumps(self)

    @classmethod
    def load(cls, path: str) -> "DataStruct":
        with open(path, "rb") as f:
            return pickle.load(f)

    @classmethod
    def loads(cls, data) -> "DataStruct":
        return pickle.loads(data)

    def __repr__(self):
        return f"{self.__class__.__name__}(data={self.data}, include_special={self.include_special}, ntt_state={self.ntt_state}, montgomery_state={self.montgomery_state}, level={self.level}, description={self.description})"

    def __str__(self):
        return self.__repr__()  # todo for better readability


# ================== #
#  Cipher Structures #
# ================== #


class Ciphertext(DataStruct):
    pass


class CiphertextTriplet(DataStruct):
    # todo does CiphertextTriplet even exits ntt_state and montgomery_state?
    pass


# ================== #
#  Key Structures    #
# ================== #


class SecretKey(DataStruct):
    # todo does secret key even exits ntt_state and montgomery_state?
    pass


class EvaluationKey(SecretKey):
    pass


class PublicKey(DataStruct):
    pass


class KeySwitchKey(DataStruct):
    pass


class RotationKey(KeySwitchKey):
    delta: int = None
    pass

    def copy_to(self, device, non_blocking=True) -> "RotationKey":
        new_instance = super().copy_to(device, non_blocking)
        new_instance.delta = self.delta
        return new_instance


class GaloisKey(DataStruct):
    pass


class ConjugationKey(DataStruct):
    pass


# ================== #
#  Plaintext Cache   #
# ================== #


class Plaintext(DataStruct):
    def __init__(
        self,
        src: Union[list, tuple],
        *,
        cache: Dict[int, Dict[str, Any]] = None,  # level: {what_cache: cache_data}
        padding=True,  # todo remove padding flag in legacy code
        scale=None,  # by default None, which means use engine's parameter
    ):
        if not isinstance(src, torch.Tensor):
            src = torch.tensor(src)
        if src.dim() == 2 and src.size(0) == 1:
            src = src.squeeze(0)
        assert src.dim() == 1, RuntimeError(
            f"Plaintext source data must be 1D tensor, got {src.dim()}D tensor."
        )
        self.src = src
        self.data = cache or defaultdict(dict)  # cache is alias of data
        self.padding = padding
        self.scale = scale

    @property
    def cache(self):
        return self.data

    @cache.setter
    def cache(self, value):
        self.data = value

    def clone(self):
        cls = self.__class__
        cache = cls.copy_tensor_to_device_recursive(self.cache, self.device)
        return cls(self.src, cache=cache)

    @property
    def device(self):
        if not self.cache:
            return self.get_device_of_tensor(self.src)
        else:
            return self.get_device_of_tensor(self.cache)

    def copy_to(self, device, non_blocking=True):
        cls = self.__class__
        cache = cls.copy_tensor_to_device_recursive(
            data=self.cache, device=device, non_blocking=non_blocking
        )
        return cls(self.src, cache=cache)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(data={self.src}, cached levels={list(self.cache.keys())})"
        )

    @property
    def level(self):
        raise NotImplementedError("Plaintext does not have level attribute.")
