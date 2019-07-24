package meta;

import database.LevelStorage;
import helper.CustomLogger;

import java.util.Random;
import java.util.Scanner;
import java.util.Set;

public class LevelSelection {
	private int numberOfLevels;
	private int currentLevel;
	private int startLevel;
    private int no_of_levels; // if startLevel is set, only startLevel ... startLevel + no_of_levels are played
	private int numberOfTimesPlayedTheMost = -1;
	private int numberOfTimesPlayedMinimum = 1000;
	private boolean allLostLevelsPlayedTwice = false;
	private int lastLostLevel = -1;

	public LevelSelection(int numberOfLevels, int startlevel, int no_of_levels) {
		this.numberOfLevels = numberOfLevels;   // total number of levels to play
        this.startLevel     = startlevel;       // first level our agent will play FIXME: in competition this should be random!
        this.no_of_levels   = no_of_levels;     // if >0, then limit range of levels played to startLevel ... startLevel + no_of_levels
        currentLevel        = 0;                // currentLevel == 0 signals that we have not yet selected any levels
	}
    
	public int selectNextLevel() {

		if (currentLevel == 0) {
            // FIXME: for final agent submission we'll start at a random level (in case we hang an experience cold restart)
            //Random generator = new Random();
            //generator.nextInt(numberOfLevels) + 1;
            currentLevel = this.startLevel;
            if (currentLevel == 0) currentLevel = 1;
		} else {
			currentLevel++;
		}

		// stay in range of the numberOfLevels
		if (currentLevel > numberOfLevels) {
            currentLevel = 1;
        }
        
        // if max. range of levels is set, stay within range
        if (no_of_levels > 0) {
            if (currentLevel >= startLevel+no_of_levels) {
                currentLevel = startLevel;
            }
        }

		LevelStorage levelStorage = LevelStorage.getInstance();
		Set<Integer> playedLevels = levelStorage.getListOfIDs();

		// check whether the newly selected currentLevel was already played
		if (!playedLevels.contains(currentLevel)) {
			return currentLevel;
		} else {
            double totalScore    = 0;
            double scores[]      = new double[numberOfLevels];

            // compute scores for all levels
            for (Integer lvl : playedLevels) {
                Level level       = levelStorage.getLevelById(lvl);
                double eMaxPoints = level.getEstimatedMaximalPoints();
                double bestScore  = level.getBestScore();
                Integer nPlayed   = level.numberOfTimesPlayed;
                Integer nTargets  = level.initialTargets.size();
                Integer nBirds    = level.numOfBirds;
                
                double posGain = eMaxPoints - bestScore;
                if (nTargets > 0) {
                    posGain /= nPlayed/Math.pow(nTargets, nBirds);
                }
                scores[lvl] = posGain;
                totalScore += posGain;
            }

            // select next level randomly based on scores
            double selection = new Random().nextDouble() * totalScore;
            for (Integer lvl : playedLevels) {
                selection -= scores[lvl];
                if (selection <= 0.0) {
                    currentLevel = lvl;
                    break;
                }
            }
            
            return currentLevel;
        }
    }
}