# horizon4_livemap
Python (3.8) tool which shows your current map position in Forza Horizon 4.


# Usage

<img src="https://github.com/bbb0x/horizon4_livemap/blob/master/github/fh4lm.png" width="600">

Just launch the tool and connect to the UDP output of the game with the details displayed in the program.
Your current world position will be displayed in the program. Very useful to check your current location in The Eliminator, as you normally have to pause the game. It is recommended that you are using at least 2 monitors, and have this program open on another monitor while playing the game on your main screen. Works with both PC and Xbox version of the game.

## PC Troubleshooting

Windows blocks UWP Apps (including FH4) to send UDP Data to the local PC. So if you are using this tool on the same PC you play Horizon 4 on, you need to exempt the game from it. I found a tool which can do this here: https://www.simracingstudio.com/forzah

## For Developers

This program was developed using Visual Studio Code on Windows. You should be able to use anything really, it's a very simple project that uses wxPython for the GUI. This was my first time on Python, so don't be surprised if I made something stupid - but I'm actually pretty pleased how it turned out.

# Todos
- Only main map is supported. While Fortune Island's positions do not overlap, the Lego Speed Champion Islands positions overlap with the main map.
Could maybe check the Y position of some areas to determinate if user is on main map or Lego. Need to find a way using the UDP Out.

- Could experiment with a slight (user-modifyable) zoom which centers on the driver, as the map is quite large

- Untested on Unix/Mac, but this program does not knowingly use Windows depended references.
