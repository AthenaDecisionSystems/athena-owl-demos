"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from dataclasses import dataclass, asdict
import json
from .ComplaintHandling_generated_model import *


class InsuranceClaimRepositoryInterface:

    def get_all_claims(self) -> list[Claim]:
        return []
    
    def get_claim(self, id: int) -> Claim:
        return None
    
    def get_claim_json(self, id: int) -> str:
        return None

    def get_all_claims_json(self) -> str:
        return None
    
