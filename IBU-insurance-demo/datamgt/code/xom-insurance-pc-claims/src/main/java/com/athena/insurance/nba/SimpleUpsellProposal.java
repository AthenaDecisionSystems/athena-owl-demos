package com.athena.insurance.nba;

import java.util.List;

/*
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;

@XmlType(name="UpsellProposal", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD)*/
public class SimpleUpsellProposal extends Action {

	public SimpleUpsellProposal() {}

	protected String description;

	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
}