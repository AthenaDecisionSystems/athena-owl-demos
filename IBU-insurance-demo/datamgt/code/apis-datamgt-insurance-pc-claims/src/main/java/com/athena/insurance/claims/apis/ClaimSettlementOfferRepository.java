package com.athena.insurance.claims.apis;

import com.athena.insurance.claims.datamodel.ClaimSettlementOffer;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class ClaimSettlementOfferRepository implements PanacheRepository<ClaimSettlementOffer> {}