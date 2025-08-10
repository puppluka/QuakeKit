-------------------------------------------------------------------------------------------

 .88888.                     dP                dP     dP oo   dP   
d8'   `8b                    88                88   .d8'      88   
88     88  dP    dP .d8888b. 88  .dP  .d8888b. 88aaa8P'  dP d8888P 
88  db 88  88    88 88'  `88 88888"   88ooood8 88   `8b. 88   88   
Y8.  Y88P  88.  .88 88.  .88 88  `8b. 88.  ... 88     88 88   88   
 `8888PY8b `88888P' `88888P8 dP   `YP `88888P' dP     dP dP   dP   

-------------------------------------------------------------------------------------------

        by Aerox Software

-------------------------------------------------------------------------------------------

  === Project Structure: ===
    |
    | -- bin == Binary utility folder.
    | -- config == Configuration file data.
    | -- demos == In-Game demos.
    | -- endscreen == DOS Quit Screens
    | -- gfx-wad == assets for gfx.wad (HUD/Flat Graphics)
    | -- graphics == palette, graphics lumps, and project files
    | -- maps == maps and brushmodels
    | -- models == model & sprite data.
    | -- music == music tracks for gameplay ambiance
    | -- qcc-src == source code for progs.dat game data file
    | -- sound == Sound FX for in-game actions and environments
    | -- source == Source code for bin/ assets, and python script tools.
    | -- textures == all map texture assets, raw and compiled in WAD2 format.

-------------------------------------------------------------------------------------------

       This project template includes a QuakeC codebase with version 1.06 bug fixes.

-------------------------------------------------------------------------------------------

Several useful utilities coded in Python (for cross-compatibility) are included:

        - Colorgen.py
                (generates a light colormap for DOSQuake from a given palette)

        - File_Splitter.py
                (for reading and file output for 'config/files.dat')

        - GetPop.py
                (Translated LibreQuake source code (from C) to make pop.lmp

        - LMPwad.py
                (unused by developer, GUI tool for WADs with raw .LMP data)

        - makePAK.py
                (used in lieu of QPakMan to generate the final 'pak0.pak' file)

        - png2ppm.py
                (unused, converts .png to an easy image format to parse with code)

-------------------------------------------------------------------------------------------

\\\    COMPILING PROJECT TOOLS    \\\
      -------------------------
    Currently, you must compile all C programs in 'source/' yourself. GCC should do the
trick, the most any of them should require on compile time is the -lm flag, but shouldn't
need anything else AS OF NOW (8/8/25)

\\\    COMPILING DEMOS    \\\
      -----------------
The Makefile reads 'files.dat' for the "quake.rc" file, specifically for the line that contains
the command 'startdemos', and any filenames listed afterwards will be stored and demos with the
same filename will be grabbed from the 'demos' directory.