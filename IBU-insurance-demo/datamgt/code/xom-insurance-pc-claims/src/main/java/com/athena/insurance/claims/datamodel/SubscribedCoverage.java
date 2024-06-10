package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.DamageType;
import jakarta.persistence.*;

@Entity
@Cacheable
public class SubscribedCoverage {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne
    @JoinColumn(name="policy_id", nullable=false)
    private InsurancePolicy policy;

    @ManyToOne
    @JoinColumn(name="insurableObject_id", nullable=false)
    private InsurableObject insurableObject;

    @Enumerated(EnumType.STRING)
    private DamageType code;
    private double protectionAmount;
    private double deductible;

    public SubscribedCoverage() {}
    public SubscribedCoverage(InsurableObject insurableObject, DamageType code, double protectionAmount, double deductible) {
        this.insurableObject = insurableObject;
        this.code = code;
        this.protectionAmount = protectionAmount;
        this.deductible = deductible;
    }

    public InsurableObject getInsurableObject() {
        return insurableObject;
    }

    public void setInsurableObject(InsurableObject insurableObject) {
        this.insurableObject = insurableObject;
    }

    public DamageType getCode() {
        return code;
    }

    public void setCode(DamageType code) {
        this.code = code;
    }

    public double getProtectionAmount() {
        return protectionAmount;
    }

    public void setProtectionAmount(double protectionAmount) {
        this.protectionAmount = protectionAmount;
    }

    public double getDeductible() {
        return deductible;
    }

    public void setDeductible(double deductible) {
        this.deductible = deductible;
    }
}
