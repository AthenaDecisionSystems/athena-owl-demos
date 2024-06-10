package com.athena.insurance.claims.datamodel.complaints;

import com.athena.insurance.claims.datamodel.Claim;

import java.beans.Transient;
import java.util.List;

public class ComplaintOnClaim {

    private Claim claim;
    private List<ClientInteraction> interactions;

    public ComplaintOnClaim() {}
    public ComplaintOnClaim(Claim claim, List<ClientInteraction> interactions) {
        this.claim = claim;
        this.interactions = interactions;
    }


    public Claim getClaim() {
        return claim;
    }

    public void setClaim(Claim claim) {
        this.claim = claim;
    }


    @Transient
    public ClientInteraction getLastInteraction() { return this.interactions.get(0); }

    public List<ClientInteraction> getInteractions() {
        return interactions;
    }

    public void setInteractions(List<ClientInteraction> interactions) {
        this.interactions = interactions;
    }
}
