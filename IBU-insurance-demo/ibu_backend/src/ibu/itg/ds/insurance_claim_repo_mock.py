"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json,logging
from ibu.itg.ds.insurance_claim_repo import InsuranceClaimRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *
class InsuranceClaimInMem(InsuranceClaimRepositoryInterface):

    def __init__(self):
        self.CLAIMSDB = dict()
        self.initialize_claims_db()

    def add_claim(self, claim: Claim):
        self.CLAIMSDB[claim.id] = claim
    


    def initialize_claims_db(self):
        c1 = Client(id=1,firstName = "Jane",
                            lastName = "Dupont",
                            paymentScore=3,
                            claimsScore=2,
                            vip=False)
        p1 = InsurancePolicy()
        p1.client =c1
        claim1 = Claim(id=2, 
                       status= Status.RECEIVED,
                       policy= p1,
                       targetDurationInDays=30, 
                       damages=[Damage( insurableObject= InsurableObject(type=Type1.Car,estimatedValue=10000))])

        self.add_claim(claim1)
        claim2=Claim(id=2,
                     policy=InsurancePolicy(
                        client = Client(
                            firstName = "Joe",
                            lastName = "Smith",
                            paymentScore=3,
                            claimsScore=2,
                            vip=False
                        ),
                        coverages = None
                    ),
                    status=Status.IN_PROCESS_VERIFIED,
                    targetDurationInDays=40,
                    creationDate="2024-04-15"
                )
        self.add_claim(claim2)
        """
        value: int
    standard_handling_time: int
    actual_handling_time: int
    reimbursement_amount: int = 0
    deductible: int = 0
    , 1000, 30, 35, 900, 100)
    """
        """
        
        sinistre2 = Claim("S2", "Client6", 2000, 30, 28, 1500, 500)
        sinistre3 = Claim("S3", "Client1", 3000, 40, 60, 2700, 300)
        sinistre4 = Claim("S4", "Client2", 4000, 40, 59, 3800, 200)
        sinistre101 = Claim("S101", "Client10", 3000, 40, 60, 2700, 300)
        sinistre201 = Claim("S201", "Client20", 3000, 40, 60, 2700, 300)
        
        self.add_claim(sinistre2)
        self.add_claim(sinistre3)
        self.add_claim(sinistre4)
        self.add_claim(sinistre101)
        self.add_claim(sinistre201)
    """

    def get_claim(self, id: int) -> Claim:
        logging.info(f"---> In claim mock get with id: {id}")
        return self.CLAIMSDB.get(id, None)


    def get_claim_json(self, id: int) -> str:
        claim = self.get_claim(id)
        if claim == None:
            return f"No claim with id '{id}' found"
        return claim.to_json()

    def get_all_claims_json(self) -> str:
        return json.dumps([claim.to_dict() for claim in self.CLAIMSDB.values()], indent=4)
    
    def get_all_claims(self) -> list[Claim]:
        return list(self.CLAIMSDB.values())
    
    












