#Set-Location ..

# Start Xml Generator to gen images 
#Include CUDA dlls in env path
$env:Path += ";C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\extras\\CUPTI\\libx64;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\include;C:\\tools\\cuda\\bin;C:\\Program Files\\cudnn-10.0\\cuda\\bin"

Set-Location .\xml_generator
python.exe __main__.py -f ..\parameters.txt
Set-Location ..

# Move them into unity ressources folder
# Move-Item .\xml_generator\gen\* 

$testResultsPath = ".\level_result.txt"

if([System.IO.File]::Exists($testResultsPath)){
    #Remove-Item -Path $testResultsPath
}

# Start Game
#
$unityId = (Start-Process .\game\Science-Birds-Windows\ScienceBirds.exe -PassThru).ID

Start-Process -FilePath C:\"Program Files (x86)"\AutoSizer\AutoSizer
$autoSizerShell = New-Object -ComObject wscript.shell;
$autoSizerShell.AppActivate("AutoSizer")


Start-Sleep 2
$autoSizerShell.SendKeys("%9")


# Start Server
$serverId = (Start-Process java "-jar .\game\agent\ScienceBirds-server.jar" -RedirectStandardOutput .\log\server.log -PassThru).Id
Start-Sleep 1

# Start Agent
$clientId = (Start-Process cmd -Argument '/c C:\PROGRA~1\Java\jdk-12\bin\java.exe -classpath C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\build;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\json-simple-1.1.1.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\WebSocket.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\Jama-1.0.2.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\commons-codec-1.7.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\junit-4.12.jar;C:\Users\Patrick\Projects\AI-Birds-LeveGANerator\game\agent\BamBirdsAgent\src\Java\jars\dyn4j-3.2.1.jar ab.demo.MainEntry -nasc 3' -RedirectStandardOutput .\log\client.log -PassThru).Id


# Start connection between client and server from control panel
$panelName = "Server Control Panel"
$whsell = New-Object -ComObject wscript.shell;
Start-Sleep 4
$whsell.AppActivate($panelName)
$whsell.SendKeys('~')




$clientFinished = $false
$saveWord = "Quadrupole"
while(-not $clientFinished) {
    foreach($line in Get-Content .\log\client.log) {
        if($line -match $saveWord){
            $clientFinished = $true
        }
    }
    Start-Sleep 5
}

Stop-Process $unityId

Stop-Process $serverId


Write-Output "Finished"


python automator/prepare_samples.py

python .\raw_level_generator\raw_image_builder.py --folder .\raw_level_generator\won_levels

