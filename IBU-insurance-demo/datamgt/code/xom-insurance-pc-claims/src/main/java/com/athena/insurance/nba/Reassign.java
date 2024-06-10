package com.athena.insurance.nba;

import java.util.Date;

/*
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;

@XmlType(name="ResendTo", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD)*/
public class Reassign extends Assign {
	public Reassign() {}
	public Reassign(RecipientType recipient) {
		this.recipient = recipient;
	}
	public Reassign(RecipientType recipient, String suggestion) {
		this.recipient = recipient;
		this.suggestion = suggestion;
	}

	public RecipientType getRecipient() {
		return recipient;
	}
	public void setRecipient(RecipientType recipient) {
		this.recipient = recipient;
	}

	public String getSuggestion() {
		return suggestion;
	}
	public void setSuggestion(String suggestion) {
		this.suggestion = suggestion;
	}

	RecipientType recipient;
	String suggestion;
}
