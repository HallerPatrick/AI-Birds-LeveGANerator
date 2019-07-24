package meta;

import ab.demo.other.Shot;
import ab.vision.ABObject;
import ab.vision.ABType;
import ab.vision.GameStateExtractor;
import database.Slingshot;
import features.Scene;
import helper.CustomLogger;
import planner.DecisionTree;
import planner.Target;
import shot.ShotPlanner;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;

public class Level {
	public enum State {
		OPEN, WON, LOST
	}

	public int levelId;
	private int maximalPointsWithoutPigs = 0;
	private int _bestScore = 0;
	public int numberOfTimesPlayed = 0;
	public int numOfBirds = 0;
	public boolean numOfBirdsConfident = false;
	private Slingshot slingshot = null;
	private double scalingFactor = 1.005;

	private State _state = State.OPEN;
	public List<Target> initialTargets = null;
	transient public List<Triplet<Shot, Target, Integer>> executedShots = new ArrayList<>();

	private Scene initialScene = null;
	transient public Scene currentScene = null;
	public DecisionTree tree = new DecisionTree();


	public Level(int levelid) {
		this.levelId = levelid;
	}

	public Slingshot getSlingshot() { return slingshot; }
	public double getScalingFactor() { return scalingFactor; }
	public boolean hasInitialScene() { return (initialScene != null); }
	public int getBestScore() { return _bestScore; }
	public int getEstimatedMaximalPoints() { return this.maximalPointsWithoutPigs + (numOfBirds - 1) * 10000; }

	public void setInitialScene(Scene s) {
		this.initialScene = s;
		this.maximalPointsWithoutPigs = 0;
		if (s != null) {
			this.maximalPointsWithoutPigs = s.estimateMaximalPointsWithoutBirds();
			setSlingshotAndScaling(s.slingshot, s.scalingFactor);
		}
	}

	public void ditchInitialScene() {
		setInitialScene(null);
		initialTargets = null;
		numOfBirds = 0;
		numOfBirdsConfident = false;
		slingshot = null;
		scalingFactor = 1.005;
		// TODO: reset limited time update slingshot counter once implemented
		tree = new DecisionTree();
		executedShots = new ArrayList<>();
	}

	public void finishLevel(GameStateExtractor.GameState state, int score) {
		numberOfTimesPlayed++;
		setLevelState(state);
		if (state == GameStateExtractor.GameState.WON) {
			if (score > _bestScore)
				_bestScore = score;
		}
		tree.finishGame(state);
		resetToUnloadedState();
	}

	public void setLevelState(GameStateExtractor.GameState state) {
		switch (state) {
		case WON:
		case LOST:
			// once won keep the level in that state no matter if we fail later
			if (_state != State.WON) {
				if (state == GameStateExtractor.GameState.WON)
					_state = State.WON;
				else
					_state = State.LOST;
			}
		}
	}

	public final State getLevelState() {
		return _state;
	}

	public void setSlingshotAndScaling(Slingshot sling, double scalingFactor) {
		boolean updated = false;
		if (sling != null) {
			this.slingshot = sling;
			updated = true;
		}
		if (scalingFactor > 0.1 && this.scalingFactor != scalingFactor) {
			this.scalingFactor = scalingFactor;
			updated = true;
		}
		if (updated) {
			// TODO: update only limited times, will prevent decision tree issues
		}
	}

	/** Create a screenshot without UI and all pigs previous position masked */
	public BufferedImage screenshotWithoutMovingParts() {
		BufferedImage screenShot = ActionRobot.get().screenshotWithoutUI(slingshot.bounds.x + slingshot.bounds.width);
		Graphics2D g2d = screenShot.createGraphics();
		g2d.setColor(Color.darkGray);
		g2d.fillRect(800, 190, 40, 100); // right wiggling triangle
		try {
			List<ABObject> pigs = currentScene.getPigs();
			if (pigs != null) {
				for (ABObject pig : pigs) {
					Rectangle r = new Rectangle(pig.getCenter());
					// the eyes of grandpa and helmet are too far apart, thats why 0.9
					r.grow((int)(pig.width * 0.9), (int)(pig.height * 0.85));
					g2d.fillRect(r.x, r.y, r.width, r.height); // because pigs are blinking
				}
			}
		} catch (Exception e){
			CustomLogger.severe("[Level] error masking pigs, returning regular screenshot...");
		}
		return screenShot;
	}

	public void wasShotIneffective(){

	}

	public ShotPlanner getShotPlanner() {
		ABType birdType;
		try { birdType = currentScene.getBirds().get(0).getType(); }
		catch (Exception e) { birdType = ABType.RedBird; }
		return new ShotPlanner(this.slingshot, this.scalingFactor, birdType);
	}

	public void resetToUnloadedState() {
		this.currentScene = this.initialScene;
		this.executedShots = new ArrayList<>();
		this.tree.resetToRootNode();
	}

	public void calculateReachabilityForScene(Scene scene) {
		if (scene == null)
			scene = currentScene;
		if (scene != null && scene.getReachableTargets().isEmpty())
			scene.setReachabilityForAllBlocks(getShotPlanner());
	}

	public void addExecutedShot(Shot executedShot, Target target, int damagePoints) {
		executedShots.add(new Triplet<>(executedShot, target, damagePoints));
		CustomLogger.info("[Meta] Level " + levelId + ": shot " + executedShots.size()
				+ " added with " + damagePoints + " damage points");
	}

	@Override
	public String toString() {
		return "Level: " + levelId + " estimatedMaxPoints: " + getEstimatedMaximalPoints()
				+ " bestScore: " + _bestScore + " numberOfTimesPlayed: " + numberOfTimesPlayed;
	}
}
