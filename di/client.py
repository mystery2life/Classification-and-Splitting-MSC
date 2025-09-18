from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from core.config import settings

def make_client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(settings.AZ_DI_ENDPOINT, AzureKeyCredential(settings.AZ_DI_KEY))
