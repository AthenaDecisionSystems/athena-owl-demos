package com.athena.insurance.nba;

import com.athena.insurance.claims.datamodel.enums.ChannelType;

import java.util.ArrayList;
import java.util.List;

public class Response {
		
	public Response() {
		this.actions = new ArrayList<>();
		this.outputTraces = new ArrayList<>();
		this.missingInfoElements = new ArrayList<>();
	}

	public List<Action> getActions() {
		return actions;
	}

	public void setActions(List<Action> actions) {
		this.actions = actions;
	}
	
	// propose a voucher of {value} with {description}
	public void appendVoucher(String explanationCode, double value, String description) {
		Voucher voucher = new Voucher();
		voucher.setExplanationCode(explanationCode);
		voucher.setValue(value);
		voucher.setDescription(description);
		this.actions.add(voucher);
	}
	
	// communicate a {messageType} to the client via {channel}
	public void appendCommunicateWithClient(String explanationCode, ChannelType channel, MessageType messageType) {
		CommunicateWithClient cwc = new CommunicateWithClient();
		cwc.setExplanationCode(explanationCode);
		cwc.setChannel(channel);
		cwc.setMessageType(messageType);
		this.actions.add(cwc);
	}

	// resend to {recepient}
	public void appendResendTo(String explanationCode, RecipientType recipient) {
		Reassign resend = new Reassign();
		resend.setExplanationCode(explanationCode);
		resend.setRecipient(recipient);
		this.actions.add(resend);
	}

	// resend to {recepient} suggesting {suggestion}
	public void appendResendTo(String explanationCode, RecipientType recipient, String suggestion) {
		Reassign resend = new Reassign();
		resend.setExplanationCode(explanationCode);
		resend.setRecipient(recipient);
		resend.setSuggestion(suggestion);
		this.actions.add(resend);
	}

	// propose a simple upsell to include some extra options
	public void appendUpsellProposal(String explanationCode, String description) {
		SimpleUpsellProposal upsell = new SimpleUpsellProposal();
		upsell.setExplanationCode(explanationCode);
		upsell.setDescription(description);
		this.actions.add(upsell);
	}
	// propose a discount on some service
	public void appendDiscount(String explanationCode, String description, double percentage) {
		Discount d = new Discount();
		d.setExplanationCode(explanationCode);
		d.setDescription(description);
		d.setPercentage(percentage);
		this.actions.add(d);
	}

	public void appendTaskSequence(String explanationCode, TaskSequence ts) {
		ts.setExplanationCode(explanationCode);
		this.actions.add(ts);
	}

	public List<String> getOutputTraces() {
		return outputTraces;
	}

	public void setOutputTraces(List<String> outputTraces) {
		this.outputTraces = outputTraces;
	}

	public List<InfoElement> getMissingInfoElements() {
		return missingInfoElements;
	}

	public void setMissingInfoElements(List<InfoElement> missingInfoElements) {
		this.missingInfoElements = missingInfoElements;
	}

	public void addTrace(String msg) {
		this.outputTraces.add(msg);
	}
	public void addMissingInfo(String path, String questionId, String type) {
		this.missingInfoElements.add(new InfoElement(path, questionId, type));
	}
	
	protected List<Action> actions;
	protected List<InfoElement> missingInfoElements;
	protected List<String> outputTraces;
}
