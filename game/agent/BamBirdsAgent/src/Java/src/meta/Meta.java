package meta;

import ab.demo.other.Shot;
import ab.vision.GameStateExtractor;
import ab.vision.GameStateExtractor.GameState;
import ab.vision.Vision;
import database.LevelStorage;
import features.SceneInitialisationException;
import helper.CustomLogger;
import knowledge.Knowledge;
import main.BamBirdPaths;
import main.SWIConnector;
import meta.Level.State;
import planner.NewPrologPlanParser;
import planner.PrologPlanner;
import planner.Target;
import shot.ShotExecutor;
import shot.ShotPlanner;

import java.awt.Point;
import java.awt.image.BufferedImage;
import java.nio.file.Path;
import java.util.List;

public class Meta implements ShotExecutor.ShotExecutorCallback {
	static public boolean EVALUATE_SHOTS = true;

	private LevelSelection levelSelector;
	private SWIConnector connector;
	private GameStateExtractor extractor;
	private ShotExecutor shotExecutor = null;

	// state machine and shot evaluation
	private boolean levelInitialized = false;
	private Level currentLevel       = null;
	private int previousScore        = 0;
	private int lastPigCount         = 0;
	private Shot lastShot            = null;
	public Target lastTarget         = null;
	public String lastShotDescriptor = "";

	public Meta(String pathToSwipl, LevelSelection levelSelector) {
		this.levelSelector = levelSelector;
		this.connector     = new SWIConnector(pathToSwipl, BamBirdPaths.NEW_PROLOG_FUNCTIONS);
		(new Thread(connector)).start();
		this.extractor     = new GameStateExtractor();
	}

	/**
	 * Callback method for prolog file generation
	 */
	public List<Target> prologGetTargets(Level level, String basename) throws IllegalArgumentException {
		Path file = new Knowledge().buildModel(level, basename);
		PrologPlanner planner = new PrologPlanner(connector, file.toString(), new NewPrologPlanParser());
		return planner.planSynchronously(20000); // 20 seconds at most for planning...
	}

	/**
	 * Tell server to load a different level and update current level object
	 */
	private void selectNextLevel()  {
		levelInitialized = true;
		CustomLogger.info("Choosing new level ...");
		int lvl = levelSelector.selectNextLevel();
		CustomLogger.info("Loading Level " + lvl);
		ActionRobot.get().loadLevel((byte) lvl);

		// get level object from memory or create fresh one
		currentLevel = LevelStorage.getInstance().getLevelById(lvl);
		if (currentLevel == null) {
			currentLevel = new Level(lvl);
		}
		currentLevel.resetToUnloadedState();
		shotExecutor = new ShotExecutor(currentLevel, this::prologGetTargets, this);
		previousScore = currentLevel.getBestScore();
		try {
			Thread.sleep(100);
		} catch (InterruptedException ignored) {}
	}

	/**
	 * @return Returns true if Meta has just initialised or {@code shotCount > 10}
	 */
	private boolean shouldStartNextLevel() {
		if (!levelInitialized)
			return true; // game has just started  or  crashed

		if (shotExecutor.currentShot > 10) { // if vision fails and agent keeps clicking somewhere on the screen
			currentLevel.numberOfTimesPlayed += 3;
			currentLevel.ditchInitialScene();
			return true;
		}
		return false;
	}

	public void startMeta() throws InterruptedException {
		BufferedImage scr;

		while (ActionRobot.get().getState() != -1) { // terminate if signal byte -1 received, means competition is over
			GameState state = ActionRobot.get().checkState(); // one of: UNKNOWN, MAIN_MENU, EPISODE_MENU, LEVEL_SELECTION, LOADING, PLAYING, WON, LOST
			scr = null; // forget previous screenshot
			switch (state) {
				case PLAYING:
					if (shouldStartNextLevel()) {
						selectNextLevel();
						break;
					}
					// TODO: better decision when to wait longer
					if (currentLevel.getLevelState() == State.LOST) {
						helper.VisionHelper.waitTillSceneIsStable();
					}
					scr = ActionRobot.get().doScreenShot();
					evaluatePreviousShot(scr);

					if (!shotExecutor.run(scr)) {
						CustomLogger.severe("OUCH: shot planning or shooting failed, trying another level");
						currentLevel.tree.finishGame(GameState.LOST);
						selectNextLevel();
					}
					break;

				// at end of level record
				case LOST:
					if (levelInitialized)
						currentLevel.numOfBirdsConfident = true;
					// and also everything for WON ...
				case WON:
					if (levelInitialized) {
						scr = ActionRobot.get().doScreenShot();
						int endScore = extractor.getScoreEndGame(scr);
						currentLevel.finishLevel(state, endScore);
						if (EVALUATE_SHOTS) {
							CustomLogger.info(String.format("%s score: %d killed: %d",
									lastShotDescriptor, (endScore - previousScore), lastPigCount));
						}
						LevelStorage.getInstance().addLeveltoStorage(currentLevel);
					}
					selectNextLevel();
					break;
				case LOADING:
					Thread.sleep(1000);
					break;
				case LEVEL_SELECTION:
					selectNextLevel();
					break;
				default:
					CustomLogger.severe("unhandled game state, start game and navigate to level selection screen!");
					Thread.sleep(1000);
					break;
			}
		}
	}

	/**
	 * Calculate score difference to previous screen
	 * @param img Reusing screenshot from other analysis
	 */
	private void evaluatePreviousShot(BufferedImage img) {
		int newScore = 0;
		if (!shotExecutor.isFirstShot()) { // record score of previous shot
			newScore = extractor.getScoreInGame(img);
			currentLevel.addExecutedShot(lastShot, lastTarget, newScore - previousScore); // record score ...
			previousScore = newScore;
		}
		if (EVALUATE_SHOTS) {
			Vision v = new Vision(img);
			int pigsRemaining = v.findPigsRealShape().size();
			if (!shotExecutor.isFirstShot()) {
				//CustomLogger.info("Sl: pigsRemaining=" + pigsRemaining + ", lastPigCount=" + lastPigCount);
				CustomLogger.info(String.format("%s score: %d killed: %d",
						lastShotDescriptor, (newScore - previousScore), (lastPigCount - pigsRemaining)));
			}
			lastPigCount = pigsRemaining;
		}
	}

	/** @return false if timeout exceeded */
	private boolean waitForLevelEnd() {
		long future = System.currentTimeMillis() + 6000; // wait max 6s
		while (System.currentTimeMillis() < future) {
			CustomLogger.info("checking state: " + (future - System.currentTimeMillis()));
			switch (ActionRobot.get().checkState()) {
                case WON:
                    try { Thread.sleep(3000); } catch (Exception ignored) {}
                case LOST:
					return true;
			}
			try { Thread.sleep(100); } catch (Exception ignored) {}
		}
		return false;
	}

	public void shutdown() { }

	/**
	 * @return Return value for {@link ShotExecutor#run(BufferedImage)} command
	 */
	@Override public boolean sceneInitialisationFailed(BufferedImage img, SceneInitialisationException e) {
		// TODO: do something with sling not found, birds not found or pigs not found ?
		CustomLogger.severe("Scene detection failed: " + e.getMessage());
		return waitForLevelEnd();
	}

	/**
	 * Just before execution
	 */
	@Override public void shotSelected(Shot proposedShot, Target target, boolean demoShot) {
		if (EVALUATE_SHOTS) {
			lastTarget = target; // null in case of demo shot
			if (demoShot)
				lastShotDescriptor = currentLevel.currentScene + " Ta:(naive)";
			else
				lastShotDescriptor = currentLevel.currentScene + " Ta:(" + lastTarget + ")";
		}
	}

	/**
	 * Evaluated predicted parabola with actual and update decision tree
	 */
	@Override public void shotDelivered(Shot shot) {
		lastShot = shot;
		BufferedImage img = currentLevel.screenshotWithoutMovingParts();

		// Step 1: Evaluate parabola  (bird has just landed or is lying on the ground already)
		// Evaluate trajectory after shot only for unaltered parabolas
		ShotPlanner planner = currentLevel.getShotPlanner();
		Point releasePoint = new Point(shot.getDx(), shot.getDy());
		double newScale = planner.calculateScalingFactorAndUpdate(img, releasePoint, shot.getT_tap());
		// FIXME: check if slingshot detection failed for first level, otherwise any call to this level will fail
		currentLevel.setSlingshotAndScaling(null, newScale);

		// Step 2: Set decision tree image
		// compare current scene with scene of node we should currently be in
		// if different: create new node with current 'scene'
		currentLevel.tree.getCurrentNode().setShot(shot);
		currentLevel.tree.compareScreenshotsReplaceCurrentNode(img);
		currentLevel.tree.getCurrentNode().savePoints(currentLevel.currentScene.sortedTargetsList());
		currentLevel.tree.getCurrentNode().compareCurrentSituationWithPrevSituation();
	}

	/**
	 * Will be called after everything has come to a still (max 16s)
	 * @param moving Hard limit exceeded
	 */
	@Override public void shotDeliveredSceneStable(BufferedImage img, boolean moving, boolean noBirds, boolean noPigs) {
		if (noBirds || noPigs)
			waitForLevelEnd();
		// seems like we won the level, wait for server to record
		else if (extractor.getGameState(img) != GameState.PLAYING)
			try {Thread.sleep(100); } catch (Exception ignored) {}
	}
}