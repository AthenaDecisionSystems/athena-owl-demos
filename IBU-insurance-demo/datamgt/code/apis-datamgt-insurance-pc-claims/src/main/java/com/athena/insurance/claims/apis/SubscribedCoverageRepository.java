package com.athena.insurance.claims.apis;

import com.athena.insurance.claims.datamodel.SubscribedCoverage;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class SubscribedCoverageRepository implements PanacheRepository<SubscribedCoverage> {}