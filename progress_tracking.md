# Progress tracking

Monday, 9.12.2024
- set up repo, environment and all files
- loaded datasets
- pivoted datasets

Tuesday, 10.12.2024
- created cleaning function for Q1 and Q2
- checked missing values -> how to fill NAs in??

Wednesday + Thursday, 11./12.12.2024
- dropped columns with > 20% NA ['q1c2_retireage', 'q1c2_jubonus', 'q1c3_immunlift', 'q1c3_evalints']
- split dataset into 15 micro-indicators (each of them containing 2-4 items)
- filled in NAs in each of the micro-indicators by row mode
- created micro-indicator by mean
- compared various options of micro-indicator mean:
  1) filling in NAs with mode
  2) not filling in NAs with mode
  3) recoded all fuzzy values into [0,1] + filled in NAs with mode 

NEXT STEP:
- create macro-indicators -> decide how to aggregate data (on median or mean?)

NICE TO HAVE:
- create documentation for missing values + recoding options (incl. visualizations?)
- country ranking
- questions ranking

OPEN QUESTIONS
- drop Island and Ireland

Ignacio:
use mode  -> to aggregate indicator
if you want to see the differences -> use mean
