package main;

import ab.demo.other.ClientActionRobot;
import features.VisualDebugger;
import helper.CustomLogger;
import helper.SrcFileCopy;
import meta.ActionRobot;
import meta.LevelSelection;
import meta.Meta;
import tester.ParabolaTester;

import java.util.Locale;

import static helper.Constants.DEBUG_ENABLED;


public class BamBird {
	private int numOfLevels;
	private LevelSelection levelSelector;
	/** The ongoing round in the competition. */
	private int roundInfo;
	/** The time limit in minutes. */
	private int timeLimit;

	private static BamBird instance = null;
	public static String serverHost = "";
	private static int team_id = 424242;
	private Meta meta;

	private BamBird() { }

	public static BamBird getInstance() {
		if (instance == null) {
			instance = new BamBird();
		}
		return instance;
	}

	private void start(String pathToSwipl, int start_level, int no_of_levels) {
		try {
			levelSelector = new LevelSelection(numOfLevels, start_level, no_of_levels); // setup level selection: # of levels, level storage

			//LevelStorage.getInstance().restoreFromFile(); // in case agent crashed
			meta = new Meta(pathToSwipl, levelSelector);
			meta.startMeta();

		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			meta.shutdown();
			//LevelStorage.getInstance().storeToFile();
		}
	}

	public static void main(String[] args) {
		// sets the language for the logger to "english" -- can be disabled
		Locale.setDefault(new Locale("en", "EN"));
		// if Constants.DEBUG_ENABLED=true, logger will log everything. Else, logger will only log "severe" messages.
		if (DEBUG_ENABLED){
			CustomLogger.setLogLevel(CustomLogger.LogLevel.INFO);
		} else {
			CustomLogger.severe("Started agent without info logging, only severe errors will be printed. To enable logging, change DEBUG_MODE in Constants.class.");
		}

		if (!VisualDebugger.globalDebuggingEnabled)
        	System.setProperty("java.awt.headless", "true"); // surpress menu bar
		if (args.length < 3) {
			CustomLogger.severe("Please provide valid arguments: server_host, team_id, path_to_swi-prolog, [start level, number of levels]");
			return;
		}

		serverHost = args[0];
		team_id = new Integer(args[1]);
        int start_level = 1;
        int no_of_levels = -1;
        if (args.length > 3) {
            try {
                start_level = Integer.parseInt(args[3]);
                if (args.length > 4) {
                    no_of_levels = Integer.parseInt(args[4]);
                }
            } catch (NumberFormatException e) {
                CustomLogger.warning("couldn't parse start level or level range, ignoring.");
            }
        }

		CustomLogger.info("Version 2018-07-16"); // FIXME: pull version from git

		SrcFileCopy.init(); // copy Prolog folder outside of jar

		BamBird bamBird = BamBird.getInstance();
		byte[] info = ActionRobot.get().configure(ClientActionRobot.intToByteArray(team_id));
		bamBird.roundInfo = info[0];
		bamBird.timeLimit = info[1];
		bamBird.numOfLevels = info[2]; // FIXME: should exploit other info from ABServer too

		CustomLogger.info("roundInfo: " + bamBird.roundInfo + ", timeLimit: " + bamBird.timeLimit + ", numOfLevels: " + bamBird.numOfLevels);

		if (false) {
			new ParabolaTester().start();
			return;
		}
		while (ActionRobot.get().getState() != -1) { // shut down if competition is over, all requests to the server should then return -1
			try {
				bamBird.start(args[2],start_level, no_of_levels);
			} catch (Exception e) {
				// Never crash for any reason, just retry forever
				CustomLogger.severe("A fatal error occurred:");
				e.printStackTrace();
				CustomLogger.severe(String.format("%n%nRestarting BamBird...%n%n"));
			}
		}
	}
}
