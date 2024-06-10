package com.athena.insurance.nba;

import java.util.Date;

/*
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;

@XmlType(name="ResendTo", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD)*/

/*
 * Business scenario - what is told to the client:
 * The claims department will call you back in the coming 7 days.
 * In case they do not contact you, please call me back on 3453453453 for a follow up of your case.
 */
public class ReassignWithCallback extends Assign {
	public ReassignWithCallback() {}
	public ReassignWithCallback(int numDays, RecipientType recipient) {
		this.callBackDeadline = numDays;
		this.recipient = recipient;
	}
	public ReassignWithCallback(int numDays, RecipientType recipient, String suggestion) {
		this.callBackDeadline = numDays;
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

	public int getCallBackDeadline() {
		return callBackDeadline;
	}
	public void setCallBackDeadline(int callBackDeadline) {
		this.callBackDeadline = callBackDeadline;
	}

	RecipientType recipient;
	String suggestion;
	int callBackDeadline;
}
