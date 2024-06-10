package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.InsurableObjectType;
import jakarta.persistence.*;

import java.util.Set;

@Entity
@Cacheable
public class InsurableObject {

    @Id
    @GeneratedValue
    private Long id;

    @OneToMany(mappedBy="insurableObject")
    private Set<SubscribedCoverage> coverages; // an insurable object is referenced by many subscribed coverages

    @Enumerated(EnumType.STRING)
    private InsurableObjectType type;
    private String description;
    private double estimatedValue;

    public InsurableObject() {}
    public InsurableObject(InsurableObjectType type, String description, double estimatedValue) {
        this.type = type;
        this.description = description;
        this.estimatedValue = estimatedValue;
    }

    public InsurableObjectType getType() {
        return type;
    }

    public void setType(InsurableObjectType type) {
        this.type = type;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public double getEstimatedValue() {
        return estimatedValue;
    }

    public void setEstimatedValue(double estimatedValue) {
        this.estimatedValue = estimatedValue;
    }
}
