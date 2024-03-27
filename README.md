# This is a simple wrapper around the france travail API.

You will need to create an account to be able to fetch data from the API.

A simple usage example is inside the data_getter.py file.

https://francetravail.io/data/documentation

Basic usage:

Place your API Client and API Secret in the .env.example file and rename it to .env

```python
from france_travail_api import FranceTravailAPI

class MyGetter(FranceTravailAPI):
    def __init__(
        self,
        code_type_territoire,
        code_territoire,
        code_type_activite,
        code_activite,
        code_type_periode,
        code_type_nomenclature,
        testing: bool = False,
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

    # Now you can implement your own methods to fetch data from the API
    def get_job_seekers_of_last_12_months(self, **kwargs):
        
        body = {
            **self.params,
            **kwargs,
        }

        data = self.fetch_endpoint(
            "stats-offres-demandes-emploi/v1/indicateur/stat-demandeurs-entrant", body
        )

        return data
```

The fetch_endpoint method will return data converted in a pandas DataFrame.