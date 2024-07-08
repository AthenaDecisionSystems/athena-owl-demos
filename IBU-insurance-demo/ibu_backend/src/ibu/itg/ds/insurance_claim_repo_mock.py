"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json,logging
from datetime import datetime
from ibu.itg.ds.insurance_claim_repo import InsuranceClaimRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *


class InsuranceClaimInMem(InsuranceClaimRepositoryInterface):

    def __init__(self):
        self.CLAIMSDB = dict()
        self.initialize_claims_db()

    def add_claim(self, claim: Claim):
        self.CLAIMSDB[claim.id] = claim
    


    def initialize_claims_db(self):
        claim2=Claim(id = 2,
                    policy=InsurancePolicy(id = 2,
                                        effectiveDate = datetime(2023, 6, 6, 0, 0),
                                        expirationDate = datetime(2024, 6, 6, 0, 0),
                                        policyType = 'Home', 
                                        subType = 'HomeBuildingsOnly', 
                                        client = Client(id = 2, 
                                                        firstName = 'Sonya',
                                                        lastName = 'Smith', 
                                                        dateOfBirth = datetime(1999, 3, 12, 0, 0),
                                                        firstContractDate = datetime(2023, 11, 12, 0, 0),
                                                        cltvPercentile=62, 
                                                        propensityToUpgradePolicy=0.61,
                                                        preferredChannel = PreferredChannel.phone), 
                                        coverages=[ 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                                         description='House', 
                                                                                                         estimatedValue=5000000.0), 
                                                                         code=Code.Wind, 
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding,
                                                                                                         description='House', 
                                                                                                         estimatedValue=5000000.0), 
                                                                         code=Code.Fire, 
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding,
                                                                                                         description='House',
                                                                                                         estimatedValue=5000000.0),
                                                                         code=Code.OtherDamage,
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                                         description='House', 
                                                                                                         estimatedValue=5000000.0), 
                                                                         code=Code.Hail, 
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                                         description='House', 
                                                                                                         estimatedValue=5000000.0), 
                                                                         code=Code.Lightning,
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                                         description='House', 
                                                                                                         estimatedValue=5000000.0), 
                                                                         code=Code.WaterDamage,
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.AuxiliaryNonResidencialBuilding,
                                                                                                         description='Wooden cabin', 
                                                                                                         estimatedValue=10000.0), 
                                                                         code=Code.Fire, 
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0), 
                                                      SubscribedCoverage(insurableObject=InsurableObject(type=Type1.Land,
                                                                                                         description='Land', 
                                                                                                         estimatedValue=600000.0), 
                                                                         code=Code.WaterDamage, 
                                                                         protectionAmount=100000.0, 
                                                                         deductible=3000.0)
                                                      ], 
                                        options=[]), 
                    damages=[Damage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                        description='House', 
                                                                                        estimatedValue=5000000.0), 
                                                        type=Type.WaterDamage,
                                                        lossValue=300.0, 
                                                        description='A carpet is damaged by water', 
                                                        date=datetime(2024, 4, 19, 0, 0),
                                                        repairable=True), 
                            Damage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding,
                                                                    description='House', 
                                                                    estimatedValue=5000000.0), 
                                    type=Type.WaterDamage,
                                    lossValue=1000.0, 
                                    description='Wooden flooring in living room has been damaged by water', 
                                    date=datetime(2024, 4, 19, 0, 0), 
                                    repairable=True)
                            ],
                    settlementOffer=ClaimSettlementOffer(claim=None, 
                                                         creationDate=datetime(2024, 4, 26, 0, 0), 
                                                         cancelContractAtExpiration=False, 
                                                         cancelContractObjectCeased=False, 
                                                         clientResponsibleForDamage=False, 
                                                         actualCoverages=[ActualCoverage(settlementOffer=None, 
                                                                                         subscribedCoverage=SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding,
                                                                                                                                                               description='House', 
                                                                                                                                                               estimatedValue=5000000.0),
                                                                                                                               code=Code.Wind,
                                                                                                                               protectionAmount=100000.0, 
                                                                                                                               deductible=3000.0), 
                                                                                         applies=False, 
                                                                                         description='WaterDamage coverage does not apply to the content of the building', 
                                                                                         reimbursementFactor=0.0, 
                                                                                         deductible=0.0), 
                                                                          ActualCoverage(settlementOffer=None, 
                                                                                         subscribedCoverage=SubscribedCoverage(insurableObject=InsurableObject(type=Type1.MainResidencialBuilding, 
                                                                                                                                                                                     description='House', 
                                                                                                                                                                                     estimatedValue=5000000.0), 
                                                                                                                                code=Code.Fire, 
                                                                                                                                protectionAmount=100000.0, 
                                                                                                                                deductible=3000.0), 
                                                                                         applies=True, 
                                                                                         description='WaterDamage due to a broken pipe - coverage applies to buildings', 
                                                                                         reimbursementFactor=0.8, 
                                                                                         deductible=1000.0)
                                                                          ]
                                                         ),
                    status=Status.IN_PROCESS_VERIFIED,
                    creationDate=datetime(2024, 2, 22, 0, 0),
                    targetDurationInDays=21,
                )
        
        self.add_claim(claim2)
        

    def get_claim(self, id: int) -> Claim:
        logging.info(f"---> In claim mock get with id: {id}")
        return self.CLAIMSDB.get(id, None)


    def get_claim_json(self, id: int) -> str:
        claim = self.get_claim(id)
        if claim == None:
            return f"No claim with id '{id}' found"
        return claim.model_dump_json()

    def get_all_claims_json(self) -> str:
        return json.dumps([claim.to_dict() for claim in self.CLAIMSDB.values()], indent=4)
    
    def get_all_claims(self) -> list[Claim]:
        return list(self.CLAIMSDB.values())
    
    












