from pydantic import BaseModel, Field



class OcpiTariff(BaseModel):
    '''
    OCPI 11.3.1. Tariff Object
    '''
    country_code: str = Field(min_length=2, max_length=2, description="""ISO-3166 alpha-2 country code of the CPO that 'owns' this Tariff.""")
    party_id: str = Field(
        min_length=3, max_length=3, description="""
        ID of the CPO that 'owns' this Traiff (following the ISO-15118
        standard).
        """,
    )