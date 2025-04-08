from dataclasses import dataclass
from typing import List, Optional

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.entities.processing_case_filters import ProcessingCaseFilters
from documente_shared.domain.repositories.processing_case import ProcessingCaseRepository
from documente_shared.infrastructure.documente_client import DocumenteClientMixin


@dataclass
class HttpProcessingCaseRepository(
    DocumenteClientMixin,
    ProcessingCaseRepository,
):
    def find(self, uuid: str, include_items: bool = False) -> Optional[ProcessingCase]:
        response = self.session.get(f"{self.api_url}/v1/processing-cases/{uuid}/")
        if response.status_code == 200:
            return ProcessingCase.from_dict(response.json())
        return None

    def persist(self, instance: ProcessingCase) -> ProcessingCase:
        response = self.session.put(
            url=f"{self.api_url}/v1/processing-cases/{instance.uuid}/",
            json=instance.to_dict,
        )
        if response.status_code not in [200, 201]:
            raise Exception(f'Error persisting processing case: {response.text}')
        return ProcessingCase.from_dict(response.json())

    def remove(self, instance: ProcessingCase):
        self.session.delete(f"{self.api_url}/v1/processing-cases/{instance.uuid}/")

    def filter(self, tenant_slug: str, filters: ProcessingCaseFilters) -> List[ProcessingCase]:
        response = self.session.get(
            url=f"{self.api_url}/v1/processing-cases/",
            headers={
                "X-Tenant": tenant_slug,
            }
        )
        if response.status_code == 200:
            raw_response = response.json()
            return [
                ProcessingCase.from_dict(item)
                for item in raw_response.get('data', [])
            ]
        return []