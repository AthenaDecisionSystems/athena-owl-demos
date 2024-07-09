package com.athena.insurance.claims.apis;

import java.util.Map;
import java.util.HashMap;
import com.athena.insurance.claims.datamodel.Client;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class ClientRepository implements PanacheRepository<Client> {

    public Client findByName(String name){
        return find("lastName", name).firstResult();
    }

    public Client findByFullName(String firstName, String name){
        Map<String, Object> params = new HashMap<>();
        params.put("name", name);
        params.put("firstName", firstName);
        return find("lastName = :name and firstName = :firstName", params).firstResult();
    }
}
