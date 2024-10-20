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

import com.athena.insurance.claims.datamodel.Claim;
import java.util.List;

@Path("repository/claims")
@ApplicationScoped
@Produces("application/json")
@Consumes("application/json")
public class ClaimRepositoryResource {

    @Inject
    ClaimRepository claimRepository;

    private static final Logger LOGGER = Logger.getLogger(ClaimRepositoryResource.class.getName());

    @GET
    public List<Claim> get() {
        return claimRepository.listAll(Sort.by("id"));
    }

    @GET
    @Path("{id}")
    public Claim getSingle(@PathParam("id") Long id) {
        Claim entity = claimRepository.findById(id);
        if (entity == null) {
            throw new WebApplicationException("Claim with id of " + id + " does not exist.", 404);
        }
        return entity;
    }

    @POST
    @Transactional
    public Response create(Claim claim) {
        if (claim.getId() != null) {
            throw new WebApplicationException("Id should not be set on request.", 422);
        }

        claimRepository.persist(claim);
        return Response.ok(claim).status(201).build();
    }


    @DELETE
    @Path("{id}")
    @Transactional
    public Response delete(@PathParam("id") Long id) {
        Claim entity = claimRepository.findById(id);
        if (entity == null) {
            throw new WebApplicationException("Claim with id of " + id + " does not exist.", 404);
        }
        claimRepository.delete(entity);
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