import requests
from datetime import date
import json
from company_account import CompanyAccount

MF_TEST_URL = "https://wl-test.mf.gov.pl"

def check_nip(nip: str):
    cdate = date.today().isoformat()  # YYYY-MM-DD
    url = f"{MF_TEST_URL}/api/search/nip/{nip}?date={cdate}"

    response = requests.get(url)
    print(url)
    print("HTTP status:", response.status_code)

    data = response.json()
    print("Full response:")
    print(json.dumps(data, indent=2, ensure_ascii=False))


## Example: replace with real NIPs
#check_nip("8461627563")   # known valid example
#print("\n" + "-" * 60 + "\n")
#check_nip("1111111111")   # invalid / non-existing


acc = CompanyAccount("Test Co", "8461627563")
acc.nip_api_check("8461627563")