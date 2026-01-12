import requests
from config import ASAAS_API_KEY

ASAAS_URL = "https://www.asaas.com/api/v3"


def criar_pix(valor: float, descricao: str):
    url = f"{ASAAS_URL}/payments"

    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY
    }

    data = {
        "billingType": "PIX",
        "value": valor,
        "description": descricao
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    return response.json()
