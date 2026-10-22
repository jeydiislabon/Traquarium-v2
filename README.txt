================================================================================
                    TRAQUARIUM - AQUARIUM WATER QUALITY MONITOR
================================================================================

Version: 1.0.0
Python: 3.8+
Developed by: Traquarium Team

================================================================================
ABOUT TRAQUARIUM
================================================================================

Traquarium is a desktop application designed to help aquarium owners monitor 
and track water quality parameters. The program allows users to record pH 
levels, temperature, and ammonia concentrations over time, providing visual 
analysis and automated warnings when parameters fall outside safe ranges.

================================================================================
HOW TO USE THE PROGRAM
================================================================================

1. HOME DASHBOARD
-----------------
• Displays overview of your latest water readings
• Shows circular stat cards for pH, temperature, and ammonia
• Includes a bar graph visualization of your most recent test
• Quick access to add new readings

2. INPUT PAGE
-------------
• Enter a profile name for your aquarium (e.g., "Main Tank", "Betta Tank")
• Input three water parameters: pH (0-14), Temperature (0-40°C), Ammonia (0-10 ppm)
• Built-in parameter guide on the right side explains ideal ranges
• Strict validation prevents invalid values from being saved
• Press Enter or click "Save Reading" to store your data

3. HISTORY PAGE
---------------
• View all saved readings in a searchable table
• Search by profile name to filter specific aquariums
• Click any row to see detailed warnings and suggestions
• Edit mode allows you to correct past readings
• Delete unwanted entries
• Color-coded warnings: Green (safe), Yellow (caution), Red (danger)

4. GRAPH PAGE
-------------
• Select a profile from History page first
• Visualize all readings for that profile as bar graphs
  - Blue bars = pH levels
  - Orange bars = Temperature
  - Red bars = Ammonia levels
• Info box shows latest reading details
• Perfect for spotting trends and tracking improvements

================================================================================
KEY FEATURES
================================================================================

• Multi-Profile Support - Track multiple aquariums separately with named profiles
• Automatic Safety Warnings - Color-coded alerts when parameters are unsafe
• Interactive Data Visualization - Bar graphs show trends across all readings
• Complete History Management - Search, edit, and delete past readings
• Real-time Input Validation - Prevents invalid data entry with strict checks
• Built-in Parameter Guide - Reference information for ideal water ranges
• Multi-user Support - Each user has separate, secure data storage
• Data Persistence - All readings saved locally in JSON format
• Keyboard Shortcuts - Quick navigation (Ctrl+H, Ctrl+1/2/3, F11)
• Offline Operation - No internet connection required

================================================================================
GETTING STARTED
================================================================================

PREREQUISITES
-------------
• Python 3.8 or higher
• pip package manager

INSTALLATION
------------
1. Install required dependencies:
   pip install -r requirements.txt

   Or manually install:
   pip install PyQt6 pyqtgraph numpy

2. Run the application:
   python main.py

FIRST TIME SETUP
----------------
1. Launch the application - You'll see a loading screen
2. Create an account - Click "Sign Up" and enter your credentials
3. Login - Use your username and password to access the dashboard
4. Add your first reading - Navigate to the Input page and enter water parameters

================================================================================
KEYBOARD SHORTCUTS
================================================================================

  Ctrl + H    Go to Home page
  Ctrl + 1    Go to Input page
  Ctrl + 2    Go to History page
  Ctrl + 3    Go to Graph page
  F11         Toggle fullscreen mode
  Ctrl + Q    Exit application
  F1          Show keyboard shortcuts help
  Ctrl + I    Show About dialog

================================================================================
WATER PARAMETER GUIDE
================================================================================

pH LEVEL (IDEAL: 6.5 - 8.0)
----------------------------
What it measures: Water acidity/alkalinity
Why it matters: Affects fish health, metabolism, and stress levels
Freshwater fish: 6.5-7.5
Marine aquariums: 8.0-8.4

Troubleshooting:
  - Too low? Add pH buffer or reduce CO2
  - Too high? Perform partial water change

TEMPERATURE (IDEAL: 20-28°C / 68-82°F)
---------------------------------------
What it measures: Water temperature
Why it matters: Critical for fish metabolism and immune function
Tropical fish: 24-28°C
Coldwater fish: 18-22°C

Troubleshooting:
  - Too low? Increase heater temperature
  - Too high? Improve ventilation or add cooling

AMMONIA (IDEAL: 0-0.5 PPM)
---------------------------
What it measures: Toxic ammonia concentration
Why it matters: Highly toxic to fish even in small amounts
Established tanks: Should be 0 ppm
New tanks: May spike during cycling

Troubleshooting:
  - >0.5 ppm? URGENT - Immediate water change required
  - 0.2-0.5 ppm? Check filter, reduce feeding

================================================================================
TECHNICAL INFORMATION
================================================================================

TECHNOLOGY STACK
----------------
• Python 3.x - Core programming language for application logic
• PyQt6 - Cross-platform GUI framework for desktop applications
• PyQtGraph - Scientific graphics and data visualization library
• JSON - Lightweight data-interchange format for persistent storage
• NumPy - Numerical computing library for data processing

DATA STORAGE
------------
• All user data is stored locally on your computer
• Each user has a separate folder in the "users" directory
• Readings are saved in JSON format for easy portability
• No internet connection required - fully offline application
• Your data remains private and secure on your device

SYSTEM REQUIREMENTS
-------------------
• Python 3.8 or higher
• Windows, macOS, or Linux operating system
• Minimum 100MB free disk space
• Screen resolution: 1050x750 or higher recommended

================================================================================
DEVELOPMENT TEAM
================================================================================

Developed by the Traquarium Team:
• Arindaeng, Paul Daniel - Assistant Programmer
• Dela Cruz, Gabriel - Designer
• Eslabon, John Donald - Lead Programmer
• Garcia, Rain - Co-Lead Programmer

PROJECT PURPOSE
---------------
This application was developed to address the practical challenge of tracking 
aquarium water quality over time. Traditional manual record-keeping is prone 
to errors and lacks analytical capabilities. Traquarium provides an automated, 
user-friendly solution with data visualization and intelligent warning systems.

================================================================================
TROUBLESHOOTING
================================================================================

PROBLEM: Application won't start
SOLUTION: Make sure all dependencies are installed
  pip install PyQt6 pyqtgraph numpy

PROBLEM: "Python is not recognized" error
SOLUTION: Install Python and add it to PATH
  Download from: https://www.python.org/downloads/

PROBLEM: Window appears then closes immediately
SOLUTION: Run from terminal to see error messages
  python main.py

PROBLEM: Cannot edit values in History page
SOLUTION: Click "Edit" button first, then double-click the cell

================================================================================
VERSION HISTORY
================================================================================

v1.0.0 (2025)
  - Initial release
  - Core water parameter tracking (pH, temperature, ammonia)
  - Multi-user support
  - Data visualization with graphs
  - Warning system
  - Modern UI with dark theme

FUTURE ENHANCEMENTS
-------------------
  - CSV/Excel export functionality for external data analysis
  - Extended parameter monitoring (nitrite, nitrate, GH, KH)
  - Automated notification system for scheduled testing
  - Cloud-based data synchronization
  - Mobile application development for cross-platform accessibility

================================================================================

Developed by the Traquarium Team
© 2025 Traquarium Team

This application demonstrates the practical application of software engineering 
principles and serves as a comprehensive solution for aquarium water quality 
monitoring.

================================================================================
