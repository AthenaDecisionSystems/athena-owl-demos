package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.DamageType;
import jakarta.persistence.*;

import java.util.Date;

@Entity
@Cacheable
public class Damage {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne
    @JoinColumn(name="claim_id", nullable=false)
    private Claim claim;

    @ManyToOne
    @JoinColumn(name = "insurableObject_id")
    private InsurableObject insurableObject;

    @Enumerated(EnumType.STRING)
    private DamageType type;

    private boolean isRepairable;
    private double lossValue;
    private String description;

    private Date date;

    public Damage() {}
    public Damage(InsurableObject insurableObject, DamageType type, boolean isRepairable, double lossValue, String description, Date date) {
        this.insurableObject = insurableObject;
        this.type = type;
        
        this.isRepairable = isRepairable;
        this.lossValue = lossValue;
        this.description = description;

        this.date = date;
    }

    public InsurableObject getInsurableObject() {
        return insurableObject;
    }

    public void setInsurableObject(InsurableObject insurableObject) {
        this.insurableObject = insurableObject;
    }

    public DamageType getType() {
        return type;
    }

    public void setType(DamageType type) {
        this.type = type;
    }

    public double getLossValue() { return this.lossValue; }
    public void setLossValue(double lossValue) { this.lossValue = lossValue;}
    
    public boolean isRepairable() { return this.isRepairable; }
    public void setRepairable(boolean isRepairable) { this.isRepairable = isRepairable; }

    public String getDescription() { return this.description; }
    public void setDescription(String description) { this.description = description; }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }
}
