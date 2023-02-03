# Transkriptor AI

Hallo David, das hier ist unser GitHub Repo.

In dem Ordner **VM** liegt unser Python Skript ab, welcher auf dem Server ausgeführt wird. 
Den Rest findest du hier. In den js Skripts ist die Funktionalität eingebaut, via einem Fetch den User Input und die Audio an unseren lokalen Flask Server zu schicken.
In der **app.py** fangen wir diesen Input also ab und verarbeiten diesen. Danach wird er mit Hilfe eines Python packages via SSH an unsere VM geschickt und dort weiter verarbeitet.

Den transkribierten Text fangen wir dann ebenfalls mit SSH wieder ab und lesen diesen in JavaScript wieder ein. 