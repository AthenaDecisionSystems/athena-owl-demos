package com.athena.insurance.nba;

/*
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlAccessType;

@XmlType(name="Action", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD)
@XmlSeeAlso({CommercialEffort.class,CommunicateWithClient.class,PrepareProposal.class,ResendTo.class,UpsellProposal.class}) */

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;


/*
 * Note that there might be an issue with polymorphic types.
 * See https://www.ibm.com/docs/en/odm/8.12.0?topic=remediation-polymorphic-deserialization-jackson-databind-in-xom
 * We are only using this as a response type anyway.
 */
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "typeDisc__")
@JsonSubTypes({
		@JsonSubTypes.Type(value = CommunicateWithClient.class, name = "CommunicateWithClient"),
		@JsonSubTypes.Type(value = DiscountOnNextRenewal.class, name = "DiscountOnNextRenewal"),
		@JsonSubTypes.Type(value = Reassign.class, name = "Reassign"),
		@JsonSubTypes.Type(value = ReassignWithCallback.class, name = "ReassignWithCallback"),
		@JsonSubTypes.Type(value = SimpleUpsellProposal.class, name = "SimpleUpsellProposal"),
		@JsonSubTypes.Type(value = Voucher.class, name = "Voucher"),
		@JsonSubTypes.Type(value = Discount.class, name = "Discount"),
		@JsonSubTypes.Type(value = TaskSequence.class, name = "TaskSequence")
})
public abstract class Action {
	protected Action() {}

	String explanationCode;

	public String getExplanationCode() {
		return explanationCode;
	}

	public void setExplanationCode(String explanationCode) {
		this.explanationCode = explanationCode;
	}
}
