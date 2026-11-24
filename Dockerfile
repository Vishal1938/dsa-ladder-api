FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY pom.xml .
RUN mvn -q dependency:go-offline
COPY src src
COPY problems problems
RUN mvn -q -DskipTests package

# Runtime needs a full JDK: the judge compiles submissions with javac.
FROM eclipse-temurin:21-jdk
RUN apt-get update && apt-get install -y --no-install-recommends util-linux && rm -rf /var/lib/apt/lists/* \
 && useradd --system --create-home --uid 10001 judge
WORKDIR /app
COPY --from=build /src/target/dsa-ladder-backend-*.jar app.jar
COPY problems problems
USER judge
ENV SPRING_PROFILES_ACTIVE=prod PROBLEMS_DIR=/app/problems JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=50"
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
