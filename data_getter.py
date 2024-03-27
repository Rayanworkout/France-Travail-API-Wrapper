from france_travail_api import FranceTravailAPI


class DataGetter(FranceTravailAPI):
    """
    This class is intended to get data from the FranceTravail API, using the wrapper
    It inherits from the FranceTravailAPI class, which defines the basic methods and parameters needed to make requests to the API.

    Then we parse the and make it available for the rest of the application.


    Methods:
            - get_job_seekers_of_last_12_months: Get the number of job seekers registered in the last 12 months.
            - get_hiring_statistics: Get statistics about hiring.


            - **kwargs: other optional parameters for each method ->  dernierePeriode: bool,
                                                                      listeCodePeriode: array[string],
                                                                      listeCodeNomenclature: array[string]
                                                                      sansCaracteristiques: bool,
                                                                      listeCaracteristiques: array[object]

            Specific kwargs are detailed in the docstrings of each method.
    """

    def __init__(
        self,
        testing: bool = False,
        code_type_territoire: str = "DEP",
        code_territoire: str = "13",
        code_type_activite: str = "ROME",
        code_activite: str = "M1805",
        code_type_periode: str = "TRIMESTRE",
        code_type_nomenclature: str = "CATCAND",
    ) -> None:

        super().__init__(
            testing,
            code_type_territoire,
            code_territoire,
            code_type_activite,
            code_activite,
            code_type_periode,
            code_type_nomenclature,
        )

    def get_job_seekers_of_last_12_months(
        self,
        **kwargs,
    ) -> dict:
        """
        Method to get the number of job seekers registered in the last 12 months.

        https://francetravail.io/data/api/marche-travail/documentation#/api-reference/operations/rechercherStatDemandeursEntrants
        """

        body = {
            **self.params,
            **kwargs,
        }

        data = self.fetch_endpoint(
            "stats-offres-demandes-emploi/v1/indicateur/stat-demandeurs-entrant", body
        )

        return data

    def get_hiring_statistics(
        self,
        **kwargs,
    ):
        """
        Get statistics about hiring.

        parameters:
                see FranceTravailAPI.__init__() docstring

        https://francetravail.io/data/api/marche-travail/documentation#/api-reference/operations/rechercherStatEmbauches
        """
        body = {
            **self.params,
            **kwargs,
        }

        data = self.fetch_endpoint(
            "stats-offres-demandes-emploi/v1/indicateur/stat-embauches", body
        )

        return data

    def get_stats_job_offers(self, **kwargs):

        body = {
            **self.params,
            **kwargs,
        }

        self.fetch_endpoint("stats-offres-demandes-emploi/v1/indicateur/stat-offres", body)
