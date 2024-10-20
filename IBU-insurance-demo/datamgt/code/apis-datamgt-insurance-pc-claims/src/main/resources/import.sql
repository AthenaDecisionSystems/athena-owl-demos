------------------------------------------
-- CLIENT 1 - David Martin
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (176541, 'David', 'Martin', '1967-02-22', '2005-10-31', 56, 0.55, 'email');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (149231, 'Auto', 'AutoThirdParty', '2023-06-06', '2024-06-06', 176541);

------------------------------------------
-- CLIENT 2 - Sonia Smith
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (245678, 'Sonya', 'Smith', '1999-03-12', '2023-11-12', 62, 0.61, 'phone');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (250304, 'Home', 'HomeBuildingsOnly', '2023-06-06', '2024-06-06', 245678);

------------------------------------------
-- CLIENT 3 - Zoe Durand
------------------------------------------
-- client data
INSERT INTO client(id, firstName, lastName, dateOfBirth, firstContractDate, cltvPercentile, propensityToUpgradePolicy, preferredChannel)
    VALUES (398765, 'Zoe', 'Duran', '2001-10-31', '2024-01-15', 44, 0.19, 'email');

-- insurance policies attached to client
INSERT INTO insurancePolicy(id, policyType, subType, effectiveDate, expirationDate, client_id)
    VALUES (375623, 'Auto', 'AutoThirdParty', '2023-06-06', '2024-06-06', 398765);

ALTER SEQUENCE client_seq RESTART WITH 398766;
ALTER SEQUENCE insurancePolicy_seq RESTART WITH 375624;


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
    VALUES (1, 'CarAccident', 12000, 1500, 149231, 1);


INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (101, 'Fire', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (102, 'Wind', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (103, 'Hail', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (104, 'Lightning', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (105, 'WaterDamage', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (106, 'OtherDamage', 100000, 3000, 250304, 101);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (107, 'WaterDamage', 100000, 3000, 250304, 102);
INSERT INTO subscribedCoverage(id, code, protectionAmount, deductible, policy_id, insurableObject_id)
    VALUES (108, 'Fire', 100000, 3000, 250304, 103);
ALTER SEQUENCE subscribedCoverage_seq RESTART WITH 9;

------------------------------------------
-- WHAT HAS BEEN CLAIMED
------------------------------------------

-- claims attached to policy
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (149230, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 149231);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (250303, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 250304);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (375622, 'PAID', '2022-10-12', 21, 375623);
INSERT INTO claim(id, status, creationDate, targetDurationInDays, policy_id)
    VALUES (375624, 'IN_PROCESS_VERIFIED', '2024-02-22', 21, 375623);
--ALTER SEQUENCE claim_seq RESTART WITH 5;

-- damages attached to claims
INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (1, '2024-04-19', 'CarAccident', true, 1000.0, 'car accident description', 149230, 1);

INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (101, '2024-04-19', 'WaterDamage', true, 1000.0, 'Wooden flooring in living room has been damaged by water', 250303, 101);
INSERT INTO damage(id, date, type, isRepairable, lossValue, description, claim_id, insurableObject_id)
    VALUES (102, '2024-04-19', 'WaterDamage', true, 300.0, 'A carpet is damaged by water', 250303, 101);
--ALTER SEQUENCE damage_seq RESTART WITH 3;

-- claim settlement offers attached to a claim
INSERT INTO claimSettlementOffer(id, claim_id, creationDate, cancelContractAtExpiration, cancelContractObjectCeased, clientResponsibleForDamage)
    VALUES(1, 149230, '2024-04-26', false, false, true);
INSERT INTO claimSettlementOffer(id, claim_id, creationDate, cancelContractAtExpiration, cancelContractObjectCeased, clientResponsibleForDamage)
    VALUES(2, 250303, '2024-04-26', false, false, false);
--ALTER SEQUENCE claimSettlementOffer_seq RESTART WITH 2;

-- actual coverages attached to a claim settlement offer
INSERT INTO actualCoverage(id, settlementOffer_id, subscribedCoverage_id, applies, description, reimbursementFactor, deductible)
    VALUES(1, 2, 101, true, 'WaterDamage due to a broken pipe - coverage applies to buildings', 0.80, 1000.0);
INSERT INTO actualCoverage(id, settlementOffer_id, subscribedCoverage_id, applies, description, reimbursementFactor, deductible)
    VALUES(2, 2, 102, false, 'WaterDamage coverage does not apply to the content of the building', 0.0, 0.0);
ALTER SEQUENCE actualCoverage_seq RESTART WITH 3;
