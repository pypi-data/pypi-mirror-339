from dataclasses import dataclass
from typing import List, Optional

from documente_shared.application.payloads import camel_to_snake
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
            response_json = response.json()
            instance_data = response_json.get('data', {})
            return ProcessingCase.from_persist_dict(camel_to_snake(instance_data))
        return None

    def persist(self, instance: ProcessingCase) -> ProcessingCase:
        response = self.session.put(
            url=f"{self.api_url}/v1/processing-cases/{instance.uuid}/",
            json=instance.to_dict,
        )
        if response.status_code not in [200, 201]:
            raise Exception(f'Error persisting processing case: {response.text}')

        response_json = response.json()
        instance_data = response_json.get('data', {})
        return ProcessingCase.from_persist_dict(camel_to_snake(instance_data))

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
            instaces_data = raw_response.get('data', [])
            return [
                ProcessingCase.from_persist_dict(item_data)
                for item_data in camel_to_snake(instaces_data)
            ]
        return []