"""Obligations module"""

from json import JSONDecodeError
import re
import httpx
from httpx import AsyncClient

from .errors import KatError, KatErrorType
from .data_models import KatObligationApiResponse, KatObligation

_REQUEST_TIMEOUT = 10
_KAT_INDIVIDUAL_URL = "https://e-uslugi.mvr.bg/api/Obligations/AND?obligatedPersonType=1&additinalDataForObligatedPersonType=1&mode=1&obligedPersonIdent={egn}&drivingLicenceNumber={license_number}"
_КАТ_BUSINESS_URL = "https://e-uslugi.mvr.bg/api/Obligations/AND?obligatedPersonType=2&additinalDataForObligatedPersonType=1&mode=1&obligedPersonIdent={egn}&personalDocumentNumber={govt_id_number}&uic={bulstat}"

ERR_INVALID_EGN = "EGN is not valid."
ERR_INVALID_LICENSE = "Driving License Number is not valid."
ERR_INVALID_USER_DATA = "User data (EGN and Driving license number combination) is not valid."

ERR_INVALID_GOV_ID = "Government ID Number is not valid."
ERR_INVALID_BULSTAT = "BULSTAT is not valid."

ERR_API_TOO_MANY_REQUESTS = "KAT API too many requests for ID={identifier}"
ERR_API_TIMEOUT = "KAT API request timed out for ID={identifier}"
ERR_API_DOWN = "KAT API was unable to process the request. Try again later."
ERR_API_MALFORMED_RESP = " KAT API returned a malformed response: {data}"
ERR_API_UNKNOWN = "KAT API returned an unknown error: {error}"

REGEX_EGN = r"^[0-9]{2}[0,1,2,4][0-9][0-9]{2}[0-9]{4}$"
REGEX_DRIVING_LICENSE = r"^[0-9]{9}$"

# ID Format Supports "123456789" and "AA1234567"
REGEX_GOVT_ID = r"^[0-9]{9}|[A-Z]{2}[0-9]{7}$"
REGEX_BULSTAT = r"^[0-9]{9}$"


class KatApiClient:
    """KAT API manager"""

    def __self__(self):
        """Initialize API client."""

    def __validate_response(self, data: KatObligationApiResponse):
        """Validate if the user is valid"""

        for od in data.obligations_data:
            if od.error_no_data_found is True:
                raise KatError(
                    KatErrorType.VALIDATION_USER_NOT_FOUND_ONLINE, ERR_INVALID_USER_DATA)

            if od.error_reading_data is True:
                raise KatError(
                    KatErrorType.API_ERROR_READING_DATA, ERR_API_DOWN)

    async def _get_obligations_from_url(
        self, url: str, identifier: str, external_httpx_client: AsyncClient = None
    ) -> list[KatObligation]:
        """
        Gets a list of obligations/fines from URL

        :param url: URL to fetch the data from
        :param identifier: Person identifier - Government ID Number or Driving License Number

        """
        data = {}

        try:
            if external_httpx_client:
                resp = await external_httpx_client.get(url, timeout=_REQUEST_TIMEOUT)
                data = resp.json()
                resp.raise_for_status()
            else:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url, timeout=_REQUEST_TIMEOUT)

                    resp.raise_for_status()

                    if (resp.headers.get("content-type") == "text/html" and "Достигнат е максимално допустимият брой заявки към системата" in resp.text):
                        raise KatError(
                            KatErrorType.API_TOO_MANY_REQUESTS,
                            ERR_API_TOO_MANY_REQUESTS.format(
                                identifier=identifier)
                        )

                    data = resp.json()

        except httpx.TimeoutException as ex_timeout:
            raise KatError(KatErrorType.API_TIMEOUT, ERR_API_TIMEOUT.format(
                identifier=identifier)) from ex_timeout

        except httpx.HTTPError as ex_apierror:
            raise KatError(KatErrorType.API_UNKNOWN_ERROR, ERR_API_UNKNOWN.format(
                error=str(ex_apierror))) from ex_apierror

        except JSONDecodeError as ex_decode_err:
            raise KatError(KatErrorType.API_UNKNOWN_ERROR, ERR_API_MALFORMED_RESP.format(
                data=str(ex_decode_err))) from ex_decode_err

        if "obligationsData" not in data:
            # This should never happen.
            # If we go in this if, this probably means they changed their schema
            raise KatError(KatErrorType.API_INVALID_SCHEMA,
                           ERR_API_MALFORMED_RESP.format(data=data))

        api_data = KatObligationApiResponse(data)
        self.__validate_response(api_data)

        response = []
        for og in api_data.obligations_data:
            for ob in og.obligations:
                response.append(ob)

        return response

    async def validate_credentials_individual(
            self,
            egn: str,
            license_number: str,
            external_httpx_client: AsyncClient = None) -> bool:
        """
        Validates the combination of EGN and License number for an individual

        :param person_egn: EGN (National Identification Number)
        :param driving_license_number: Driver's License Number

        """

        # Validate EGN
        if egn is None or re.search(REGEX_EGN, egn) is None:
            raise KatError(KatErrorType.VALIDATION_EGN_INVALID,
                           ERR_INVALID_EGN)

        # Validate License Number
        if license_number is None or re.search(REGEX_DRIVING_LICENSE, license_number) is None:
            raise KatError(
                KatErrorType.VALIDATION_ID_DOCUMENT_INVALID, ERR_INVALID_LICENSE)

        data = await self.get_obligations_individual(egn, license_number, external_httpx_client)

        return data is not None

    async def validate_credentials_business(
            self,
            egn: str,
            govt_id_number: str,
            bulstat: str,
            external_httpx_client: AsyncClient = None) -> bool:
        """
        Validates the combination of EGN, Government ID Number and BULSTAT for a business

        :param person_egn: EGN (National Identification Number)
        :param govt_id_number: Government ID Number
        :param bulstat: Business BULSTAT

        """

        # Validate EGN
        if egn is None or re.search(REGEX_EGN, egn) is None:
            raise KatError(KatErrorType.VALIDATION_EGN_INVALID,
                           ERR_INVALID_EGN)

        # Validate Government ID Number
        if govt_id_number is None or re.search(REGEX_GOVT_ID, govt_id_number) is None:
            raise KatError(
                KatErrorType.VALIDATION_ID_DOCUMENT_INVALID, ERR_INVALID_GOV_ID)

        # Validate BULSTAT
        if govt_id_number is None or re.search(REGEX_BULSTAT, bulstat) is None:
            raise KatError(
                KatErrorType.VALIDATION_ID_DOCUMENT_INVALID, ERR_INVALID_BULSTAT)

        data = await self.get_obligations_business(egn, govt_id_number, bulstat, external_httpx_client)

        return data is not None

    async def get_obligations_individual(
        self, egn: str, license_number: str, external_httpx_client: AsyncClient = None
    ) -> list[KatObligation]:
        """
        Gets a list of obligations/fines for an individual

        :param person_egn: EGN (National Identification Number)
        :param driving_license_number: Driver's License Number
        """

        url = _KAT_INDIVIDUAL_URL.format(
            egn=egn, license_number=license_number)

        return await self._get_obligations_from_url(url, license_number, external_httpx_client)

    async def get_obligations_business(
        self, egn: str, govt_id_number: str, bulstat: str, external_httpx_client: AsyncClient = None
    ) -> list[KatObligation]:
        """
        Gets a list of obligations/fines for an individual

        :param person_egn: EGN (National Identification Number)
        :param driving_license_number: Driver's License Number
        """

        url = _КАТ_BUSINESS_URL.format(
            egn=egn, govt_id_number=govt_id_number, bulstat=bulstat)

        return await self._get_obligations_from_url(url, govt_id_number, external_httpx_client)
