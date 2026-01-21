# Setup

Make sure to adjust the path to your conda environment in the environment.yml file.
Also, place unpleasant pictures (.jpg) and sound (tv.wav) into subfolder iaps.


# Configuration Settings

Configuration settings for the application are stored in the `settings.json` file, located in the installation folder at `%LOCALAPPDATA%\Programs\4Sc1\ExperimentApp`. This file controls the flow and operational mode of your application, helping to tailor the user experience for testing or regular use.

## `mode`
- **Type**: String
- **Description**: Specifies the mode in which the application runs.
- **Options**:
  - `test`: Used for testing features. In this mode, additional shortcuts may be enabled, and the application can be closed by pressing the ESC button. However, this might not work while being in a trial.
  - `experiment`: Standard operation mode without shortcuts.

## `shortcut`
- **Type**: String
- **Description**: Defines a shortcut to a specific test within the application. This setting is only effective in `test` mode.
- **Options**:
  - `nback`: Shortcut to the n-back test.
  - `eaa`: Shortcut to the EAA test.
  - `stroop`: Shortcut to the Stroop test.
  - `wisconsin`: Shortcut to the Wisconsin test.

## Experiment Results Storage

- **Location**: The results of the experiments will be stored in participant-specific subfolders located within the `%LOCALAPPDATA%\ExperimentResults` folder. This organization helps in maintaining a structured and easily accessible format for individual participant data.
