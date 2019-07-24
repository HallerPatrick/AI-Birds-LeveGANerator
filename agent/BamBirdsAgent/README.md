BamBird 2017
============

Repository structure
--------------------

- `game/`: files required to install and start the game (including
  **instructions in `README.md`** file)
- `src/`: source code of our agent
  - `src/Java/jars/`: Java libraries necessary to compile and run the agent
  - `src/Java/src/`: Java source code
  - `src/Prolog/`: legacy Prolog source code from 2016 (*read at your own risk*)
  - `src/NewProlog/`: fresh and juicy Prolog code from 2017
- `doc/`: documentation, etc.

Starting the BamBird agent
--------------------------

Make sure you are in the root directory of the BamBird repository (the same
directory this very file is located in).

1. Open Chrome:

	Make sure Chrome is configured correctly (see `game/README.md`). You have
	to select *SD* mode of the Angry Birds game, otherwise the server won't
	work.

2. Run the AIBirds server:

	Open a terminal and enter the following command:

	```
	ant run-server
	```

	This will open the server application.

3. Run the Agent:

	Open another terminal and enter this command:

	```
	ant run
	```

	Now the server application should have detected a connected client. Press
	*Start* in the server application.

	To shut-down, simply close the server application window or open the
    terminal in which you started the server and press `Ctrl-C`.

Using Ant
---------

The BamBird agent can be compiled, run and packaged
using [Apache Ant](https://ant.apache.org/). Use one of the following targets:

- **`run-server`**

	Execute the AIBirds server (`game/abV1.32/ABServer.jar`).

- **`run`**

	Execute the BamBird agent (`main.BamBird.class`).

	*Note:* BamBird expects the Prolog files to be in a directory called
    `./NewProlog/` (relative to the current working directory, i.e. the
    directory you are currently in). If they are missing the planning will not
    work. The easy way around this is to create a symbolic link pointing to
    `src/NewProlog` in the project root. You can also change into the `build/`
    directory and use `ant -f ../build.xml run`, but that's just silly.

	The following arguments can be passed by calling Ant with the `-D` option:
	- `host`: the host on which the ABServer is running (default: `localhost`)
	- `team`: the team ID (default: 0)
	- `swipl`: the path to SWI Prolog (default: `/usr/bin/swipl`)
	- `level`: first level the agent will choose (default: 1)

	For example:
	```
	ant run -Dhost=localhost -Dteam=12345 -Dswipl=/usr/bin/swipl 
	```

	For testing purposes the default values should be just fine.

- **`dist`**

	Create a JAR containing all compiled Java classes (including the library
    JARs) and Prolog files in the `dist/` directory.

	*Note*: The JAR packs the Prolog planner and will generate file and
        directory substructures. In order to add new Prolog files to the agent
        the JAVA source code has to be changed to also copy these files from the JAR


- `prepare`

	Create the directories in which the compiled files will be stored. This
    does not have to be called manually.

- `compile`

	Compile all Java files in the Java source directory to the `build/`
    directory and copy the Prolog files over. This does not have to be called
    manually.

- `clean`

	Remove the `build/` and `dist/` directories.
