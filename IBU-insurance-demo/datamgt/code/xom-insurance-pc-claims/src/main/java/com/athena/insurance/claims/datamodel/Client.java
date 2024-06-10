package com.athena.insurance.claims.datamodel;

import com.athena.insurance.claims.datamodel.enums.ChannelType;
import jakarta.persistence.*;

import java.util.Date;
import java.util.Set;

@Entity
@Cacheable
public class Client {

    @Id @GeneratedValue private Long id;

    @Column(length = 40, unique = true)
    private String firstName;

    @Column(length = 40, unique = true)
    private String lastName;

    @Basic private Date dateOfBirth;

    // Used to compute length of time as customer
    @Basic private Date firstContractDate;

    // Customer Lifetime Value Percentile, i.e. between 0 and 100
    @Basic private int cltvPercentile;

    @Basic private double propensityToUpgradePolicy;

    // a client has many policies
    @OneToMany(mappedBy="client")
    private Set<InsurancePolicy> policies;

    @Enumerated(EnumType.STRING)
    private ChannelType preferredChannel;

    public Client() {}

    public Client(String firstName,
                  String lastName,
                  Date dateOfBirth,
                  Date firstContractDate,
                  int cltvPercentile,
                  double disposableIncome,
                  ChannelType preferredChannel) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.dateOfBirth = dateOfBirth;
        this.firstContractDate =firstContractDate;
        this.cltvPercentile = cltvPercentile;
        this.propensityToUpgradePolicy = disposableIncome;
        this.preferredChannel = preferredChannel;
    }

    public Long getId() {
        return id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Date getDateOfBirth() {
        return dateOfBirth;
    }
    public void setDateOfBirth(Date dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public Date getFirstContractDate() {
        return firstContractDate;
    }

    public void setFirstContractDate(Date firstContractDate) {
        this.firstContractDate = firstContractDate;
    }

    public ChannelType getPreferredChannel() {
        return preferredChannel;
    }

    public void setPreferredChannel(ChannelType preferredChannel) {
        this.preferredChannel = preferredChannel;
    }

    public int getCltvPercentile() {
        return cltvPercentile;
    }

    public void setCltvPercentile(int cltvPercentile) {
        this.cltvPercentile = cltvPercentile;
    }

    public double getPropensityToUpgradePolicy() {
        return propensityToUpgradePolicy;
    }

    public void setPropensityToUpgradePolicy(double propensityToUpgradePolicy) {
        this.propensityToUpgradePolicy = propensityToUpgradePolicy;
    }
}
