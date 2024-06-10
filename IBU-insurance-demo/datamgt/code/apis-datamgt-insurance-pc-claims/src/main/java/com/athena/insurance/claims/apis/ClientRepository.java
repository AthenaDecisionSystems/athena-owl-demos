package com.athena.insurance.claims.apis;

import com.athena.insurance.claims.datamodel.Client;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class ClientRepository implements PanacheRepository<Client> {

    public Client findByName(String name){
        return find("lastName", name).firstResult();
    }
}