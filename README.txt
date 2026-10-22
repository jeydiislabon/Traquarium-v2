================================================================================
         TRAQUARIUM v2 — DECISION SUPPORT SYSTEM FOR AQUATIC RETAIL FACILITIES
================================================================================

Version: 2.0.0
Python : 3.8+
Author : Eslabon, John Donald S.
Institution: Technological Institute of the Philippines — Quezon City
Course : CPE025A | CPE31S1A — Major (Capstone) Design Experience
Semester: 1st Semester, SY 2026–2027

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
volume needed to bring all tanks below the safe NH3 threshold.

All data is stored locally in a per-user SQLite database — no internet
connection or paid subscription is required.

================================================================================
SCIENCE BEHIND THE SYSTEM
================================================================================

UN-IONIZED AMMONIA EQUILIBRIUM (Emerson et al., 1975)
------------------------------------------------------
Total Ammonia Nitrogen (TAN) exists in two forms in water:
  • Ionised ammonium (NH4+) — non-toxic
  • Un-ionised ammonia (NH3) — highly toxic even at 0.02 mg/L

The fraction of TAN that is toxic NH3 depends on pH and temperature:

  pKa = 0.09018 + (2729.92 / (273.15 + T))
  f   = 1 / (1 + 10^(pKa − pH))
  NH3 = TAN × f

TOXICITY CLASSIFICATION
-----------------------
  Safe           : NH3 < 0.02 mg/L   — no immediate action required
  Caution        : 0.02 ≤ NH3 < 0.05 — perform 25–30% water change
  Critical Toxic : NH3 ≥ 0.05 mg/L   — emergency intervention required

PSO WATER CHANGE OPTIMIZATION
------------------------------
Particle Swarm Optimization finds the minimum total water volume to change
across all tanks while ensuring every tank drops below 0.02 mg/L NH3.

  Swarm size      : 30 particles
  Max iterations  : 200
  Inertia (w)     : 0.7
  Cognitive (c1)  : 1.5
  Social (c2)     : 1.5
  Dilution model  : NH3_after = NH3_before × (1 − c)

================================================================================
HOW TO USE THE PROGRAM
================================================================================

1. LOADING → LOGIN / REGISTER
   • Launch the app; a loading screen appears briefly
   • Create a new account or log in with existing credentials
   • Each user has a separate, isolated SQLite database

2. HOME DASHBOARD
   • Overview of total readings and profiles tracked
   • Stat cards showing latest pH, Temperature, and NH3
   • Quick bar chart of the most recent reading
   • Button to navigate to the Input page

3. INPUT PAGE
   • Enter a unique Tank / Profile name (e.g. "Main Tank", "Cichlid 1")
   • Enter the three required parameters from your test kit:
       - TAN  — Total Ammonia Nitrogen (0–10 mg/L)
       - pH   — Water pH (6.0–9.0)
       - Temp — Water temperature (15–35 °C)
   • Optionally log kH and gH (for historical records, no effect on NH3)
   • Click "Save Reading" or press Enter
   • The system displays the computed NH3, toxicity level, and inference time

4. HISTORY PAGE
   • View all readings in a table with columns:
       Timestamp | Tank Name | TAN | pH | Temp | NH3 | Toxicity
   • Rows are colour-coded: green (Safe), amber (Caution), red (Critical)
   • Click any row → click "Show Details" to see dosing instructions and
     parameter warnings for the selected tank
   • Search by tank name, edit (TAN/pH/Temp recalculates NH3 on save),
     or delete individual readings

5. GRAPH PAGE
   • Select a tank from the History page to visualise its readings
   • Grouped bar chart: TAN (light blue), pH (cyan), Temp (amber), NH3 (red)
   • Info box shows the latest reading and toxicity classification

================================================================================
KEYBOARD SHORTCUTS
================================================================================

  Ctrl + H    Go to Home page
  Ctrl + 1    Go to Input page
  Ctrl + 2    Go to History page
  Ctrl + 3    Go to Graph page
  F11         Toggle fullscreen
  Ctrl + Q    Exit application
  F1          Show keyboard shortcuts help
  Ctrl + I    About Traquarium

================================================================================
GETTING STARTED
================================================================================

PREREQUISITES
-------------
  Python 3.8 or higher

INSTALLATION
------------
  pip install PyQt6 pyqtgraph numpy

RUN
---
  python main.py

FIRST TIME SETUP
----------------
  1. Launch — loading screen appears
  2. Click "Sign Up", enter a username and password
  3. Log in and go to Input page
  4. Enter TAN, pH, and Temperature from your test kit
  5. Click "Save Reading" — NH3 and toxicity are computed and stored instantly

================================================================================
PROJECT STRUCTURE
================================================================================

  main.py              — Entry point (QApplication initialisation)
  main_app.py          — MainWindow, page stack, navigation, session lifecycle
  ammonia_engine.py    — Emerson (1975) NH3 equilibrium calculation engine
  pso_engine.py        — Kennedy & Eberhart (1995) PSO optimisation engine
  data_model.py        — SQLite CRUD layer (ReadingManager, WaterReading)
  auth/
    user_manager.py    — User registration and credential validation
  pages/
    loading_page.py    — Animated loading / splash screen
    login_page.py      — Login form
    register_page.py   — Registration form
    welcome_page.py    — Post-login welcome screen
    home_page.py       — Dashboard with stats and latest-reading chart
    input_page.py      — Parameter input form (TAN, pH, Temp, kH, gH)
    history_page.py    — Reading table with edit, delete, dosing details
    graph_page.py      — Per-tank bar chart visualisation
  ui/
    base_page.py       — AquaPage base class (header, nav bar, shortcuts)
    components.py      — ButtonFactory, InputFieldFactory, FrameFactory, etc.
    styles.py          — Qt stylesheet strings
    helpers.py         — ValidationHelper, WarningHelper, DataHelper, etc.
    constants.py       — Font and colour tokens
    animations.py      — Hover animations
    dialogs.py         — About dialog
    utils.py           — Asset path resolution

================================================================================
DATABASE SCHEMA
================================================================================

  File location: users/<username>/readings.db  (SQLite)

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

  Python 3.8+   — Core language
  PyQt6 ≥6.4    — Cross-platform GUI framework
  PyQtGraph ≥0.13 — Scientific bar chart rendering
  NumPy ≥1.24   — Array operations for PSO and graphing
  sqlite3       — Stdlib embedded relational database
  math          — pKa equilibrium formula (math.pow)
  random        — PSO stochastic particle initialisation
  time          — Inference time measurement (time.perf_counter)

================================================================================
SYSTEM REQUIREMENTS
================================================================================

  Processor  : Intel/AMD x86-64
  RAM        : 4 GB minimum (typical peak usage < 150 MB)
  Disk       : 100 MB free
  Display    : 1050 × 750 or higher
  OS         : Windows, macOS, or Linux
  Python     : 3.8 or higher

================================================================================
REFERENCES
================================================================================

  Emerson, K., Russo, R. C., Lund, R. E., & Thurston, R. V. (1975).
    Aqueous ammonia equilibrium calculations: Effect of pH and temperature.
    Journal of the Fisheries Research Board of Canada, 32(12), 2379–2383.

  Kennedy, J., & Eberhart, R. (1995).
    Particle swarm optimization.
    Proceedings of ICNN'95, 4, 1942–1948.

================================================================================
VERSION HISTORY
================================================================================

  v2.0.0 (2026)
    - Replaced raw ammonia input with TAN-based NH3 equilibrium engine
      (Emerson et al., 1975 — pKa thermodynamic model)
    - Added AmmoniaEngine: pKa → NH3 fraction → NH3 mg/L → toxicity classification
    - Added PSOEngine: multi-tank minimal water change optimisation
    - Migrated data storage from JSON flat files to SQLite (ACID-compliant)
    - Added NH3 and Toxicity columns to History table (colour-coded rows)
    - Input page: TAN field replaces direct ammonia; optional kH/gH logging
    - Dosing instructions panel in History dropdown
    - Graph page: now plots TAN, pH, Temp, and NH3 per tank
    - All edit operations recalculate NH3 and toxicity on save
    - Validation ranges updated to Emerson model bounds
      (pH 6.0–9.0, Temp 15–35 °C)

  v1.0.0 (2025)
    - Initial release (team prototype)
    - Basic pH, Temperature, Ammonia logging with JSON storage

================================================================================
© 2026 John Donald S. Eslabon — Technological Institute of the Philippines
================================================================================
