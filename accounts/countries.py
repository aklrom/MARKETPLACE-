import phonenumbers
import pycountry

def get_countries_choices():
    choices=[]
    for region in phonenumbers.SUPPORTED_REGIONS:
        country=pycountry.countries.get(alpha_2=region)
        if country is None:
            continue
        name=getattr(country, "common_name", country.name)
        code = f"+{phonenumbers.country_code_for_region(region)}"
        choices.append((code,f"{name} ({code})"))

    return sorted(choices, key=lambda c: c[1])    