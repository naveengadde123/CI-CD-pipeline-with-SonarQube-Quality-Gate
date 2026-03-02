# CI-CD-pipeline-with-SonarQube-Quality-Gate

Jenkins (Windows) + SonarQube (Ubuntu Linux)
📌 Project Overview

This project demonstrates a complete CI/CD pipeline integrating:

Jenkins (Windows)

SonarQube (Ubuntu Linux)

GitHub repository

SonarScanner

Quality Gate validation

The pipeline performs:

Source code checkout

Static code analysis using SonarQube

Quality Gate validation

Automatic pipeline pass/fail based on code quality

🏗 Architecture
Developer → GitHub → Jenkins (Windows)
                               ↓
                        SonarScanner
                               ↓
                    SonarQube (Ubuntu :9000)
                               ↓
                        Webhook Callback
                               ↓
                       Jenkins Quality Gate
🖥 Environment Setup
🔹 SonarQube (Ubuntu Linux)

Installed manually on Ubuntu.

Install Java
sudo apt update
sudo apt install openjdk-17-jdk -y
java -version
Download and Extract SonarQube

Download from official website of SonarQube.

wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-<version>.zip
sudo apt install unzip -y
unzip sonarqube-<version>.zip
sudo mv sonarqube-<version> /opt/sonarqube
Start SonarQube
cd /opt/sonarqube/bin/linux-x86-64
./sonar.sh start

Access SonarQube:

http://<ubuntu-ip>:9000

Default credentials:

Username: admin

Password: admin

🔹 Jenkins (Windows)

Installed locally on Windows.

Access URL:

http://localhost:8082/
🔌 Required Jenkins Plugins

Install from:

Manage Jenkins → Manage Plugins

SonarQube Scanner for Jenkins

Pipeline

Pipeline Stage View

Git

GitHub Integration

Credentials Binding

Restart Jenkins after installation.

⚙ Configure SonarScanner in Jenkins

Manage Jenkins → Global Tool Configuration

Under SonarQube Scanner:

Name: SonarScanner

Install automatically

Select latest version

🔐 Configure SonarQube Server in Jenkins

Manage Jenkins → Configure System → SonarQube Servers → Add

Name: SonarQube-Server

Server URL:

http://<ubuntu-ip>:9000
Generate Token in SonarQube

Login → My Account → Security → Generate Token

Copy token → Add in Jenkins as Secret Text credential.

🔔 Webhook Configuration (Critical)

In SonarQube:

Administration → Configuration → Webhooks → Create

Webhook URL:

http://<windows-ip>:8082/sonarqube-webhook/

Important:

Use Windows machine IP (not localhost)

Must end with /

Port 8082 must be open

Jenkins must be reachable from Ubuntu

This webhook allows SonarQube to notify Jenkins when analysis is complete.

📂 Project Files
Jenkinsfile
pipeline {
   agent any

   stages {

       stage('Checkout') {
           steps {
               checkout scm
           }
       }

       stage('SonarQube Analysis') {
           steps {
               script {
                   def scannerHome = tool 'SonarScanner'
                   withSonarQubeEnv('SonarQube-Server') {
                       bat "${scannerHome}\\bin\\sonar-scanner.bat"
                   }
               }
           }
       }

       stage('Quality Gate') {
           steps {
               timeout(time: 5, unit: 'MINUTES') {
                   waitForQualityGate abortPipeline: true
               }
           }
       }
   }

   post {
       success {
           echo 'Pipeline completed successfully!'
       }
       failure {
           echo 'Pipeline failed due to Quality Gate failure.'
       }
   }
}
sonar-project.properties
sonar.projectKey=flask-app
sonar.projectName=Flask Application
sonar.projectVersion=1.0
sonar.sources=.
sonar.sourceEncoding=UTF-8
🔄 Pipeline Execution Flow

Jenkins pulls code from GitHub

SonarScanner runs analysis

Report uploaded to SonarQube

SonarQube processes report

Webhook notifies Jenkins

Jenkins resumes pipeline

Quality Gate determines pass/fail

🛡 Quality Gate

Quality Gate checks:

Bugs

Vulnerabilities

Code Smells

Coverage %

Duplications %

If conditions fail:

waitForQualityGate abortPipeline: true

Pipeline fails automatically.

🧪 Testing Failure Scenario

Example insecure code used for testing:

password = "admin123"

def divide():
    a = 10
    b = 0
    return a / b

Issues detected:

Hardcoded credentials (Security vulnerability)

Division by zero (Bug)

Unused variables (Code smell)

Use of eval() (Critical vulnerability)

Quality Gate fails when rules are strict.

📊 How to View Analysis Results in SonarQube

Open:

http://<ubuntu-ip>:9000

Login

Click Projects

Select your project

Dashboard Displays:

Quality Gate status

Bugs

Vulnerabilities

Security Hotspots

Code Smells

Coverage

Duplications

View Detailed Issues:

Go to:

Issues → Filter by Type (Bug / Vulnerability / Code Smell)

Click any issue to see:

File name

Line number

Description

Suggested fix

View Analysis History:

Project → Activity

Shows:

Previous builds

Quality Gate results

Timeline comparison

🚨 Troubleshooting
Issue: Pipeline Timeout

Cause:
Webhook not configured correctly.

Solution:
Used Windows IP instead of localhost.

Issue: Network Connectivity

Ubuntu could not access Jenkins using localhost.

Solution:
Used Windows machine IP and opened port 8082 in firewall.

📚 Key Learnings

Difference between localhost and machine IP

Webhook callback mechanism

Jenkins asynchronous waiting for SonarQube

Static code analysis vs runtime errors

Cross-machine network configuration

🛠 Tools Used

Jenkins

SonarQube

GitHub

Ubuntu

Windows 11