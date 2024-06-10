package com.athena.insurance.claims.datamodel;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;

import java.util.Date;
import java.util.Set;

@Entity
@Cacheable
public class ClaimSettlementOffer {

    @Id
    @GeneratedValue
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "claim_id")
    @JsonBackReference  // do not serialize to avoid infinite recursion
    private Claim claim;

    @Basic
    private Date creationDate;

    @Basic
    private boolean cancelContractAtExpiration;

    @Basic
    private boolean cancelContractObjectCeased;

    @Basic
    private boolean clientResponsibleForDamage;

    @OneToMany(mappedBy="settlementOffer")
    @JsonManagedReference
    private Set<ActualCoverage> actualCoverages;

    public ClaimSettlementOffer() {}
    public ClaimSettlementOffer(Date creationDate, boolean cancelContractAtExpiration, boolean cancelContractObjectCeased) {
        this.creationDate = creationDate;
        this.cancelContractAtExpiration = cancelContractAtExpiration;
        this.cancelContractObjectCeased = cancelContractObjectCeased;
    }

    public Claim getClaim() {
        return claim;
    }

    public void setClaim(Claim claim) {
        this.claim = claim;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public boolean isCancelContractAtExpiration() {
        return cancelContractAtExpiration;
    }

    public void setCancelContractAtExpiration(boolean cancelContractAtExpiration) {
        this.cancelContractAtExpiration = cancelContractAtExpiration;
    }

    public boolean isCancelContractObjectCeased() {
        return cancelContractObjectCeased;
    }

    public void setCancelContractObjectCeased(boolean cancelContractObjectCeased) {
        this.cancelContractObjectCeased = cancelContractObjectCeased;
    }

    public boolean isClientResponsibleForDamage() {
        return clientResponsibleForDamage;
    }

    public void setClientResponsibleForDamage(boolean clientResponsibleForDamage) {
        this.clientResponsibleForDamage = clientResponsibleForDamage;
    }

    public Set<ActualCoverage> getActualCoverages() {
        return actualCoverages;
    }

    public void setActualCoverages(Set<ActualCoverage> actualCoverages) {
        this.actualCoverages = actualCoverages;
    }

    @JsonIgnore
    public double getDeductibleTotal() {
        return this.actualCoverages.stream()
                .mapToDouble(c -> c.getDeductible())
                .sum();
    }
}
