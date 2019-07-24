## Instructions for adding additional Angry Birds levels:

1. In Chrome/Chromium, go to Settings->Tools->Extensions
2. Tick "Developer Mode"
3. Click "Load unpacked extensions..."
4. Select the "custom_levels" folder and confirm
5. Make sure the extension called "Angry Birds Interface" is enabled
6. Copy the .json files for the desired levels into the `custom_levels/levels` folder
7. These levels will replace the original levels on Angry Birds Chrome corresponding to their number

Levels must follow the following naming convention to replace the levels on the first poached eggs page:

Level1-1.json, Level1-2.json, Level1-3.json, etc. Up to a maximum of Level1-21.json

To replace the levels on the second and third poached eggs pages, use the naming convention Level2-X.json and Level3-X.json respectively

Some example json files used for levels in past competition are provided in `past_competition_levels` and test-levels should be stored in `test-levels`

## Troubleshooting

* Try deleting your browser cache
* Enable Allow in Incognito in chrome://extensions