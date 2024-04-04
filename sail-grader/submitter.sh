#!/bin/bash

# Exclude:
# 1. files > 5M
# 2. files under ./target/maven-status/maven-compiler-plugin/
#    which lists the path names of the java source files that contain the submissionUsername
# e.g. ./target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst:/home/<andrew_id>/Project_Database/src/main/java/edu/cmu/cs/cloud/YelpApp.java

find_files_to_submit() {
  find . -size -5M -type f ! -path "./target/maven-status/maven-compiler-plugin/*" ! -path "./target/surefire-reports/*" ! -path "*/.git/*" ! -path "*/.DS_Store" ! -path "*/._*" ! -path "*/*.tar.gz"
}

# the context per task required by AGS
# you need to update the context here per task
lmsName="sail2"
secretKey="9113513e079a4c64"
projectId="ope-author-autoscalin-fl6rpghr"
taskId="a570b0c6-a097-433f-9d07-0a66ea6676d6"
courseType="cloud-developer"
duration=300

# bump the artifact version everytime you make change to the submitter unless it is a bug fix
# wherein you want to override an existing submitter version that has bugs
artifactVersion="v1"

# the generic context required by AGS
studentDNS=$(curl --silent ipinfo.io/ip)
ags_dns="autograding.sailplatform.org"
signature="1K9SaGliHwthRgeOi12hUdCUwAPmN"

while getopts ":ha:" opt; do
  case $opt in
  h)
    echo "This program is used to submit and grade your solutions." >&2
    echo "Usage: ./submitter"
    exit
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    exit 1
    ;;
  esac
done

if [[ -z "${SUBMISSION_USERNAME}" ]]; then
  echo "Please set SUBMISSION_USERNAME as your submission username first with the command:"
  echo "export SUBMISSION_USERNAME=\"value\""
  exit 1
else
  submissionUsername="${SUBMISSION_USERNAME}"
fi

if [[ -z "${SUBMISSION_PASSWORD}" ]]; then
  echo "Please set SUBMISSION_PASSWORD as your submission password from the Sail() platform with the command:"
  echo "export SUBMISSION_PASSWORD=\"value\""
  exit 1
else
  submissionPassword="${SUBMISSION_PASSWORD}"
fi

echo "Uploading answers..."
echo "Files larger than 5M will be ignored."
# exclude /target/maven-status/maven-compiler-plugin/ log files
find_files_to_submit | tar -cvzf $(dirname "$0")/"$submissionUsername".tar.gz -T - &>/dev/null
postUrl="https://$ags_dns/submit?signature=$signature&submissionUsername=$submissionUsername&submissionPassword=$submissionPassword&dns=$studentDNS&projectId=$projectId&taskId=$taskId&secretKey=$secretKey&duration=$duration&lmsName=$lmsName&courseType=$courseType&artifactVersion=$artifactVersion"
submitFile=$(dirname "$0")/"$submissionUsername".tar.gz
if ! curl -s -F file=@"$submitFile" "$postUrl"; then
  echo "Submission failed, please check your password or try again later."
  exit
else
  # the code can also reaches here with submission failure due to a existing pending submission
  echo "If your submission is uploaded successfully. Log in to the Sail() platform and open the submissions table to see how you did!"

  rm -rf $(dirname "$0")/"$submissionUsername".tar.gz
fi
