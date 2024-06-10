package com.athena.insurance.nba;

/*
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;

@XmlType(name="CommercialEffort", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD) */
public class Voucher extends Action {
	
	String description;

	public Voucher() {}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}
}
