
# Set cuda envs manually
# Example
$env:Path += ";C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\extras\\CUPTI\\libx64;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\include;C:\\tools\\cuda\\bin;C:\\Program Files\\cudnn-10.0\\cuda\\bin"

# ARGS
$unityGamePath=$args[0]
$autosizerPath=$args[1]
$clientPath=$args[2]
$serverPath=$args[3]

$logPath = "..\log\client.log"
Write-Output "Following paths are set"
Write-Output "Unity game path: " $unityGamePath
Write-Output "Client jar path: " $clientPath
Write-Output "Server jar path: " $serverPath
Write-Output "Autosizer path: " $autosizerPath


### Start Game ###
$unityId = (Start-Process $unityGamePath -PassThru).ID


### Autosizer ###
if ($autosizerPath -ne "None") {
    Start-Process -FilePath $autosizerPath
    $autoSizerShell = New-Object -ComObject wscript.shell;
    $autoSizerShell.AppActivate("AutoSizer")

    # Use shortcut manuel setup up to auto size unity
    Start-Sleep 2
    $autoSizerShell.SendKeys("%9")
}


### Server ###
$serverId = (Start-Process java "-jar $serverPath" -PassThru).Id
Start-Sleep 1


### Client ###
$clientCommand = "-jar " + $clientPath + " -nasc"
Write-Output $clientCommand
#$clientId = (Start-Process java $clientCommand -RedirectStandardOutput $logPath -PassThru ).Id
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
    foreach($line in Get-Content $logPath) {
        if($line -match $saveWord){
            $clientFinished = $true
        }
    }
    Start-Sleep 5
}

Stop-Process $unityId
Stop-Process $serverId

Write-Output "Finished"

