package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.PolicySubType;
import com.athena.insurance.claims.datamodel.enums.PolicyType;
import jakarta.persistence.*;

import java.util.Date;
import java.util.List;
import java.util.Set;

@Entity
@Cacheable
public class InsurancePolicy {

    @Id
    @GeneratedValue
    private Long id;

    @Basic
    private Date effectiveDate;

    @Basic
    private Date expirationDate;

    @Enumerated(EnumType.STRING)
    private PolicyType policyType;

    @Enumerated(EnumType.STRING)
    private PolicySubType subType;


    @ManyToOne
    @JoinColumn(name="client_id", nullable=false)
    private Client client;

    @OneToMany(mappedBy="policy")
    private Set<Claim> claims;

    @OneToMany(mappedBy="policy")
    private Set<SubscribedCoverage> coverages;

    @Column
    @Enumerated
    @ElementCollection(targetClass = OptionType.class)
    private List<OptionType> options;

    public InsurancePolicy() {}
    public InsurancePolicy(PolicyType policyType, PolicySubType subType,Date effectiveDate, Date expirationDate, Client client, List<OptionType> options) {
        this.policyType = policyType;
        this.subType = subType;
        this.effectiveDate = effectiveDate;
        this.expirationDate = expirationDate;
        this.client = client;
        this.options = options;
    }


    public Long getId() {
        return id;
    }

    public Date getEffectiveDate() {
        return effectiveDate;
    }

    public void setEffectiveDate(Date effectiveDate) {
        this.effectiveDate = effectiveDate;
    }

    public Date getExpirationDate() {
        return expirationDate;
    }

    public void setExpirationDate(Date expirationDate) {
        this.expirationDate = expirationDate;
    }

    public PolicyType getPolicyType() {
        return policyType;
    }

    public void setPolicyType(PolicyType policyType) {
        this.policyType = policyType;
    }

    public PolicySubType getSubType() {
        return subType;
    }

    public void setSubType(PolicySubType subType) {
        this.subType = subType;
    }

    public Client getClient() {
        return client;
    }

    public void setClient(Client client) {
        this.client = client;
    }

    public Set<SubscribedCoverage> getCoverages() {
        return coverages;
    }

    public void setCoverages(Set<SubscribedCoverage> coverages) {
        this.coverages = coverages;
    }

    public List<OptionType> getOptions() {
        return options;
    }

    public void setOptions(List<OptionType> options) {
        this.options = options;
    }
}
