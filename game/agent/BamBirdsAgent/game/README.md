# Setup AIBirds: Game, Server and Agent
To run an Angry Birds bot you will need to

1. setup Chrome and add the AIBirds extension
2. modify your computers DNS records to prevent cache invalidation
3. replace Chrome cache folder
4. install Java and run the provisioned AIBirds server.

## 1. Google Chrome
1. I recommend to use a dedicated installation of Google Chrome to play the game. You won't have to mess with your main browser this way. You can either use [Chrome](https://www.google.de/chrome/browser/desktop/index.html), [Chrome Canary](https://www.google.com/chrome/browser/canary.html) (not available for Linux), [Chrome unstable](https://www.google.com/chrome/browser/desktop/index.html?platform=linux&extra=devchannel) or Chromium, whichever suits your needs.
2. Install the AIBirds Chrome extension: Open Chrome and navigate to [chrome://extensions/](chrome://extensions/). Check the `Developer mode` box, click `Load unpacked extension...` and choose the folder `abV1.32/plugin`.

## 2. DNS
1. Open the following file in a simple text editor (e.g. Notepad on Windows or TextEdit on OS X). Windows: `C:\WINDOWS\system32\drivers\etc\hosts`, OS X and Linux: `/etc/hosts`. Note that some folders might be hidden.
2. Add this line to the bottom of the document:
`127.0.0.1       chrome.angrybirds.com`. Save the file.
3. Open a browser window and try to visit `chrome.angrybirds.com`. An error message should be shown (e.g. "This site can't be reached").

## 3. Cache
1. Quit Chrome. 
2. Open the following path in your systems file explorer. Replace `$user$` with your user name and `$chrome$` with your version of Chrome (e.g. `google-chrome` for Chrome on Linux).  Windows: `C:\\Users\$user$\AppData\Local\Google\$chrome$\User Data\Default`, OS X: `/Users/$user$/Library/Application Support/Google/$chrome$/Default`, Linux: `/home/$user$/.config/$chrome$/Default`.
3. Unzip `Application Cache.zip` (it's in the same folder as this README). Copy the resulting folder `Application Cache` to the directory you've opened. By doing this you probably replace an existing folder.
5. Open Chrome and visit `chrome.angrybirds.com`. Angry Birds should be loading.

## 4. Java Setup
[Download](http://www.oracle.com/technetwork/java/javase/downloads/index.html) and install the JRE (Java Runtime Environment) or JDK (Java Development Kit).

# Run the Game, Server and Agent
After completing the necessary steps described above, you should be able to run the built-in naive agent.
1. Start Chrome and navigate to `chrome.angrybirds.com`. Make sure that the SD - mode is selected! HD does not work.
2. After the game has loaded, click on the big "PLAY" button and select the level pack on the bottom left ("Poached Eggs").
3. Open a terminal in the `abV1.32` folder.
4. Start the server: `java -jar ABServer.jar`.
5. Start the naive agent: `java -jar ABSoftware.jar -nasc`.
6. The server window should inform you about one connected client. Press "Start". The agent should select the first level and start playing! You have to manually confirm any pop-up dialogs.

# Additional Ressources
See `AIBirds-Getting-Started.pdf` and `AIBirds-Chrome-Issues.pdf` for more additional guidance. The Server and Agent is documented in `abV1.32/doc/`.
