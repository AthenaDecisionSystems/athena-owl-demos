package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.complaints.ClientInteraction;
import com.athena.insurance.claims.datamodel.complaints.ComplaintOnClaim;
import com.athena.insurance.claims.datamodel.complaints.MotiveType;
import com.athena.insurance.claims.datamodel.enums.*;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ClaimTest {

    @Test
    void testCreateClaim() {
        Calendar dateOfBirth_cal = new GregorianCalendar(2003,10,31);
        Calendar firstContractDate_cal = new GregorianCalendar(2023,11,10);

        Client client = new Client("Joe", "Smith", dateOfBirth_cal.getTime(), firstContractDate_cal.getTime(), 60, 450.0, ChannelType.email);

        InsurableObject house = new InsurableObject(InsurableObjectType.MainResidencialBuilding, "House", 1000000);
        InsurableObject land = new InsurableObject(InsurableObjectType.Land, "Land", 200000);
        InsurableObject cabin = new InsurableObject(InsurableObjectType.AuxiliaryNonResidencialBuilding, "Wooden cabin", 30000);

        SubscribedCoverage houseCov1 = new SubscribedCoverage(house, DamageType.Fire, 100000, 1000);
        SubscribedCoverage houseCov2 = new SubscribedCoverage(house, DamageType.Wind, 100000, 1000);
        SubscribedCoverage houseCov3 = new SubscribedCoverage(house, DamageType.Hail, 100000, 1000);
        SubscribedCoverage houseCov4 = new SubscribedCoverage(house, DamageType.Lightning, 100000, 1000);
        SubscribedCoverage houseCov5 = new SubscribedCoverage(house, DamageType.WaterDamage, 100000, 4000);
        SubscribedCoverage houseCov6 = new SubscribedCoverage(house, DamageType.OtherDamage, 100000, 2000);
        SubscribedCoverage landCov = new SubscribedCoverage(land, DamageType.WaterDamage, 100000, 1000);
        SubscribedCoverage cabinCov = new SubscribedCoverage(cabin, DamageType.Fire, 10000, 1000);

        Calendar effective_cal = new GregorianCalendar(2023,10,31);
        Calendar expiration_cal = new GregorianCalendar(2024,10,31);
        List<OptionType> options = new ArrayList<>();
        InsurancePolicy policy = new InsurancePolicy(PolicyType.Home, PolicySubType.HomeBuildingsAndContent, effective_cal.getTime(), expiration_cal.getTime(), client, options);

        Set<SubscribedCoverage> subscribedCoverages = new HashSet<>(Arrays.asList(houseCov1, houseCov2, houseCov3, houseCov4, houseCov5, houseCov6, landCov, cabinCov));
        policy.setCoverages(subscribedCoverages);

        Calendar claim_cal = new GregorianCalendar(2024,3,23);
        Claim claim = new Claim(ClaimStatusType.OFFER_SENT, claim_cal.getTime(), 3, policy);
        Calendar damage_cal = new GregorianCalendar(2024,3,21);

        // Damage(InsurableObject insurableObject, DamageType type, boolean isRepairable, double lossValue, String description, Date date)
        Damage houseDamage = new Damage(house, DamageType.WaterDamage, true, 4000, "", damage_cal.getTime());
        Damage landDamage = new Damage(land, DamageType.WaterDamage, true, 3000, "", damage_cal.getTime());
        Damage cabinDamage = new Damage(cabin, DamageType.WaterDamage, true, 3300, "", damage_cal.getTime());
        Set<Damage> damages = new HashSet<>(Arrays.asList(houseDamage, landDamage, cabinDamage));
        claim.setDamages(damages);

        Calendar settlement_cal = new GregorianCalendar(2024,4,2);
        ClaimSettlementOffer settlementOffer = new ClaimSettlementOffer(settlement_cal.getTime(), false, false);

        // SubscribedCoverage subscribedCoverage, boolean applies, String description, double reimbursementFactor, double deductible
        ActualCoverage houseActCov1 = new ActualCoverage(houseCov1, false, "", 100000, 1000);
        ActualCoverage houseActCov2 = new ActualCoverage(houseCov2, false, "", 100000, 1000);
        ActualCoverage houseActCov3 = new ActualCoverage(houseCov3, false, "", 100000, 1000);
        ActualCoverage houseActCov4 = new ActualCoverage(houseCov4, false, "", 100000, 1000);
        ActualCoverage houseActCov5 = new ActualCoverage(houseCov5, true, "water damage covered by policy", 100000, 4000);
        ActualCoverage houseActCov6 = new ActualCoverage(houseCov6, false, "", 100000, 2000);
        ActualCoverage landActCov = new ActualCoverage(landCov, false, "not applicable as per clause 14.7 of contract", 100000, 1000);
        ActualCoverage cabinActCov = new ActualCoverage(cabinCov, true, "water damage covered by policy", 10000, 1000);

        Set<ActualCoverage> actualCoverages = new HashSet<>(Arrays.asList(houseActCov1, houseActCov2, houseActCov3, houseActCov4, houseActCov5, houseActCov6, landActCov, cabinActCov));
        settlementOffer.setActualCoverages(actualCoverages);
        settlementOffer.setClientResponsibleForDamage(false);
        claim.setSettlementOffer(settlementOffer);

        assertEquals(ClaimStatusType.OFFER_SENT, claim.getStatus());
        assertEquals("Joe", claim.getPolicy().getClient().getFirstName());

        assertEquals(8, claim.getPolicy().getCoverages().size());
        assertEquals(3, claim.getDamages().size());

        ComplaintOnClaim complaint = new ComplaintOnClaim();
        complaint.setClaim(claim);

        Calendar interaction_cal = new GregorianCalendar(2024,4,12);
        ClientInteraction interaction = new ClientInteraction(interaction_cal.getTime());
        interaction.setMotive(MotiveType.UnsatisfiedWithAppliedCoverages);
        interaction.setIntentionToLeave(true);
        interaction.setCompetitorName("OtherInsurer");
        interaction.setCompetitorPolicyName("HousePlus");
        interaction.setCompetitorPrice(500000.0);
        List<ClientInteraction> interactions = new ArrayList<>(Arrays.asList(interaction));
        complaint.setInteractions(interactions);
    }
}
