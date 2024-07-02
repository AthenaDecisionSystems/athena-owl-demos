# org.kie.kogito.kogito-quarkus-archetype - 1.10.0.Final #

# Running

- Compile and Run

    ```
     mvn clean package quarkus:dev
    ```

- Native Image (requires JAVA_HOME to point to a valid GraalVM)

    ```
    mvn clean package -Pnative
    ```
  
  native executable (and runnable jar) generated in `target/`

# Test your application


# TBD



# Developing

Add your business assets resources (process definition, rules, decisions) into src/main/resources.

Add your java classes (data model, utilities, services) into src/main/java.

Then just build the project and run.


# OpenAPI (Swagger) documentation
[Specification at swagger.io](https://swagger.io/docs/specification/about/)

The exposed service [OpenAPI specification](https://swagger.io/docs/specification) is generated at 
[/q/openapi](http://localhost:8080/q/openapi).

You can visualize and interact with the generated specification using the embbeded [Swagger UI](http://localhost:8080/q/swagger-ui) or importing the generated specification file on [Swagger Editor](https://editor.swagger.io).

In addition client application can be easily generated from the swagger definition to interact with this service.
