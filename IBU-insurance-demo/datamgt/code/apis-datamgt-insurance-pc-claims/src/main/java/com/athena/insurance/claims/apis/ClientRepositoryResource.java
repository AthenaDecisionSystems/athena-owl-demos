package com.athena.insurance.claims.apis;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.quarkus.panache.common.Sort;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.ExceptionMapper;
import jakarta.ws.rs.ext.Provider;
import org.jboss.logging.Logger;

import com.athena.insurance.claims.datamodel.Client;
import java.util.List;

@Path("repository/clients")
@ApplicationScoped
@Produces("application/json")
@Consumes("application/json")
public class ClientRepositoryResource {

    @Inject
    ClientRepository clientRepository;

    private static final Logger LOGGER = Logger.getLogger(ClientRepositoryResource.class.getName());

    @GET
    public List<Client> get() {
        return clientRepository.listAll(Sort.by("lastName"));
    }

    @GET
    @Path("{id}")
    public Client getSingle(@PathParam("id") Long id) {
        Client entity = clientRepository.findById(id);
        if (entity == null) {
            throw new WebApplicationException("Client with id of " + id + " does not exist.", 404);
        }
        return entity;
    }

    @GET
    @Path("/search/{name}")
    public Client searchByName(@PathParam("name") String name) {
        Client entity = clientRepository.findByName(name);
        if (entity == null) {
            throw new WebApplicationException("Client with name of " + name + " does not exist.", 404);
        }
        return entity;
    }

    @POST
    @Transactional
    public Response create(Client client) {
        if (client.getId() != null) {
            throw new WebApplicationException("Id should not be set on request.", 422);
        }

        clientRepository.persist(client);
        return Response.ok(client).status(201).build();
    }

    @PUT
    @Path("{id}")
    @Transactional
    public Client update(@PathParam("id") Long id, Client client) {
        if (client.getFirstName() == null) {
            throw new WebApplicationException("Client Name was not set on request.", 422);
        }

        Client entityToUpdate = clientRepository.findById(id);

        if (entityToUpdate == null) {
            throw new WebApplicationException("Client with id of " + id + " does not exist.", 404);
        }

        entityToUpdate.setFirstName(client.getFirstName());
        entityToUpdate.setLastName(client.getLastName());
        entityToUpdate.setDateOfBirth(client.getDateOfBirth());
        entityToUpdate.setCltvPercentile(client.getCltvPercentile());
        entityToUpdate.setPropensityToUpgradePolicy(client.getPropensityToUpgradePolicy());
        return entityToUpdate;
    }

    @DELETE
    @Path("{id}")
    @Transactional
    public Response delete(@PathParam("id") Long id) {
        Client entity = clientRepository.findById(id);
        if (entity == null) {
            throw new WebApplicationException("Client with id of " + id + " does not exist.", 404);
        }
        clientRepository.delete(entity);
        return Response.status(204).build();
    }

    @Provider
    public static class ErrorMapper implements ExceptionMapper<Exception> {

        @Inject
        ObjectMapper objectMapper;

        @Override
        public Response toResponse(Exception exception) {
            LOGGER.error("Failed to handle request", exception);

            int code = 500;
            if (exception instanceof WebApplicationException) {
                code = ((WebApplicationException) exception).getResponse().getStatus();
            }

            ObjectNode exceptionJson = objectMapper.createObjectNode();
            exceptionJson.put("exceptionType", exception.getClass().getName());
            exceptionJson.put("code", code);

            if (exception.getMessage() != null) {
                exceptionJson.put("error", exception.getMessage());
            }

            return Response.status(code)
                    .entity(exceptionJson)
                    .build();
        }
    }
}