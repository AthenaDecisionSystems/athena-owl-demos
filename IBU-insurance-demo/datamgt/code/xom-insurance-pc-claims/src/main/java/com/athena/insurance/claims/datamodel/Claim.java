package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.ClaimStatusType;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;

import java.util.Date;
import java.util.HashSet;
import java.util.Set;

@Entity
@Cacheable
public class Claim {

    @Id @GeneratedValue
    private Long id;

    @Enumerated(EnumType.STRING)
    private ClaimStatusType status;

    @Basic
    private Date creationDate;

    @Basic
    private int targetDurationInDays;

    /*
    * See https://www.baeldung.com/hibernate-one-to-many
    */
    @ManyToOne
    @JoinColumn(name="policy_id", nullable=false)
    private InsurancePolicy policy; // a claim always refers to a unique policy

    @OneToMany(mappedBy="claim")
    private Set<Damage> damages;

    // a claim might have zero or one settlement offer, i.e. optional
    @OneToOne(mappedBy = "claim", cascade = CascadeType.ALL, optional = true)
    @JsonManagedReference
    private ClaimSettlementOffer settlementOffer;

    public Long getId() {
        return id;
    }

    public Claim() {}
    public Claim(ClaimStatusType status, Date creationDate, int targetDurationInDays, InsurancePolicy policy) {
        this.status = status;
        this.creationDate = creationDate;
        this.targetDurationInDays = targetDurationInDays;
        this.policy = policy;

        this.damages = new HashSet<>();
    }

    public ClaimStatusType getStatus() {
        return status;
    }

    public void setStatus(ClaimStatusType status) {
        this.status = status;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public int getTargetDurationInDays() {
        return targetDurationInDays;
    }

    public void setTargetDurationInDays(int targetDurationInDays) {
        this.targetDurationInDays = targetDurationInDays;
    }

    public InsurancePolicy getPolicy() {
        return policy;
    }

    public void setPolicy(InsurancePolicy policy) {
        this.policy = policy;
    }

    public Set<Damage> getDamages() {
        return damages;
    }

    public void setDamages(Set<Damage> damages) {
        this.damages = damages;
    }

    public ClaimSettlementOffer getSettlementOffer() {
        return settlementOffer;
    }

    public void setSettlementOffer(ClaimSettlementOffer settlementOffer) {
        this.settlementOffer = settlementOffer;
    }
}
