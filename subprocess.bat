@echo off
start /min "" "main.exe"  # Exécute l'exécutable en minimisant la console
timeout /t 300 /nobreak >nul  # Attendre 5 minutes (300 secondes)
move "mouse_coordinates.txt" "%USERPROFILE%\Downloads"  # Déplacer le fichier de coordonnées
move "mouse_movement.png" "%USERPROFILE%\Downloads"  # Déplacer le fichier d'image
