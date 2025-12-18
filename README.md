# NBA Player Analytics Data Dictionary

## Overview
This dataset aggregates advanced NBA player tracking data from multiple sources, providing a granular view of player performance across shooting, defense, rebounding, play-type efficiency, and physical profiles.

---

## 1. Shot Location (Zones)
**File Name:** `full_players_shotloc.csv`

### Human-Readable Glossary
Tracks shooting efficiency broken down by court zones.
* **Zones:** `Restricted Area`, `In The Paint (Non-RA)`, `Mid-Range`, `Corner 3`, `Above the Break 3`.
* **Metrics:**
    * **FGM/FGA:** Field Goals Made/Attempted.
    * **FG_PCT:** Field Goal Percentage.
    * **FREQ:** Frequency (Percentage of total shots taken from this zone).

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Unique Player Identifier |
| `PLAYER` | object | Player Name |
| `SEASON` | object | NBA Season (e.g., 2023-24) |
| `Restricted Area - FGM` | int64 | FGM in zone: Restricted Area |
| `Restricted Area - FGA` | int64 | FGA in zone: Restricted Area |
| `Restricted Area - FG_PCT` | float64 | FG% in zone: Restricted Area |
| `Restricted Area - FREQ` | float64 | Shot Freq in zone: Restricted Area |
| `In The Paint (Non-RA) - FGM` | int64 | FGM in zone: In The Paint (Non-RA) |
| `In The Paint (Non-RA) - FGA` | int64 | FGA in zone: In The Paint (Non-RA) |
| `In The Paint (Non-RA) - FG_PCT` | float64 | FG% in zone: In The Paint (Non-RA) |
| `In The Paint (Non-RA) - FREQ` | float64 | Shot Freq in zone: In The Paint (Non-RA) |
| `Mid-Range - FGM` | int64 | FGM in zone: Mid-Range |
| `Mid-Range - FGA` | int64 | FGA in zone: Mid-Range |
| `Mid-Range - FG_PCT` | float64 | FG% in zone: Mid-Range |
| `Mid-Range - FREQ` | float64 | Shot Freq in zone: Mid-Range |
| `Left Corner 3 - FGM` | int64 | FGM in zone: Left Corner 3 |
| `Left Corner 3 - FGA` | int64 | FGA in zone: Left Corner 3 |
| `Left Corner 3 - FG_PCT` | float64 | FG% in zone: Left Corner 3 |
| `Left Corner 3 - FREQ` | float64 | Shot Freq in zone: Left Corner 3 |
| `Right Corner 3 - FGM` | int64 | FGM in zone: Right Corner 3 |
| `Right Corner 3 - FGA` | int64 | FGA in zone: Right Corner 3 |
| `Right Corner 3 - FG_PCT` | float64 | FG% in zone: Right Corner 3 |
| `Right Corner 3 - FREQ` | float64 | Shot Freq in zone: Right Corner 3 |
| `Above the Break 3 - FGM` | int64 | FGM in zone: Above the Break 3 |
| `Above the Break 3 - FGA` | int64 | FGA in zone: Above the Break 3 |
| `Above the Break 3 - FG_PCT` | float64 | FG% in zone: Above the Break 3 |
| `Above the Break 3 - FREQ` | float64 | Shot Freq in zone: Above the Break 3 |
| `Corner 3 - FGM` | int64 | FGM in zone: Corner 3 (Total) |
| `Corner 3 - FGA` | int64 | FGA in zone: Corner 3 (Total) |
| `Corner 3 - FG_PCT` | float64 | FG% in zone: Corner 3 (Total) |
| `Corner 3 - FREQ` | float64 | Shot Freq in zone: Corner 3 (Total) |
| `TOTAL_FGM` | float64 | Total Season FGM (All Zones) |
| `TOTAL_FGA` | float64 | Total Season FGA (All Zones) |

---

## 2. Shot Type & Context
**File Name:** `full_players_shottype_small.csv`

### Human-Readable Glossary
Tracks shooting efficiency based on the context of the shot (dribbles, defense, time).
* **Contexts:**
    * **Dribbles:** `0`, `1`, `2`, `3-6`, `7+`.
    * **Defender Distance:** `Very Tight (0-2ft)`, `Tight (2-4ft)`, `Open (4-6ft)`, `Wide Open (6+ft)`.
    * **Touch Time:** `< 2 Seconds`, `2-6 Seconds`, `6+ Seconds`.
    * **Shot Type:** `Pull Ups`, `Catch and Shoot`.
* **Metrics:**
    * **2 FGM/A:** 2-Point stats.
    * **3 FGM/A:** 3-Point stats.
    * **FGM/A:** Total stats.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `TEAM_ID` | float64 | Identifier |
| `0 Dribbles - 2 FGA` | float64 | 2pt Attempts with 0 Dribbles |
| `0 Dribbles - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (0 Dribbles) |
| `0 Dribbles - 2 FGM` | float64 | 2pt Makes with 0 Dribbles |
| `0 Dribbles - 2 FG_PCT` | float64 | 2pt % with 0 Dribbles |
| `0 Dribbles - 3 FGA` | float64 | 3pt Attempts with 0 Dribbles |
| `0 Dribbles - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (0 Dribbles) |
| `0 Dribbles - 3 FGM` | float64 | 3pt Makes with 0 Dribbles |
| `0 Dribbles - 3 FG_PCT` | float64 | 3pt % with 0 Dribbles |
| `0 Dribbles - FGA` | float64 | Total Attempts with 0 Dribbles |
| `0 Dribbles - FGA_FREQ` | float64 | Frequency of Total Attempts (0 Dribbles) |
| `0 Dribbles - FGM` | float64 | Total Makes with 0 Dribbles |
| `0 Dribbles - FG_PCT` | float64 | Total % with 0 Dribbles |
| `0-2 Feet - Very Tight - 2 FGA` | float64 | 2pt Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 2 FGM` | float64 | 2pt Makes (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 2 FG_PCT` | float64 | 2pt % (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 3 FGA` | float64 | 3pt Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 3 FGM` | float64 | 3pt Makes (Defender 0-2ft) |
| `0-2 Feet - Very Tight - 3 FG_PCT` | float64 | 3pt % (Defender 0-2ft) |
| `0-2 Feet - Very Tight - FGA` | float64 | Total Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - FGA_FREQ` | float64 | Frequency of Total Attempts (Defender 0-2ft) |
| `0-2 Feet - Very Tight - FGM` | float64 | Total Makes (Defender 0-2ft) |
| `0-2 Feet - Very Tight - FG_PCT` | float64 | Total % (Defender 0-2ft) |
| `1 Dribble - 2 FGA` | float64 | 2pt Attempts (1 Dribble) |
| `1 Dribble - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (1 Dribble) |
| `1 Dribble - 2 FGM` | float64 | 2pt Makes (1 Dribble) |
| `1 Dribble - 2 FG_PCT` | float64 | 2pt % (1 Dribble) |
| `1 Dribble - 3 FGA` | float64 | 3pt Attempts (1 Dribble) |
| `1 Dribble - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (1 Dribble) |
| `1 Dribble - 3 FGM` | float64 | 3pt Makes (1 Dribble) |
| `1 Dribble - 3 FG_PCT` | float64 | 3pt % (1 Dribble) |
| `1 Dribble - FGA` | float64 | Total Attempts (1 Dribble) |
| `1 Dribble - FGA_FREQ` | float64 | Frequency of Total Attempts (1 Dribble) |
| `1 Dribble - FGM` | float64 | Total Makes (1 Dribble) |
| `1 Dribble - FG_PCT` | float64 | Total % (1 Dribble) |
| `2 Dribbles - 2 FGA` | float64 | 2pt Attempts (2 Dribbles) |
| `2 Dribbles - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (2 Dribbles) |
| `2 Dribbles - 2 FGM` | float64 | 2pt Makes (2 Dribbles) |
| `2 Dribbles - 2 FG_PCT` | float64 | 2pt % (2 Dribbles) |
| `2 Dribbles - 3 FGA` | float64 | 3pt Attempts (2 Dribbles) |
| `2 Dribbles - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (2 Dribbles) |
| `2 Dribbles - 3 FGM` | float64 | 3pt Makes (2 Dribbles) |
| `2 Dribbles - 3 FG_PCT` | float64 | 3pt % (2 Dribbles) |
| `2 Dribbles - FGA` | float64 | Total Attempts (2 Dribbles) |
| `2 Dribbles - FGA_FREQ` | float64 | Frequency of Total Attempts (2 Dribbles) |
| `2 Dribbles - FGM` | float64 | Total Makes (2 Dribbles) |
| `2 Dribbles - FG_PCT` | float64 | Total % (2 Dribbles) |
| `2-4 Feet - Tight - 2 FGA` | float64 | 2pt Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - 2 FGM` | float64 | 2pt Makes (Defender 2-4ft) |
| `2-4 Feet - Tight - 2 FG_PCT` | float64 | 2pt % (Defender 2-4ft) |
| `2-4 Feet - Tight - 3 FGA` | float64 | 3pt Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - 3 FGM` | float64 | 3pt Makes (Defender 2-4ft) |
| `2-4 Feet - Tight - 3 FG_PCT` | float64 | 3pt % (Defender 2-4ft) |
| `2-4 Feet - Tight - FGA` | float64 | Total Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - FGA_FREQ` | float64 | Frequency of Total Attempts (Defender 2-4ft) |
| `2-4 Feet - Tight - FGM` | float64 | Total Makes (Defender 2-4ft) |
| `2-4 Feet - Tight - FG_PCT` | float64 | Total % (Defender 2-4ft) |
| `3-6 Dribbles - 2 FGA` | float64 | 2pt Attempts (3-6 Dribbles) |
| `3-6 Dribbles - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (3-6 Dribbles) |
| `3-6 Dribbles - 2 FGM` | float64 | 2pt Makes (3-6 Dribbles) |
| `3-6 Dribbles - 2 FG_PCT` | float64 | 2pt % (3-6 Dribbles) |
| `3-6 Dribbles - 3 FGA` | float64 | 3pt Attempts (3-6 Dribbles) |
| `3-6 Dribbles - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (3-6 Dribbles) |
| `3-6 Dribbles - 3 FGM` | float64 | 3pt Makes (3-6 Dribbles) |
| `3-6 Dribbles - 3 FG_PCT` | float64 | 3pt % (3-6 Dribbles) |
| `3-6 Dribbles - FGA` | float64 | Total Attempts (3-6 Dribbles) |
| `3-6 Dribbles - FGA_FREQ` | float64 | Frequency of Total Attempts (3-6 Dribbles) |
| `3-6 Dribbles - FGM` | float64 | Total Makes (3-6 Dribbles) |
| `3-6 Dribbles - FG_PCT` | float64 | Total % (3-6 Dribbles) |
| `4-6 Feet - Open - 2 FGA` | float64 | 2pt Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - 2 FGM` | float64 | 2pt Makes (Defender 4-6ft) |
| `4-6 Feet - Open - 2 FG_PCT` | float64 | 2pt % (Defender 4-6ft) |
| `4-6 Feet - Open - 3 FGA` | float64 | 3pt Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - 3 FGM` | float64 | 3pt Makes (Defender 4-6ft) |
| `4-6 Feet - Open - 3 FG_PCT` | float64 | 3pt % (Defender 4-6ft) |
| `4-6 Feet - Open - FGA` | float64 | Total Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - FGA_FREQ` | float64 | Frequency of Total Attempts (Defender 4-6ft) |
| `4-6 Feet - Open - FGM` | float64 | Total Makes (Defender 4-6ft) |
| `4-6 Feet - Open - FG_PCT` | float64 | Total % (Defender 4-6ft) |
| `6+ Feet - Wide Open - 2 FGA` | float64 | 2pt Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - 2 FGM` | float64 | 2pt Makes (Defender 6+ft) |
| `6+ Feet - Wide Open - 2 FG_PCT` | float64 | 2pt % (Defender 6+ft) |
| `6+ Feet - Wide Open - 3 FGA` | float64 | 3pt Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - 3 FGM` | float64 | 3pt Makes (Defender 6+ft) |
| `6+ Feet - Wide Open - 3 FG_PCT` | float64 | 3pt % (Defender 6+ft) |
| `6+ Feet - Wide Open - FGA` | float64 | Total Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - FGA_FREQ` | float64 | Frequency of Total Attempts (Defender 6+ft) |
| `6+ Feet - Wide Open - FGM` | float64 | Total Makes (Defender 6+ft) |
| `6+ Feet - Wide Open - FG_PCT` | float64 | Total % (Defender 6+ft) |
| `7+ Dribbles - 2 FGA` | float64 | 2pt Attempts (7+ Dribbles) |
| `7+ Dribbles - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (7+ Dribbles) |
| `7+ Dribbles - 2 FGM` | float64 | 2pt Makes (7+ Dribbles) |
| `7+ Dribbles - 2 FG_PCT` | float64 | 2pt % (7+ Dribbles) |
| `7+ Dribbles - 3 FGA` | float64 | 3pt Attempts (7+ Dribbles) |
| `7+ Dribbles - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (7+ Dribbles) |
| `7+ Dribbles - 3 FGM` | float64 | 3pt Makes (7+ Dribbles) |
| `7+ Dribbles - 3 FG_PCT` | float64 | 3pt % (7+ Dribbles) |
| `7+ Dribbles - FGA` | float64 | Total Attempts (7+ Dribbles) |
| `7+ Dribbles - FGA_FREQ` | float64 | Frequency of Total Attempts (7+ Dribbles) |
| `7+ Dribbles - FGM` | float64 | Total Makes (7+ Dribbles) |
| `7+ Dribbles - FG_PCT` | float64 | Total % (7+ Dribbles) |
| `Catch and Shoot - 2 FGA` | float64 | 2pt Attempts (Catch and Shoot) |
| `Catch and Shoot - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Catch and Shoot) |
| `Catch and Shoot - 2 FGM` | float64 | 2pt Makes (Catch and Shoot) |
| `Catch and Shoot - 2 FG_PCT` | float64 | 2pt % (Catch and Shoot) |
| `Catch and Shoot - 3 FGA` | float64 | 3pt Attempts (Catch and Shoot) |
| `Catch and Shoot - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Catch and Shoot) |
| `Catch and Shoot - 3 FGM` | float64 | 3pt Makes (Catch and Shoot) |
| `Catch and Shoot - 3 FG_PCT` | float64 | 3pt % (Catch and Shoot) |
| `Catch and Shoot - FGA` | float64 | Total Attempts (Catch and Shoot) |
| `Catch and Shoot - FGA_FREQ` | float64 | Frequency of Total Attempts (Catch and Shoot) |
| `Catch and Shoot - FGM` | float64 | Total Makes (Catch and Shoot) |
| `Catch and Shoot - FG_PCT` | float64 | Total % (Catch and Shoot) |
| `Less than 10 ft - 2 FGA` | float64 | 2pt Attempts (<10ft) |
| `Less than 10 ft - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (<10ft) |
| `Less than 10 ft - 2 FGM` | float64 | 2pt Makes (<10ft) |
| `Less than 10 ft - 2 FG_PCT` | float64 | 2pt % (<10ft) |
| `Less than 10 ft - 3 FGA` | float64 | 3pt Attempts (<10ft) |
| `Less than 10 ft - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (<10ft) |
| `Less than 10 ft - 3 FGM` | float64 | 3pt Makes (<10ft) |
| `Less than 10 ft - 3 FG_PCT` | float64 | 3pt % (<10ft) |
| `Less than 10 ft - FGA` | float64 | Total Attempts (<10ft) |
| `Less than 10 ft - FGA_FREQ` | float64 | Frequency of Total Attempts (<10ft) |
| `Less than 10 ft - FGM` | float64 | Total Makes (<10ft) |
| `Less than 10 ft - FG_PCT` | float64 | Total % (<10ft) |
| `OVERALL - 2 FGA` | int64 | Total 2pt Attempts |
| `OVERALL - 2 FGA_FREQ` | float64 | Total 2pt Frequency |
| `OVERALL - 2 FGM` | int64 | Total 2pt Makes |
| `OVERALL - 2 FG_PCT` | float64 | Total 2pt % |
| `OVERALL - 3 FGA` | int64 | Total 3pt Attempts |
| `OVERALL - 3 FGA_FREQ` | float64 | Total 3pt Frequency |
| `OVERALL - 3 FGM` | int64 | Total 3pt Makes |
| `OVERALL - 3 FG_PCT` | float64 | Total 3pt % |
| `OVERALL - FGA` | int64 | Total Attempts |
| `OVERALL - FGA_FREQ` | float64 | Total Frequency |
| `OVERALL - FGM` | int64 | Total Makes |
| `OVERALL - FG_PCT` | float64 | Total FG% |
| `Other - 2 FGA` | float64 | 2pt Attempts (Other Context) |
| `Other - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Other) |
| `Other - 2 FGM` | float64 | 2pt Makes (Other) |
| `Other - 2 FG_PCT` | float64 | 2pt % (Other) |
| `Other - 3 FGA` | float64 | 3pt Attempts (Other Context) |
| `Other - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Other) |
| `Other - 3 FGM` | float64 | 3pt Makes (Other) |
| `Other - 3 FG_PCT` | float64 | 3pt % (Other) |
| `Other - FGA` | float64 | Total Attempts (Other) |
| `Other - FGA_FREQ` | float64 | Frequency of Total Attempts (Other) |
| `Other - FGM` | float64 | Total Makes (Other) |
| `Other - FG_PCT` | float64 | Total % (Other) |
| `Pull Ups - 2 FGA` | float64 | 2pt Attempts (Pull Ups) |
| `Pull Ups - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Pull Ups) |
| `Pull Ups - 2 FGM` | float64 | 2pt Makes (Pull Ups) |
| `Pull Ups - 2 FG_PCT` | float64 | 2pt % (Pull Ups) |
| `Pull Ups - 3 FGA` | float64 | 3pt Attempts (Pull Ups) |
| `Pull Ups - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Pull Ups) |
| `Pull Ups - 3 FGM` | float64 | 3pt Makes (Pull Ups) |
| `Pull Ups - 3 FG_PCT` | float64 | 3pt % (Pull Ups) |
| `Pull Ups - FGA` | float64 | Total Attempts (Pull Ups) |
| `Pull Ups - FGA_FREQ` | float64 | Frequency of Total Attempts (Pull Ups) |
| `Pull Ups - FGM` | float64 | Total Makes (Pull Ups) |
| `Pull Ups - FG_PCT` | float64 | Total % (Pull Ups) |
| `Touch 2-6 Seconds - 2 FGA` | float64 | 2pt Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - 2 FGM` | float64 | 2pt Makes (Touch 2-6s) |
| `Touch 2-6 Seconds - 2 FG_PCT` | float64 | 2pt % (Touch 2-6s) |
| `Touch 2-6 Seconds - 3 FGA` | float64 | 3pt Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - 3 FGM` | float64 | 3pt Makes (Touch 2-6s) |
| `Touch 2-6 Seconds - 3 FG_PCT` | float64 | 3pt % (Touch 2-6s) |
| `Touch 2-6 Seconds - FGA` | float64 | Total Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - FGA_FREQ` | float64 | Frequency of Total Attempts (Touch 2-6s) |
| `Touch 2-6 Seconds - FGM` | float64 | Total Makes (Touch 2-6s) |
| `Touch 2-6 Seconds - FG_PCT` | float64 | Total % (Touch 2-6s) |
| `Touch 6+ Seconds - 2 FGA` | float64 | 2pt Attempts (Touch 6s+) |
| `Touch 6+ Seconds - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Touch 6s+) |
| `Touch 6+ Seconds - 2 FGM` | float64 | 2pt Makes (Touch 6s+) |
| `Touch 6+ Seconds - 2 FG_PCT` | float64 | 2pt % (Touch 6s+) |
| `Touch 6+ Seconds - 3 FGA` | float64 | 3pt Attempts (Touch 6s+) |
| `Touch 6+ Seconds - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Touch 6s+) |
| `Touch 6+ Seconds - 3 FGM` | float64 | 3pt Makes (Touch 6s+) |
| `Touch 6+ Seconds - 3 FG_PCT` | float64 | 3pt % (Touch 6s+) |
| `Touch 6+ Seconds - FGA` | float64 | Total Attempts (Touch 6s+) |
| `Touch 6+ Seconds - FGA_FREQ` | float64 | Frequency of Total Attempts (Touch 6s+) |
| `Touch 6+ Seconds - FGM` | float64 | Total Makes (Touch 6s+) |
| `Touch 6+ Seconds - FG_PCT` | float64 | Total % (Touch 6s+) |
| `Touch < 2 Seconds - 2 FGA` | float64 | 2pt Attempts (Touch <2s) |
| `Touch < 2 Seconds - 2 FGA_FREQ` | float64 | Frequency of 2pt Attempts (Touch <2s) |
| `Touch < 2 Seconds - 2 FGM` | float64 | 2pt Makes (Touch <2s) |
| `Touch < 2 Seconds - 2 FG_PCT` | float64 | 2pt % (Touch <2s) |
| `Touch < 2 Seconds - 3 FGA` | float64 | 3pt Attempts (Touch <2s) |
| `Touch < 2 Seconds - 3 FGA_FREQ` | float64 | Frequency of 3pt Attempts (Touch <2s) |
| `Touch < 2 Seconds - 3 FGM` | float64 | 3pt Makes (Touch <2s) |
| `Touch < 2 Seconds - 3 FG_PCT` | float64 | 3pt % (Touch <2s) |
| `Touch < 2 Seconds - FGA` | float64 | Total Attempts (Touch <2s) |
| `Touch < 2 Seconds - FGA_FREQ` | float64 | Frequency of Total Attempts (Touch <2s) |
| `Touch < 2 Seconds - FGM` | float64 | Total Makes (Touch <2s) |
| `Touch < 2 Seconds - FG_PCT` | float64 | Total % (Touch <2s) |

---

## 3. Synergy Play Types
**File Name:** `full_synergy_stats.csv`

### Human-Readable Glossary
Tracks efficiency across specific basketball play types.
* **Play Types:** `Isolation`, `Transition`, `PNR Handler`, `PNR Roll Man`, `Post Up`, `Spot Up`, `Handoff`, `Cut`, `OffScreen`, `Putbacks`.
* **Metrics:**
    * **PPP:** Points Per Possession (Main efficiency metric).
    * **PERCENTILE:** League rank (0-100).
    * **FREQ:** Frequency of this play type.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `Isolation_PERCENTILE` | float64 | Percentile Rank: Isolation |
| `Isolation_GP` | int64 | Games Played: Isolation |
| `Isolation_FREQ` | float64 | Frequency: Isolation |
| `Isolation_PPP` | float64 | Points Per Possession: Isolation |
| `Isolation_FG_PCT` | float64 | FG%: Isolation |
| `Isolation_FT_FREQ` | float64 | Free Throw Freq: Isolation |
| `Isolation_TOV_FREQ` | float64 | Turnover Freq: Isolation |
| `Isolation_SF_FREQ` | float64 | Shooting Foul Freq: Isolation |
| `Isolation_AND1_FREQ` | float64 | And-1 Freq: Isolation |
| `Isolation_SCORE_FREQ` | float64 | Score Freq: Isolation |
| `Isolation_EFG_PCT` | float64 | Effective FG%: Isolation |
| `Isolation_POSS` | float64 | Total Possessions: Isolation |
| `Isolation_PTS` | float64 | Total Points: Isolation |
| `Isolation_FGM` | float64 | Total FGM: Isolation |
| `Isolation_FGA` | float64 | Total FGA: Isolation |
| `Transition_PERCENTILE` | float64 | Percentile Rank: Transition |
| `Transition_GP` | int64 | Games Played: Transition |
| `Transition_FREQ` | float64 | Frequency: Transition |
| `Transition_PPP` | float64 | Points Per Possession: Transition |
| `Transition_FG_PCT` | float64 | FG%: Transition |
| `Transition_FT_FREQ` | float64 | Free Throw Freq: Transition |
| `Transition_TOV_FREQ` | float64 | Turnover Freq: Transition |
| `Transition_SF_FREQ` | float64 | Shooting Foul Freq: Transition |
| `Transition_AND1_FREQ` | float64 | And-1 Freq: Transition |
| `Transition_SCORE_FREQ` | float64 | Score Freq: Transition |
| `Transition_EFG_PCT` | float64 | Effective FG%: Transition |
| `Transition_POSS` | float64 | Total Possessions: Transition |
| `Transition_PTS` | float64 | Total Points: Transition |
| `Transition_FGM` | float64 | Total FGM: Transition |
| `Transition_FGA` | float64 | Total FGA: Transition |
| `PNR_Handler_PERCENTILE` | float64 | Percentile Rank: PNR Handler |
| `PNR_Handler_GP` | int64 | Games Played: PNR Handler |
| `PNR_Handler_FREQ` | float64 | Frequency: PNR Handler |
| `PNR_Handler_PPP` | float64 | Points Per Possession: PNR Handler |
| `PNR_Handler_FG_PCT` | float64 | FG%: PNR Handler |
| `PNR_Handler_FT_FREQ` | float64 | Free Throw Freq: PNR Handler |
| `PNR_Handler_TOV_FREQ` | float64 | Turnover Freq: PNR Handler |
| `PNR_Handler_SF_FREQ` | float64 | Shooting Foul Freq: PNR Handler |
| `PNR_Handler_AND1_FREQ` | float64 | And-1 Freq: PNR Handler |
| `PNR_Handler_SCORE_FREQ` | float64 | Score Freq: PNR Handler |
| `PNR_Handler_EFG_PCT` | float64 | Effective FG%: PNR Handler |
| `PNR_Handler_POSS` | float64 | Total Possessions: PNR Handler |
| `PNR_Handler_PTS` | float64 | Total Points: PNR Handler |
| `PNR_Handler_FGM` | float64 | Total FGM: PNR Handler |
| `PNR_Handler_FGA` | float64 | Total FGA: PNR Handler |
| `PNR_Roll_PERCENTILE` | float64 | Percentile Rank: PNR Roll Man |
| `PNR_Roll_GP` | int64 | Games Played: PNR Roll Man |
| `PNR_Roll_FREQ` | float64 | Frequency: PNR Roll Man |
| `PNR_Roll_PPP` | float64 | Points Per Possession: PNR Roll Man |
| `PNR_Roll_FG_PCT` | float64 | FG%: PNR Roll Man |
| `PNR_Roll_FT_FREQ` | float64 | Free Throw Freq: PNR Roll Man |
| `PNR_Roll_TOV_FREQ` | float64 | Turnover Freq: PNR Roll Man |
| `PNR_Roll_SF_FREQ` | float64 | Shooting Foul Freq: PNR Roll Man |
| `PNR_Roll_AND1_FREQ` | float64 | And-1 Freq: PNR Roll Man |
| `PNR_Roll_SCORE_FREQ` | float64 | Score Freq: PNR Roll Man |
| `PNR_Roll_EFG_PCT` | float64 | Effective FG%: PNR Roll Man |
| `PNR_Roll_POSS` | float64 | Total Possessions: PNR Roll Man |
| `PNR_Roll_PTS` | float64 | Total Points: PNR Roll Man |
| `PNR_Roll_FGM` | float64 | Total FGM: PNR Roll Man |
| `PNR_Roll_FGA` | float64 | Total FGA: PNR Roll Man |
| `Post_Up_PERCENTILE` | float64 | Percentile Rank: Post Up |
| `Post_Up_GP` | int64 | Games Played: Post Up |
| `Post_Up_FREQ` | float64 | Frequency: Post Up |
| `Post_Up_PPP` | float64 | Points Per Possession: Post Up |
| `Post_Up_FG_PCT` | float64 | FG%: Post Up |
| `Post_Up_FT_FREQ` | float64 | Free Throw Freq: Post Up |
| `Post_Up_TOV_FREQ` | float64 | Turnover Freq: Post Up |
| `Post_Up_SF_FREQ` | float64 | Shooting Foul Freq: Post Up |
| `Post_Up_AND1_FREQ` | float64 | And-1 Freq: Post Up |
| `Post_Up_SCORE_FREQ` | float64 | Score Freq: Post Up |
| `Post_Up_EFG_PCT` | float64 | Effective FG%: Post Up |
| `Post_Up_POSS` | float64 | Total Possessions: Post Up |
| `Post_Up_PTS` | float64 | Total Points: Post Up |
| `Post_Up_FGM` | float64 | Total FGM: Post Up |
| `Post_Up_FGA` | float64 | Total FGA: Post Up |
| `Spot_Up_PERCENTILE` | float64 | Percentile Rank: Spot Up |
| `Spot_Up_GP` | int64 | Games Played: Spot Up |
| `Spot_Up_FREQ` | float64 | Frequency: Spot Up |
| `Spot_Up_PPP` | float64 | Points Per Possession: Spot Up |
| `Spot_Up_FG_PCT` | float64 | FG%: Spot Up |
| `Spot_Up_FT_FREQ` | float64 | Free Throw Freq: Spot Up |
| `Spot_Up_TOV_FREQ` | float64 | Turnover Freq: Spot Up |
| `Spot_Up_SF_FREQ` | float64 | Shooting Foul Freq: Spot Up |
| `Spot_Up_AND1_FREQ` | float64 | And-1 Freq: Spot Up |
| `Spot_Up_SCORE_FREQ` | float64 | Score Freq: Spot Up |
| `Spot_Up_EFG_PCT` | float64 | Effective FG%: Spot Up |
| `Spot_Up_POSS` | float64 | Total Possessions: Spot Up |
| `Spot_Up_PTS` | float64 | Total Points: Spot Up |
| `Spot_Up_FGM` | float64 | Total FGM: Spot Up |
| `Spot_Up_FGA` | float64 | Total FGA: Spot Up |
| `Handoff_PERCENTILE` | float64 | Percentile Rank: Handoff |
| `Handoff_GP` | int64 | Games Played: Handoff |
| `Handoff_FREQ` | float64 | Frequency: Handoff |
| `Handoff_PPP` | float64 | Points Per Possession: Handoff |
| `Handoff_FG_PCT` | float64 | FG%: Handoff |
| `Handoff_FT_FREQ` | float64 | Free Throw Freq: Handoff |
| `Handoff_TOV_FREQ` | float64 | Turnover Freq: Handoff |
| `Handoff_SF_FREQ` | float64 | Shooting Foul Freq: Handoff |
| `Handoff_AND1_FREQ` | float64 | And-1 Freq: Handoff |
| `Handoff_SCORE_FREQ` | float64 | Score Freq: Handoff |
| `Handoff_EFG_PCT` | float64 | Effective FG%: Handoff |
| `Handoff_POSS` | float64 | Total Possessions: Handoff |
| `Handoff_PTS` | float64 | Total Points: Handoff |
| `Handoff_FGM` | float64 | Total FGM: Handoff |
| `Handoff_FGA` | float64 | Total FGA: Handoff |
| `Cut_PERCENTILE` | float64 | Percentile Rank: Cut |
| `Cut_GP` | int64 | Games Played: Cut |
| `Cut_FREQ` | float64 | Frequency: Cut |
| `Cut_PPP` | float64 | Points Per Possession: Cut |
| `Cut_FG_PCT` | float64 | FG%: Cut |
| `Cut_FT_FREQ` | float64 | Free Throw Freq: Cut |
| `Cut_TOV_FREQ` | float64 | Turnover Freq: Cut |
| `Cut_SF_FREQ` | float64 | Shooting Foul Freq: Cut |
| `Cut_AND1_FREQ` | float64 | And-1 Freq: Cut |
| `Cut_SCORE_FREQ` | float64 | Score Freq: Cut |
| `Cut_EFG_PCT` | float64 | Effective FG%: Cut |
| `Cut_POSS` | float64 | Total Possessions: Cut |
| `Cut_PTS` | float64 | Total Points: Cut |
| `Cut_FGM` | float64 | Total FGM: Cut |
| `Cut_FGA` | float64 | Total FGA: Cut |
| `OffScreen_PERCENTILE` | float64 | Percentile Rank: Off Screen |
| `OffScreen_GP` | int64 | Games Played: Off Screen |
| `OffScreen_FREQ` | float64 | Frequency: Off Screen |
| `OffScreen_PPP` | float64 | Points Per Possession: Off Screen |
| `OffScreen_FG_PCT` | float64 | FG%: Off Screen |
| `OffScreen_FT_FREQ` | float64 | Free Throw Freq: Off Screen |
| `OffScreen_TOV_FREQ` | float64 | Turnover Freq: Off Screen |
| `OffScreen_SF_FREQ` | float64 | Shooting Foul Freq: Off Screen |
| `OffScreen_AND1_FREQ` | float64 | And-1 Freq: Off Screen |
| `OffScreen_SCORE_FREQ` | float64 | Score Freq: Off Screen |
| `OffScreen_EFG_PCT` | float64 | Effective FG%: Off Screen |
| `OffScreen_POSS` | float64 | Total Possessions: Off Screen |
| `OffScreen_PTS` | float64 | Total Points: Off Screen |
| `OffScreen_FGM` | float64 | Total FGM: Off Screen |
| `OffScreen_FGA` | float64 | Total FGA: Off Screen |
| `Putbacks_PERCENTILE` | float64 | Percentile Rank: Putbacks |
| `Putbacks_GP` | int64 | Games Played: Putbacks |
| `Putbacks_FREQ` | float64 | Frequency: Putbacks |
| `Putbacks_PPP` | float64 | Points Per Possession: Putbacks |
| `Putbacks_FG_PCT` | float64 | FG%: Putbacks |
| `Putbacks_FT_FREQ` | float64 | Free Throw Freq: Putbacks |
| `Putbacks_TOV_FREQ` | float64 | Turnover Freq: Putbacks |
| `Putbacks_SF_FREQ` | float64 | Shooting Foul Freq: Putbacks |
| `Putbacks_AND1_FREQ` | float64 | And-1 Freq: Putbacks |
| `Putbacks_SCORE_FREQ` | float64 | Score Freq: Putbacks |
| `Putbacks_EFG_PCT` | float64 | Effective FG%: Putbacks |
| `Putbacks_POSS` | float64 | Total Possessions: Putbacks |
| `Putbacks_PTS` | float64 | Total Points: Putbacks |
| `Putbacks_FGM` | float64 | Total FGM: Putbacks |
| `Putbacks_FGA` | float64 | Total FGA: Putbacks |

---

## 4. Rebounding Contexts
**File Name:** `full_players_rebound_aggregated.csv`

### Human-Readable Glossary
Tracks rebounding performance in different situations (contested vs. uncontested, distance from hoop).
* **Contexts:**
    * **Contest Level:** `0 Contesting` (Uncontested), `1 Contesting`, `2+ Contesting`.
    * **Distance:** `0-3 Feet` (Close), `3-6 Feet`, `6-10 Feet`, `10+ Feet` (Long rebounds).
* **Metrics:**
    * **DREB:** Defensive Rebounds.
    * **OREB:** Offensive Rebounds.
    * **REB_FREQ:** % of total rebounds grabbed in this specific context.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `TEAM_ID` | float64 | Identifier |
| `0 Contesting Rebounders - DREB` | float64 | Uncontested Defensive Rebounds |
| `0 Contesting Rebounders - OREB` | float64 | Uncontested Offensive Rebounds |
| `0 Contesting Rebounders - REB` | float64 | Uncontested Total Rebounds |
| `0 Contesting Rebounders - REB_FREQ` | float64 | Uncontested Rebound Frequency |
| `0-3 Feet - DREB` | float64 | Defensive Rebounds (0-3ft) |
| `0-3 Feet - OREB` | float64 | Offensive Rebounds (0-3ft) |
| `0-3 Feet - REB` | float64 | Total Rebounds (0-3ft) |
| `0-3 Feet - REB_FREQ` | float64 | Rebound Frequency (0-3ft) |
| `1 Contesting Rebounder - DREB` | float64 | Defensive Rebounds (1 Contestor) |
| `1 Contesting Rebounder - OREB` | float64 | Offensive Rebounds (1 Contestor) |
| `1 Contesting Rebounder - REB` | float64 | Total Rebounds (1 Contestor) |
| `1 Contesting Rebounder - REB_FREQ` | float64 | Rebound Frequency (1 Contestor) |
| `10+ Feet - DREB` | float64 | Defensive Rebounds (10+ft) |
| `10+ Feet - OREB` | float64 | Offensive Rebounds (10+ft) |
| `10+ Feet - REB` | float64 | Total Rebounds (10+ft) |
| `10+ Feet - REB_FREQ` | float64 | Rebound Frequency (10+ft) |
| `2+ Contesting Rebounders - DREB` | float64 | Defensive Rebounds (2+ Contestors) |
| `2+ Contesting Rebounders - OREB` | float64 | Offensive Rebounds (2+ Contestors) |
| `2+ Contesting Rebounders - REB` | float64 | Total Rebounds (2+ Contestors) |
| `2+ Contesting Rebounders - REB_FREQ` | float64 | Rebound Frequency (2+ Contestors) |
| `3-6 Feet - DREB` | float64 | Defensive Rebounds (3-6ft) |
| `3-6 Feet - OREB` | float64 | Offensive Rebounds (3-6ft) |
| `3-6 Feet - REB` | float64 | Total Rebounds (3-6ft) |
| `3-6 Feet - REB_FREQ` | float64 | Rebound Frequency (3-6ft) |
| `6-10 Feet - DREB` | float64 | Defensive Rebounds (6-10ft) |
| `6-10 Feet - OREB` | float64 | Offensive Rebounds (6-10ft) |
| `6-10 Feet - REB` | float64 | Total Rebounds (6-10ft) |
| `6-10 Feet - REB_FREQ` | float64 | Rebound Frequency (6-10ft) |
| `OVERALL - DREB` | float64 | Total Defensive Rebounds |
| `OVERALL - OREB` | float64 | Total Offensive Rebounds |
| `OVERALL - REB` | float64 | Total Rebounds |
| `OVERALL - REB_FREQ` | float64 | Total Rebound Frequency |

---

## 5. Defense (Overall)
**File Name:** `full_players_defense_Overall.csv`

### Human-Readable Glossary
Tracks how well a player defends shots overall.
* **D_FG_PCT:** Opponent shooting % vs this player.
* **NORMAL_FG_PCT:** Opponent's expected shooting %.
* **PCT_PLUSMINUS:** The difference. (Negative = Good Defense).

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `FREQ` | float64 | Frequency of defensive possessions |
| `D_FGM` | float64 | Opponent FGM (Defended) |
| `D_FGA` | float64 | Opponent FGA (Defended) |
| `D_FG_PCT` | float64 | Opponent FG% (Defended) |
| `NORMAL_FG_PCT` | float64 | Opponent Expected FG% |
| `PCT_PLUSMINUS` | float64 | Defensive Impact (Diff) |

---

## 6. Defense (2-Pointers)
**File Name:** `full_players_defense_2_Pointers.csv`

### Human-Readable Glossary
Tracks defensive impact specifically against 2-point shots.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `FREQ` | float64 | Frequency of defensive possessions |
| `D_FGM` | float64 | Opponent 2PM (Defended) |
| `D_FGA` | float64 | Opponent 2PA (Defended) |
| `D_FG_PCT` | float64 | Opponent 2P% (Defended) |
| `NORMAL_FG_PCT` | float64 | Opponent Expected 2P% |
| `PCT_PLUSMINUS` | float64 | Defensive Impact 2P (Diff) |

---

## 7. Defense (3-Pointers)
**File Name:** `full_players_defense_3_Pointers.csv`

### Human-Readable Glossary
Tracks defensive impact specifically against 3-point shots.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `SEASON` | object | Identifier |
| `FREQ` | float64 | Frequency of defensive possessions |
| `D_FGM` | float64 | Opponent 3PM (Defended) |
| `D_FGA` | float64 | Opponent 3PA (Defended) |
| `D_FG_PCT` | float64 | Opponent 3P% (Defended) |
| `NORMAL_FG_PCT` | float64 | Opponent Expected 3P% |
| `PCT_PLUSMINUS` | float64 | Defensive Impact 3P (Diff) |

---

## 8. Player Features & Box Score
**File Name:** `Updating_per_year_player_features_stats.csv`

### Human-Readable Glossary
Physical attributes and standard box score totals (Points, Rebounds, Assists, etc.) aggregated for the season.

### AI-Readable Schema
| Column Name | Data Type | Description |
|---|---|---|
| `PLAYER_ID` | int64 | Identifier |
| `PLAYER` | object | Identifier |
| `SEASON` | object | Identifier |
| `Height` | object | Player Height |
| `Weight` | float64 | Player Weight |
| `Position` | object | Player Position |
| `Draft Year` | object | Draft Year |
| `GP` | int64 | Games Played |
| `MIN` | float64 | Total Minutes |
| `AST` | int64 | Total Assists |
| `TOV` | int64 | Total Turnovers |
| `STL` | int64 | Total Steals |
| `BLK` | int64 | Total Blocks |
| `PF` | int64 | Total Personal Fouls |
| `PFD` | int64 | Total Fouls Drawn |
| `PTS` | int64 | Total Points |
| `PLUS_MINUS` | float64 | Total Plus/Minus |