# TTC Tire Parser
_Visualization and modelling tool for data from the FSAE Tire Test Consortuim_

## How To Use
1. Input TTC raw or run data file paths.
2. The program will visualize several useful plots. Take note of the run start/end indices before/after the cooldown/warmup.
3. The program wil visualize the same plots with the data sliced as needed. Take note of the number of tire pressures, inclination angles, and vertical loads used. These are the controlled variables which Calspan iterates through in testing.
4. The program will then provide a grid plot of the data.

## Limitations
- Only pure slip conditions ($SA=0$ for longitudinal data)
- Magic formula 5.2 not yet implemented
