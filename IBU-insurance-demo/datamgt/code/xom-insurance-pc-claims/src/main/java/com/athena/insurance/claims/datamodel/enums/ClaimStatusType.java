package com.athena.insurance.claims.datamodel.enums;

public enum ClaimStatusType {
    RECEIVED,
    IN_PROCESS_VALIDATED,
    IN_PROCESS_ASSESSED,
    IN_PROCESS_VERIFIED,
    IN_PROCESS_LOSS_ADJUSTER_REPORTED,
    REJECTION_SENT,
    REJECTION_COMPLAINT,
    OFFER_SENT,
    OFFER_ACCEPTED,
    PAID,
    CLOSED
}
