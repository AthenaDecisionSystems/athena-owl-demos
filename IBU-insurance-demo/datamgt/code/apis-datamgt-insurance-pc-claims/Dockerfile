## Stage 1 : build with maven builder image with native capabilities
FROM quay.io/quarkus/centos-quarkus-maven:20.1.0-java11 AS build
WORKDIR /project
USER root
COPY . /project
RUN chown -R quarkus /project
USER quarkus
RUN mvn -f /project/pom.xml  clean package -DskipTests

## Stage 2 : create the docker final image

FROM registry.access.redhat.com/ubi8/openjdk-17:1.18


COPY --chown=185 --from=build /project/target/quarkus-app/lib/ /deployments/lib/
COPY --chown=185 --from=build /project/target/quarkus-app/*.jar /deployments/
COPY --chown=185 --from=build /project/target/quarkus-app/app/ /deployments/app/
COPY --chown=185 --from=build /project/target/quarkus-app/quarkus/ /deployments/quarkus/

EXPOSE 8080

USER 185
ENV JAVA_OPTS_APPEND="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
ENV JAVA_APP_JAR="/deployments/quarkus-run.jar"

ENTRYPOINT [ "/opt/jboss/container/java/run/run-java.sh" ]