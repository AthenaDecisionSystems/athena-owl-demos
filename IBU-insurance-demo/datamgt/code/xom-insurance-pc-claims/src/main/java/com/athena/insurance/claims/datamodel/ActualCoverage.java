package com.athena.insurance.claims.datamodel;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;

@Entity
@Cacheable
public class ActualCoverage {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne
    @JoinColumn(name="settlementOffer_id", nullable=false)
    @JsonBackReference  // do not serialize to avoid infinite recursion
    private ClaimSettlementOffer settlementOffer;  // an actual coverage always refer to a unique claim settlement offer

    @ManyToOne
    @JoinColumn(name="subscribedCoverage_id", nullable=false)
    private SubscribedCoverage subscribedCoverage;

    private boolean applies;
    private String description;
    private double reimbursementFactor;
    private double deductible;

    public ActualCoverage() {}
    public ActualCoverage(SubscribedCoverage subscribedCoverage, boolean applies, String description, double reimbursementFactor, double deductible) {
        this.subscribedCoverage = subscribedCoverage;
        this.applies = applies;
        this.description = description;
        this.reimbursementFactor = reimbursementFactor;
        this.deductible = deductible;
    }

    public ClaimSettlementOffer getSettlementOffer() {
        return settlementOffer;
    }

    public void setSettlementOffer(ClaimSettlementOffer settlementOffer) {
        this.settlementOffer = settlementOffer;
    }

    public SubscribedCoverage getSubscribedCoverage() {
        return subscribedCoverage;
    }

    public void setSubscribedCoverage(SubscribedCoverage subscribedCoverage) {
        this.subscribedCoverage = subscribedCoverage;
    }

    public boolean isApplies() {
        return applies;
    }

    public void setApplies(boolean applies) {
        this.applies = applies;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public double getReimbursementFactor() {
        return reimbursementFactor;
    }

    public void setReimbursementFactor(double reimbursementFactor) {
        this.reimbursementFactor = reimbursementFactor;
    }

    public double getDeductible() {
        return deductible;
    }

    public void setDeductible(double deductible) {
        this.deductible = deductible;
    }
}
