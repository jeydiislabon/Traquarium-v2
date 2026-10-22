================================================================================
     TRAQUARIUM v2 -- DECISION SUPPORT SYSTEM FOR AQUATIC RETAIL FACILITIES
================================================================================

Version   : 2.0.0
Python    : 3.8+
Author    : Eslabon, John Donald S.
Institution: Technological Institute of the Philippines -- Quezon City
Course    : CPE025A | CPE31S1A -- Major (Capstone) Design Experience
Semester  : 1st Semester, SY 2026-2027

================================================================================
COLOR PALETTE (Aquarium-Inspired, DMC thread palette)
================================================================================

  DMC 336  Navy Blue            #1A2472   Deep backgrounds, sidebar base
  DMC 797  Royal Blue           #2255A4   Panel fills, card surfaces
  DMC 3837 Ultra Dark Lavender  #673888   Accents, borders, selected states
  DMC 3607 Light Plum           #C06090   Hover states, secondary accents
  DMC 600  Very Dark Cranberry  #B01040   Primary buttons, badges, danger
  DMC 150  Ultra Dark Dusty Rose #8B1A3A  Pressed states, deep accents

================================================================================
ABOUT TRAQUARIUM
================================================================================

Traquarium is an offline desktop decision support system for small-scale
freshwater aquatic retail facilities. It accepts manual water parameter
measurements (TAN, pH, Temperature) from standard liquid or colorimetric
test kits, computes the toxic un-ionized ammonia (NH3) concentration using
the Emerson et al. (1975) thermodynamic equilibrium model, classifies the
toxicity level, and generates step-by-step chemical dosing instructions.

For multi-tank facilities, the Particle Swarm Optimization (PSO) engine
(Kennedy & Eberhart, 1995) computes the minimal combined water change
volume needed to bring all tanks below the safe NH3 threshold of 0.02 mg/L.

All data is stored locally in a per-user SQLite database. No internet
connection or paid subscription is required.

================================================================================
SCIENCE BEHIND THE SYSTEM
================================================================================

UN-IONIZED AMMONIA EQUILIBRIUM (Emerson et al., 1975)
------------------------------------------------------
Total Ammonia Nitrogen (TAN) exists in two forms in water:
  - Ionised ammonium (NH4+) -- non-toxic
  - Un-ionised ammonia (NH3) -- highly toxic even at 0.02 mg/L

  pKa = 0.09018 + (2729.92 / (273.15 + T))
  f   = 1 / (1 + 10^(pKa - pH))
  NH3 = TAN x f

TOXICITY CLASSIFICATION
-----------------------
  Safe           : NH3 < 0.02 mg/L  -- no immediate action required
  Caution        : 0.02 to 0.05 mg/L -- perform 25-30% water change
  Critical Toxic : NH3 >= 0.05 mg/L  -- emergency intervention required

PSO WATER CHANGE OPTIMIZATION
------------------------------
Particle Swarm Optimization finds the minimum total water volume to change
across all tanks while ensuring every tank drops below 0.02 mg/L NH3.

  Swarm size   : 30 particles
  Max iterations: 200
  Inertia (w)  : 0.7
  Cognitive (c1): 1.5
  Social (c2)  : 1.5
  Dilution model: NH3_after = NH3_before x (1 - c)

================================================================================
HOW TO USE THE PROGRAM
================================================================================

1. LOADING -> LOGIN / REGISTER
   - Launch app; loading screen with progress bar appears
   - Create a new account or log in with existing credentials
   - Each user has a separate, isolated SQLite database

2. HOME DASHBOARD
   - Summary strip: total readings, profiles tracked, last updated
   - Bar chart of the latest reading (TAN, pH, Temp, NH3)
   - Stat cards: pH, Temperature, NH3 (mg/L), Toxicity level

3. INPUT PAGE
   - Enter a unique Tank / Profile name (e.g. "Main Tank")
   - Enter the three required parameters from your test kit:
       TAN  -- Total Ammonia Nitrogen (0 to 10 mg/L)
       pH   -- Water pH (6.0 to 9.0)
       Temp -- Water temperature (15 to 35 deg C)
   - Click "Save Reading" -- the right panel shows the computation:
       pKa, NH3 fraction, NH3 (mg/L), toxicity level, inference time

4. HISTORY PAGE
   - Table with columns: Timestamp | Tank Name | TAN | pH | Temp | NH3 | Toxicity
   - Rows colour-coded: green (Safe), amber (Caution), red (Critical)
   - Click a row -> "Show Details" for dosing instructions and warnings
   - Edit (TAN/pH/Temp recalculates NH3 on save) or delete readings

5. GRAPH PAGE
   - Select a tank from History to visualise all its readings
   - Grouped bar chart: TAN (light blue), pH (cyan), Temp (amber), NH3 (red)
   - Info box shows latest reading and toxicity classification

================================================================================
KEYBOARD SHORTCUTS
================================================================================

  Ctrl + H    Go to Home
  Ctrl + 1    Go to Input
  Ctrl + 2    Go to History
  Ctrl + 3    Go to Graph
  F11         Toggle fullscreen
  Ctrl + Q    Exit
  F1          Keyboard shortcuts help
  Ctrl + I    About Traquarium

================================================================================
GETTING STARTED
================================================================================

  pip install PyQt6 pyqtgraph numpy
  python main.py

================================================================================
PROJECT STRUCTURE
================================================================================

  main.py              -- Entry point
  main_app.py          -- MainWindow, page stack, navigation, session
  ammonia_engine.py    -- Emerson (1975) NH3 equilibrium engine
  pso_engine.py        -- Kennedy & Eberhart (1995) PSO engine
  data_model.py        -- SQLite CRUD (ReadingManager, WaterReading)
  auth/user_manager.py -- User registration and login
  pages/
    loading_page.py    -- Animated loading screen
    login_page.py      -- SENSE-style split login (left brand + right form)
    register_page.py   -- Matching split registration page
    welcome_page.py    -- Post-login welcome screen
    home_page.py       -- Dashboard with stats, chart, nav sidebar
    input_page.py      -- TAN/pH/Temp form + live computation result panel
    history_page.py    -- Reading table with edit, delete, dosing details
    graph_page.py      -- Per-tank grouped bar chart
  ui/
    base_page.py       -- AquaPage base class (header, nav, shortcuts)
    components.py      -- ButtonFactory, InputFieldFactory, FrameFactory
    styles.py          -- All Qt stylesheets (aquarium palette)
    constants.py       -- Palette tokens, fonts
    helpers.py         -- Validators, warnings, painters
    dialogs.py         -- About dialog

================================================================================
DATABASE SCHEMA (users/<username>/readings.db)
================================================================================

  CREATE TABLE readings (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp   TEXT    NOT NULL,
      tank_name   TEXT    NOT NULL,
      tan         REAL    NOT NULL,   -- Total Ammonia Nitrogen (mg/L)
      ph          REAL    NOT NULL,
      temperature REAL    NOT NULL,
      nh3         REAL    NOT NULL,   -- Computed un-ionized NH3 (mg/L)
      toxicity    TEXT    NOT NULL,   -- Safe / Caution / Critical Toxic
      kh          REAL,               -- Carbonate Hardness (optional)
      gh          REAL                -- General Hardness   (optional)
  );

================================================================================
TECHNOLOGY STACK
================================================================================

  Python 3.8+     -- Core language
  PyQt6 >=6.4     -- GUI framework (widgets, layouts, signals)
  PyQtGraph >=0.13 -- Scientific bar chart rendering (BarGraphItem)
  NumPy >=1.24    -- Array ops for PSO and graphing
  sqlite3         -- Stdlib embedded ACID database
  math            -- pKa equilibrium (math.pow)
  random          -- PSO particle stochastic init
  time            -- Inference time (time.perf_counter)

================================================================================
SYSTEM REQUIREMENTS
================================================================================

  Processor : Intel/AMD x86-64
  RAM       : 4 GB minimum (typical peak < 150 MB)
  Disk      : 100 MB free
  Display   : 1050 x 750 or higher
  OS        : Windows, macOS, or Linux
  Python    : 3.8 or higher

================================================================================
REFERENCES
================================================================================

  Emerson, K., Russo, R. C., Lund, R. E., & Thurston, R. V. (1975).
    Aqueous ammonia equilibrium calculations: Effect of pH and temperature.
    Journal of the Fisheries Research Board of Canada, 32(12), 2379-2383.

  Kennedy, J., & Eberhart, R. (1995).
    Particle swarm optimization.
    Proceedings of ICNN'95, 4, 1942-1948.

================================================================================
VERSION HISTORY
================================================================================

  v2.0.0 (2026)
    - Aquarium-inspired color palette (Navy/Royal/Lavender/Plum/Cranberry)
    - SENSE-style split login and register pages
    - AmmoniaEngine: Emerson (1975) pKa -> NH3 equilibrium calculation
    - PSOEngine: multi-tank minimal water change optimization
    - SQLite migration (from JSON flat files)
    - Input page: TAN field + live computation result panel
    - History: 7-column table with toxicity colour-coded rows
    - Graph: 4-bar groups (TAN, pH, Temp, NH3) per tank
    - All emojis removed; clean ASCII text labels throughout
    - Validation ranges updated to Emerson model bounds (pH 6-9, T 15-35)

  v1.0.0 (2025)
    - Initial team prototype (JSON storage, raw ammonia input)

================================================================================
(c) 2026 John Donald S. Eslabon -- Technological Institute of the Philippines
================================================================================
