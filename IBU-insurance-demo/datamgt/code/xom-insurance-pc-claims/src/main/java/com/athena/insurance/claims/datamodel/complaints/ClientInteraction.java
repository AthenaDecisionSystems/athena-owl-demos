package com.athena.insurance.claims.datamodel.complaints;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Date;


public class ClientInteraction {

    @JsonProperty(required = true)
    private Date date;

    private MotiveType motive;
    private boolean intentionToLeave;

    // TODO: to be added once we extract it using a LLM
    // private DegreeOfInsatisfaction degreeOfInsatisfaction;

    // relevant if intentionToLeave is true
    private String competitorName;
    private String competitorPolicyName;
    private Double competitorPrice;

    // relevant if motive is UnsatisfiedWithDelay
    private Date desiredResolutionDate;
    private Date desiredReimbursementDate;

    // relevant if motive is UnsatisfiedWithReimbursedAmount
    private Double expectedAmount;
    private boolean unsatisfiedWithDeductible;

    public ClientInteraction(Date date) {
        this.date = date;
    }
    public ClientInteraction() {}

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public MotiveType getMotive() {
        return motive;
    }

    public void setMotive(MotiveType motive) {
        this.motive = motive;
    }

    public boolean isIntentionToLeave() {
        return intentionToLeave;
    }
    public boolean noIntentionToLeave() {
        return !intentionToLeave;
    }
    public void setIntentionToLeave(boolean intentionToLeave) {
        this.intentionToLeave = intentionToLeave;
    }

    public String getCompetitorName() {
        return competitorName;
    }

    public void setCompetitorName(String competitorName) {
        this.competitorName = competitorName;
    }

    public String getCompetitorPolicyName() {
        return competitorPolicyName;
    }

    public void setCompetitorPolicyName(String competitorPolicyName) {
        this.competitorPolicyName = competitorPolicyName;
    }

    public Double getCompetitorPrice() {
        return competitorPrice;
    }

    public void setCompetitorPrice(Double competitorPrice) {
        this.competitorPrice = competitorPrice;
    }

    public Date getDesiredResolutionDate() {
        return desiredResolutionDate;
    }

    public void setDesiredResolutionDate(Date desiredResolutionDate) {
        this.desiredResolutionDate = desiredResolutionDate;
    }

    public Date getDesiredReimbursementDate() {
        return desiredReimbursementDate;
    }

    public void setDesiredReimbursementDate(Date desiredReimbursementDate) {
        this.desiredReimbursementDate = desiredReimbursementDate;
    }

    public Double getExpectedAmount() {
        return expectedAmount;
    }

    public void setExpectedAmount(Double expectedAmount) {
        this.expectedAmount = expectedAmount;
    }

    public boolean isUnsatisfiedWithDeductible() {
        return unsatisfiedWithDeductible;
    }

    public void setUnsatisfiedWithDeductible(boolean unsatisfiedWithDeductible) {
        this.unsatisfiedWithDeductible = unsatisfiedWithDeductible;
    }
}