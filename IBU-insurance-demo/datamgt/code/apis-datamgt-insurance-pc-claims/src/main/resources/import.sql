------------------------------------------
-- CLIENT 1 - David Martin
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (1, 'David', 'Martin', '1967-02-22', '2005-10-31', 56, 0.55, 'email');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (1, 'Auto', 'AutoThirdParty', '2023-06-06', '2024-06-06', 1);

------------------------------------------
-- CLIENT 2 - Sonia Smith
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (2, 'Sonya', 'Smith', '1999-03-12', '2023-11-12', 62, 0.61, 'phone');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (2, 'Home', 'HomeBuildingsOnly', '2023-06-06', '2024-06-06', 2);

------------------------------------------
-- CLIENT 3 - Zoe Durand
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (3, 'Zoe', 'Duran', '2001-10-31', '2024-01-15', 44, 0.19, 'email');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (3, 'Auto', 'AutoThirdParty', '2023-06-06', '2024-06-06', 3);

ALTER SEQUENCE client_seq RESTART WITH 4;
ALTER SEQUENCE insurancePolicy_seq RESTART WITH 4;


-- insurable objects attached to subscribed coverage
INSERT INTO insurableObject(id, type, description, estimatedValue)
    VALUES (1, 'Car', 'Car', 5000000);

INSERT INTO insurableObject(id, type, description, estimatedValue)
    VALUES (101, 'MainResidencialBuilding', 'House', 5000000);
INSERT INTO insurableObject(id, type, description, estimatedValue)
    VALUES (102, 'Land', 'Land', 600000);
INSERT INTO insurableObject(id, type, description, estimatedValue)
    VALUES (103, 'AuxiliaryNonResidencialBuilding', 'Wooden cabin', 10000);
ALTER SEQUENCE insurableObject_seq RESTART WITH 4;

-- subscribed coverages attached to policy
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (1, 'CarAccident', 12000, 1500, 1, 1);


INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (101, 'Fire', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (102, 'Wind', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (103, 'Hail', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (104, 'Lightning', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (105, 'WaterDamage', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (106, 'OtherDamage', 100000, 3000, 2, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (107, 'WaterDamage', 100000, 3000, 2, 102);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (108, 'Fire', 100000, 3000, 2, 103);
ALTER SEQUENCE subscribedCoverage_seq RESTART WITH 9;

------------------------------------------
-- WHAT HAS BEEN CLAIMED
------------------------------------------

-- claims attached to policy
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (1, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 1);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (2, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 2);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (3, 'PAID', '2022-10-12', 21, 3);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (4, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 3);
--ALTER SEQUENCE claim_seq RESTART WITH 5;

-- damages attached to claims
INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (1, '2024-04-19', 'CarAccident', true, 1000.0, 'car accident description', 1, 1);

INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (101, '2024-04-19', 'WaterDamage', true, 1000.0, 'Wooden flooring in living room has been damaged by water', 2, 101);
INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (102, '2024-04-19', 'WaterDamage', true, 300.0, 'A carpet is damaged by water', 2, 101);
--ALTER SEQUENCE damage_seq RESTART WITH 3;

-- claim settlement offers attached to a claim
INSERT INTO claimSettlementOffer(id, claim_id, creationDate, cancelContractAtExpiration, cancelContractObjectCeased, clientResponsibleForDamage)
    VALUES(1, 1, '2024-04-26', false, false, true);
INSERT INTO claimSettlementOffer(id, claim_id, creationDate, cancelContractAtExpiration, cancelContractObjectCeased, clientResponsibleForDamage)
    VALUES(2, 2, '2024-04-26', false, false, false);
--ALTER SEQUENCE claimSettlementOffer_seq RESTART WITH 2;

-- actual coverages attached to a claim settlement offer
INSERT INTO actualCoverage(id, settlementOffer_id, subscribedCoverage_id, applies, description, reimbursementFactor, deductible)
    VALUES(1, 2, 101, true, 'WaterDamage due to a broken pipe - coverage applies to buildings', 0.80, 1000.0);
INSERT INTO actualCoverage(id, settlementOffer_id, subscribedCoverage_id, applies, description, reimbursementFactor, deductible)
    VALUES(2, 2, 102, false, 'WaterDamage coverage does not apply to the content of the building', 0.0, 0.0);
ALTER SEQUENCE actualCoverage_seq RESTART WITH 3;
