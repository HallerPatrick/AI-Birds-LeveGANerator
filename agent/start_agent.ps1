
# Start agent server
start powershell {java -jar ScienceBirds-server.jar; Read-Host}

start powershell {java -jar NaiveAgent.jar -nasc; Read-Host}

