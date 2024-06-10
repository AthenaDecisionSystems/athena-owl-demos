package com.athena.insurance.nba;

import com.athena.insurance.claims.datamodel.enums.ChannelType;

/*
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;

@XmlType(name="CommunicateWithClient", namespace="http://www.athenadecisions.com/insurance-demo/1.0")
@XmlAccessorType(XmlAccessType.FIELD)*/
public class CommunicateWithClient extends Action {
	public CommunicateWithClient() {}
	ChannelType channel;
	public ChannelType getChannel() {
		return channel;
	}
	public void setChannel(ChannelType channel) {
		this.channel = channel;
	}
	public MessageType getMessageType() {
		return messageType;
	}
	public void setMessageType(MessageType messageType) {
		this.messageType = messageType;
	}

	MessageType messageType;
}
