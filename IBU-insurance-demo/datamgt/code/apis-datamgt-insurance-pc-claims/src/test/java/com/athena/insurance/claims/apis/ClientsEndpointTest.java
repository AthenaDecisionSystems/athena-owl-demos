package com.athena.insurance.claims.apis;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.core.IsNot.not;

import org.junit.jupiter.api.Test;

import io.quarkus.test.junit.QuarkusTest;

@QuarkusTest
public class ClientsEndpointTest {

    @Test
    public void testClientRepository() {
        performTest("/repository/clients");
    }

    private void performTest(String path) {
        //List all, :
        given()
                .when().get(path)
                .then()
                .statusCode(200)
                .body(
                        containsString("Dupont"),
                        containsString("Smith"),
                        containsString("Durand"));

        //Delete the first client
        given()
                .when().delete(path + "/1")
                .then()
                .statusCode(204);

        //List all, first one is missing now:
        given()
                .when().get(path)
                .then()
                .statusCode(200)
                .body(
                        not(containsString("Dupont")),
                        containsString("Smith"),
                        containsString("Durand"));
    }

}
