# Start Xml Generator to gen images 
#Include CUDA dlls in env path
$env:Path += ";C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\extras\\CUPTI\\libx64;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\include;C:\\tools\\cuda\\bin;C:\\Program Files\\cudnn-10.0\\cuda\\bin"

Set-Location .\xml_generator
#python.exe __main__.py -f ..\parameters.txt
Set-Location ..

# Move them into unity ressources folder
# Move-Item .\xml_generator\gen\* 

# Start Game
.\game\Science-Birds-Windows\ScienceBirds.exe

# Start Server
# Start-Process "java -jar .\game\agent\ScienceBirds-server.jar"
Start-Process cmd -Argument "/c java -jar .\game\agent\ScienceBirds-server.jar" -RedirectStandardOutput .\log\server.log
Start-Sleep 1

# Start Agent
Start-Process cmd -Argument '/c C:\PROGRA~1\Java\jdk-12\bin\java.exe -classpath C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\out\production\abV1.32;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\external\jar-in-jar-loader.zip;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\external\WebSocket.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\external\commons-codec-1.7.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\external\Jama-1.0.2.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\game\abV1.32\external\json-simple-1.1.1.jar ab.demo.MainEntry -nasc' -RedirectStandardOutput .\log\client.log

$panelName = "Server Control Panel"

Start-Sleep 2

$whsell = New-Object -ComObject wscript.shell;

$whsell.AppActivate($panelName)

Start-Sleep .5

$whsell.SendKeys('~')


