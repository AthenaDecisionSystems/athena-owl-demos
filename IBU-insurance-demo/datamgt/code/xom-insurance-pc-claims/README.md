# Java object model to be used by ODM and Quarkus API project

- package to build the jar
- install will copy it into local Maven repository
> ./mvnw clean compile package

Note that the jar is copied as an unmanaged jar to the ODM project and the Quarkus API project.
- under workspace/xom-insurance-pc-claims-lib/lib in ODM
- under api-datamgt-insurance-pc-claims/unmanaged-jars

Possible improvement: If we publish the jar using `./mnvw install`, then the Quarkus API project could include it as a managed dependency in its pom file.