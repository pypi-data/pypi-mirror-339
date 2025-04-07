from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Union

"""
Class interfaces for enerplex-api/src/models/response.model.ts
Version: 0.0.2
"""

T = TypeVar('T')

@dataclass
class ApiResponse(Generic[T]):
    successful: bool
    data: Optional[T]
    errorMessage: Optional[str]
    responseType: str
    dataType: Optional[str]
    api_version: str

    # We need constructors because dataclasses do not properly support inheritance of optional attributes.
    def __init__(
        self,
        successful: bool,
        responseType: str,
        api_version: str,
        data: T = None,
        errorMessage: str = "",
        dataType: str = ""
    ):
        self.successful = successful
        self.responseType = responseType
        self.api_version = api_version
        self.data = data
        self.errorMessage = errorMessage
        self.dataType = dataType


@dataclass
class SuccessResponse(ApiResponse[None]):
    # We need constructors because dataclasses do not properly support inheritance of optional attributes.
    def __init__(
        self,
        successful: bool,
        responseType: str,
        api_version: str,
        errorMessage: str = "",
        dataType: str = ""
    ):
        super().__init__(successful, responseType, api_version, None, errorMessage, dataType)


@dataclass
class DataResponse(ApiResponse[T]):
    # We need constructors because dataclasses do not properly support inheritance of optional attributes.
    def __init__(
        self,
        successful: bool,
        responseType: str,
        api_version: str,
        data: T = None,
        errorMessage: str = "",
        dataType: str = ""
    ):
        super().__init__(successful, responseType, api_version, data, errorMessage, dataType)

@dataclass
class ErrorResponse(ApiResponse[None]):
    # We need constructors because dataclasses do not properly support inheritance of optional attributes.
    def __init__(
        self,
        successful: bool,
        responseType: str,
        api_version: str,
        errorMessage: str,
        dataType: str = ""
    ):
        super().__init__(successful, responseType, api_version, None, errorMessage, dataType)



@dataclass
class LoginResponse(ApiResponse[None]):
    token: str
    expiresIn: str

    # We need constructors because dataclasses do not properly support inheritance of optional attributes.
    def __init__(
        self,
        successful: bool,
        responseType: str,
        api_version: str,
        token: str,
        expiresIn: str,
        data: T = None,
        errorMessage: str = "",
        dataType: str = ""
    ):
        super().__init__(successful, responseType, api_version, data, errorMessage, dataType)
        self.token = token
        self.expiresIn = expiresIn
