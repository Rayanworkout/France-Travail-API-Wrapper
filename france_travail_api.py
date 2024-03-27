import os
import io
import pandas as pd
import requests

from dotenv import load_dotenv


class FranceTravailAPI:
    """
    This class is a wrapper around the FranceTravail API.

    I use it to define the methods needed to make requests to the API.
    The class that inherits from it will define the different endpoints.


    Methods:
            - get_or_refresh_access_token: Get the access token from the API, needed to make requests.
            - get_job_seekers_of_last_12_months: Get the number of job seekers registered in the last 12 months.

    https://francetravail.io/data/documentation

    """

    BASE_URL = "https://api.francetravail.io/partenaire/"
    load_dotenv()

    GOUV_API_CLIENT_ID = os.getenv("GOUV_API_CLIENT_ID")
    GOUV_API_SECRET_KEY = os.getenv("GOUV_API_SECRET_KEY")

    def __init__(
        self,
        testing,
        code_type_territoire,
        code_territoire,
        code_type_activite,
        code_activite,
        code_type_periode,
        code_type_nomenclature,
    ) -> None:
        """
        parameters:
                - code_type_territoire: the type of territory (e.g "REG", "DEP", "COM", "PAYS" ...)
                - code_territoire:  the code of the territory (e.g "11", "75", "75056" ...)
                - code_type_activite: the type of activity (e.g "NAF", "ROME" ...) https://blog.easyfichiers.com/wp-content/uploads/2014/08/Liste-code-naf-ape.pdf
                - code_activite: the code of the activity (e.g "6201Z", "A110" ...)
                - code_type_periode: the type of period (e.g "ANNEE", "TRIMESTRE" ...)

        """

        self.access_token = (
            self.get_or_refresh_access_token() if testing is False else "test_token"
        )  # For testing purposes

        # Headers and parameters for the requests

        self.code_type_territoire = code_type_territoire
        self.code_territoire = code_territoire
        self.code_type_activite = code_type_activite
        self.code_activite = code_activite
        self.code_type_periode = code_type_periode
        self.code_type_nomenclature = code_type_nomenclature

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/xml, application/json",
        }

        self.params = {
            "codeTypeTerritoire": self.code_type_territoire,
            "codeTerritoire": self.code_territoire,
            "codeTypeActivite": self.code_type_activite,
            "codeActivite": self.code_activite,
            "codeTypePeriode": self.code_type_periode,
            "codeTypeNomenclature": self.code_type_nomenclature,
        }

    @classmethod
    def to_dataframe(cls, xml_string: str) -> pd.DataFrame:
        """
        Method to convert an XML string to a pandas DataFrame.

        We use the pandas.read_xml method to convert the XML string to a DataFrame.

        https://pandas.pydata.org/docs/reference/api/pandas.read_xml.html
        """

        with io.StringIO(xml_string) as xml_content:
            df = pd.read_xml(xml_content)

        # Remove rows where all values are None or NaN
        df.dropna(how="all", inplace=True)

        # Remove columns where all values are None or NaN
        df.dropna(axis=1, how="all", inplace=True)

        # Reset index
        df.reset_index(drop=True, inplace=True)

        return df

    @classmethod
    def get_or_refresh_access_token(
        cls,
        realm: str = "partenaire",
        scopes: list = ["api_stats-offres-demandes-emploiv1", "offresetdemandesemploi"],
    ) -> str:
        """
        Method to get the access token from the FranceTravail API.

        We need an access token to be able to make requests to the API, and our credentials to get an access token.
        These credentials are stored in the .env file.

        Each access token has a limited lifetime, and we need to get a new one when it expires.
        The default lifetime is 1499 seconds (25 minutes).

        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/generer-access-token
        """

        url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": cls.GOUV_API_CLIENT_ID,
            "client_secret": cls.GOUV_API_SECRET_KEY,
            "scope": " ".join(scopes),
        }

        response = requests.post(url + f"?realm={realm}", headers=headers, data=body)

        # Raise an error if the request was unsuccessful
        response.raise_for_status()

        # Otherwise, we parse the response
        response = response.json()

        error = response.get("error")

        match error:
            case "invalid_client":
                raise ValueError("Invalid client or secret key credentials.")
            case "invalid_scope":
                raise ValueError("Invalid or unauthorized scope.")
            case "unsupported_grant_type":
                raise ValueError("Unsupported grant type.")
            case _:
                pass

        # Unpacking the response dictionary
        scope, expires_in, token_type, access_token = (
            response["scope"],
            response["expires_in"],
            response["token_type"],
            response["access_token"],
        )

        return access_token

    def fetch_endpoint(self, endpoint: str, body: dict) -> pd.DataFrame:
        """
        Method to fetch an endpoint from the API.

        We make a POST request to the API with the url, headers and body parameters.
        We then parse the response to a pandas DataFrame.

        """

        url = FranceTravailAPI.BASE_URL + endpoint

        response = requests.post(url, headers=self.headers, json=body)

        # Raise an error if the request was unsuccessful
        response.raise_for_status()

        # Otherwise, we parse the response
        data = self.to_dataframe(response.text)

        return data
