# from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Scenario:
    request_payload: dict
    decision_service_name: str
    rule_app: str
    ruleset: str

    def __init__(self, request_payload: dict,
                 decision_service_name: str,
                 rule_app: str,
                 ruleset: str):
        self.request_payload = request_payload
        self.decision_service_name = decision_service_name
        self.rule_app = rule_app
        self.ruleset = ruleset


# Scenarios passengers

class Flight(BaseModel):
    departsFromMemberState: bool
    landsInMemberState: bool
    operatingAirCarrierIsCommunityCarrier: bool
    stipulatedCheckInTime: str
    publishedDepartureTime: str


class Ticket(BaseModel):
    fare: str


class Passenger(BaseModel):
    status: str
    presentationForCheckInTime: str


class FlightEvent(BaseModel):
    flightEventType: str


flight = Flight(departsFromMemberState=False,
                landsInMemberState=True,
                operatingAirCarrierIsCommunityCarrier=False,
                stipulatedCheckInTime="",
                publishedDepartureTime="2024-09-19T19:00:00")

ticket = Ticket(fare="FreeOfCharge")

passenger = Passenger(status="HasAConfirmedReservation",
                      presentationForCheckInTime="2024-09-19T18:15:01")

flightEvent = FlightEvent(flightEventType="Delay")

scenario_passengers_1 = Scenario(
    request_payload={
        "flight": flight.dict(),
        "ticket": ticket.dict(),
        "passenger": passenger.dict(),
        "flightEvent": flightEvent.dict(),
    },
    decision_service_name='ec_passengers_demo_decision',
    rule_app='ec_passengers_deployment',
    ruleset='check_if_in_scope_of_application')


# Scenarios ibu

class Status(Enum):
    RECEIVED = 'RECEIVED'
    IN_PROCESS_VALIDATED = 'IN_PROCESS_VALIDATED'
    IN_PROCESS_ASSESSED = 'IN_PROCESS_ASSESSED'
    IN_PROCESS_VERIFIED = 'IN_PROCESS_VERIFIED'
    IN_PROCESS_LOSS_ADJUSTER_REPORTED = 'IN_PROCESS_LOSS_ADJUSTER_REPORTED'
    REJECTION_SENT = 'REJECTION_SENT'
    REJECTION_COMPLAINT = 'REJECTION_COMPLAINT'
    OFFER_SENT = 'OFFER_SENT'
    OFFER_ACCEPTED = 'OFFER_ACCEPTED'
    PAID = 'PAID'
    CLOSED = 'CLOSED'


class PreferredChannel(Enum):
    email = 'email'
    mail = 'mail'
    SMS = 'SMS'
    phone = 'phone'


class Client(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    # dateOfBirth: Optional[datetime] = None
    dateOfBirth: Optional[str] = None

    # firstContractDate: Optional[datetime] = None
    firstContractDate: Optional[str] = None

    cltvPercentile: Optional[int] = None
    propensityToUpgradePolicy: Optional[float] = None
    preferredChannel: Optional[PreferredChannel] = None


class Motive(Enum):
    UnsatisfiedWithDelay = 'UnsatisfiedWithDelay'
    UnsatisfiedWithReimbursedAmount = 'UnsatisfiedWithReimbursedAmount'
    UnsatisfiedWithAppliedCoverages = 'UnsatisfiedWithAppliedCoverages'
    UnsatisfiedWithQualityOfCustomerService = 'UnsatisfiedWithQualityOfCustomerService'
    InformationInquiry = 'InformationInquiry'


class ClientInteraction(BaseModel):

    # date: Optional[datetime] = None
    date: Optional[str] = None

    # motive: Optional[Motive] = None
    motive: Optional[str] = None

    intentionToLeave: Optional[bool] = None
    competitorName: Optional[str] = None
    competitorPolicyName: Optional[str] = None
    competitorPrice: Optional[float] = None

    # desiredResolutionDate: Optional[datetime] = None
    # desiredReimbursementDate: Optional[datetime] = None

    desiredResolutionDate: Optional[str] = None
    desiredReimbursementDate: Optional[str] = None

    expectedAmount: Optional[float] = None
    unsatisfiedWithDeductible: Optional[bool] = None


class Type(Enum):
    Wind = 'Wind'
    Hail = 'Hail'
    Fire = 'Fire'
    Lightning = 'Lightning'
    WaterDamage = 'WaterDamage'
    Freezing = 'Freezing'
    OtherDamage = 'OtherDamage'
    Theft = 'Theft'


class Type1(Enum):
    Car = 'Car'
    Motorbike = 'Motorbike'
    Truck = 'Truck'
    Lorry = 'Lorry'
    Land = 'Land'
    MainResidencialBuilding = 'MainResidencialBuilding'
    AuxiliaryResidencialBuilding = 'AuxiliaryResidencialBuilding'
    AuxiliaryNonResidencialBuilding = 'AuxiliaryNonResidencialBuilding'
    Flat = 'Flat'
    ParkingLot = 'ParkingLot'
    PersonalObject = 'PersonalObject'


class InsurableObject(BaseModel):
    type: Optional[Type1] = None
    description: Optional[str] = None
    estimatedValue: Optional[float] = None


class PolicyType(Enum):
    Auto = 'Auto'
    Home = 'Home'
    PersonalObject = 'PersonalObject'
    Life = 'Life'
    Health = 'Health'


class SubType(Enum):
    AutoThirdParty = 'AutoThirdParty'
    AutoAllRisk = 'AutoAllRisk'
    HomeBuildingsOnly = 'HomeBuildingsOnly'
    HomeBuildingsAndContent = 'HomeBuildingsAndContent'


class Option(Enum):
    SubstitutionVehicle = 'SubstitutionVehicle'
    ContentIncluded = 'ContentIncluded'
    NoDeductible = 'NoDeductible'


class Code(Enum):
    Wind = 'Wind'
    Hail = 'Hail'
    Fire = 'Fire'
    Lightning = 'Lightning'
    WaterDamage = 'WaterDamage'
    Freezing = 'Freezing'
    OtherDamage = 'OtherDamage'
    Theft = 'Theft'


class SubscribedCoverage(BaseModel):
    insurableObject: Optional[InsurableObject] = None
    code: Optional[Code] = None
    protectionAmount: Optional[float] = None
    deductible: Optional[float] = None


class Action(BaseModel):
    explanationCode: Optional[str] = None
    typeDisc__: str


class Assign(BaseModel):
    explanationCode: Optional[str] = None


class Channel(Enum):
    email = 'email'
    mail = 'mail'
    SMS = 'SMS'
    phone = 'phone'


class MessageType(Enum):
    ApologyOnly = 'ApologyOnly'
    SorryAboutPerceptionButFair = 'SorryAboutPerceptionButFair'
    AcknowledgmentOfReceipt = 'AcknowledgmentOfReceipt'
    Proposal = 'Proposal'


class CommunicateWithClient(Action):
    channel: Optional[Channel] = None
    messageType: Optional[MessageType] = None


class Discount(Action):
    description: Optional[str] = None
    percentage: Optional[float] = None


class DiscountOnNextRenewal(Action):
    description: Optional[str] = None
    percentage: Optional[float] = None


class InfoElement(BaseModel):
    path: Optional[str] = None
    questionId: Optional[str] = None
    type: Optional[str] = None


class Recipient(Enum):
    CallCenterClientRepresentative = 'CallCenterClientRepresentative'
    SpecializedClientRepresentative = 'SpecializedClientRepresentative'
    ClaimsExpert = 'ClaimsExpert'
    QualitySpecialist = 'QualitySpecialist'


class Reassign(Action):
    recipient: Optional[Recipient] = None
    suggestion: Optional[str] = None


class ReassignWithCallback(Action):
    recipient: Optional[Recipient] = None
    suggestion: Optional[str] = None
    callBackDeadline: Optional[int] = None


class SimpleUpsellProposal(Action):
    description: Optional[str] = None


class TaskSequence(Action):
    tasks: Optional[list[Assign]] = None


class Voucher(Action):
    description: Optional[str] = None


class Error(BaseModel):
    code: Optional[int] = Field(None, description='HTTP error code.')
    message: Optional[str] = Field(None, description='Error message.')
    details: Optional[str] = Field(None, description='Detailed error message.')
    errorCode: Optional[str] = Field(None, description='Product error code.')


class Response(BaseModel):
    actions: Optional[list[Action]] = None
    missingInfoElements: Optional[list[InfoElement]] = None
    outputTraces: Optional[list[str]] = None


class Damage(BaseModel):
    insurableObject: Optional[InsurableObject] = None
    type: Optional[Type] = None

    # date: Optional[datetime] = None
    date: Optional[str] = None


class InsurancePolicy(BaseModel):
    id: Optional[int] = None

    # effectiveDate: Optional[datetime] = None
    # expirationDate: Optional[datetime] = None

    effectiveDate: Optional[str] = None
    expirationDate: Optional[str] = None

    # policyType: Optional[PolicyType] = None
    policyType: Optional[str] = None

    # subType: Optional[SubType] = None
    subType: Optional[str] = None

    client: Optional[Client] = None
    coverages: Optional[list[SubscribedCoverage]] = Field(None)
    options: Optional[list[Option]] = None


class Request(BaseModel):
    field__DecisionID__: Optional[str] = Field(
        None,
        alias='__DecisionID__',
        description='Unique identifier representing the execution of the decision service operation. If it is not specified, it will be computed automatically.',
    )
    complaint: Optional['ComplaintOnClaim'] = None


class ActualCoverage(BaseModel):
    settlementOffer: Optional['ClaimSettlementOffer'] = None
    subscribedCoverage: Optional[SubscribedCoverage] = None
    applies: Optional[bool] = None
    description: Optional[str] = None
    reimbursementFactor: Optional[float] = None
    deductible: Optional[float] = None


class Claim(BaseModel):
    id: Optional[int] = None
    # status: Optional[Status] = None => CHANGED TO ->
    status: Optional[str] = None

    # creationDate: Optional[datetime] = None
    creationDate: Optional[str] = None

    targetDurationInDays: Optional[int] = None
    policy: Optional[InsurancePolicy] = None
    damages: Optional[list[Damage]] = Field(None)
    settlementOffer: Optional['ClaimSettlementOffer'] = None


class ClaimSettlementOffer(BaseModel):
    claim: Optional[Claim] = None

    # creationDate: Optional[datetime] = None
    creationDate: Optional[str] = None

    cancelContractAtExpiration: Optional[bool] = None
    cancelContractObjectCeased: Optional[bool] = None
    clientResponsibleForDamage: Optional[bool] = None
    actualCoverages: Optional[list[ActualCoverage]] = Field(None)


class ComplaintOnClaim(BaseModel):
    claim: Optional[Claim] = None
    interactions: Optional[list[ClientInteraction]] = None


scenario_ibu_1 = Scenario(
    request_payload={
        "complaint": ComplaintOnClaim(
            claim=Claim(
                policy=InsurancePolicy(
                    policyType=PolicyType.Auto,
                    subType=SubType.AutoThirdParty,
                    client=Client(
                        firstName="Joe",
                        lastName="Smith",
                        cltvPercentile=56,
                        propensityToUpgradePolicy=0.34
                    ),
                    coverages=[],
                    options=[]
                ),
                status=Status.IN_PROCESS_VERIFIED,
                creationDate="2024-04-05",
                damages=[],
                settlementOffer=None
            ),
            interactions=[
                ClientInteraction(
                    date="2024-04-15",
                    motive=Motive.UnsatisfiedWithAppliedCoverages,
                    intentionToLeave=False
                )
            ]).dict()

    },
    decision_service_name='ds-insurance-pc-claims-nba',
    rule_app='ComplaintHandling',
    ruleset='nextBestAction')
