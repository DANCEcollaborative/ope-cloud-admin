# Base bare openjdk image
FROM openjdk:8-jre-slim

# Enable/disable AGS v2
ENV AGS_V2_ENABLED true

################################################################################
# Add external datasets / configuration / etc...that are required by your grader
################################################################################

# For example, some projects have secret datasets that are not included in the grader executable
# ADD dataset/data/secret /grader/secret

# Add the grader executable to the docker image.
ADD target/sail_grader.jar /grader/sail_grader.jar

RUN sh -c 'touch /grader/sail_grader.jar'

# The grader exists in the "/grader" directory, however all submission files including student tar file exist in submission directory
WORKDIR /submission

# The main grading command
ENTRYPOINT ["java", "-XX:-OmitStackTraceInFastThrow", "-ea", "-Dfile.encoding=UTF-8", "-jar", "/grader/sail_grader.jar"]
