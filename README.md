# Gruppe 2
Leon Ams - Head of Development \
Sercan Berkpinar - Product Owner, Development \
Levin Bolbas - Development \
Lukas Buser - Scrum Master, Development


# Run the project (in docker - Tested for Ubuntu)

1. Navigate to the Repo Folder
    <pre>cd AdvancedSoftwareEngineering/</pre>

2. Build the docker container (try sudo if permission denied)
    <pre>docker build -t blokus-app .</pre>

3. Add our database as Volume and run the container. Please add your absolute path to the Repo Directory instead of "pwd".
    <pre>docker run -v /"pwd"/AdvancedSoftwareEngineering/database:/app/database -p 5000:5000 blokus-app</pre>

4. Visite the Website on
    <pre>http://127.0.0.1:5000</pre>


# Further Information

The Standarduser in the database is test@test with pw: test

You can clean the database with /database/db_init.py (go back to the state with only test@test user)

1. Navigate to the Repo Folder
    <pre>cd AdvancedSoftwareEngineering/</pre>

2. With python3
    <pre>python3 /database/db_init.py</pre>


# Features

1. We have 2 lobbies: one for user games (Lobby 1), where they will be matched with up to 4 AI players, and another for an AI game (Lobby 2). In Lobby 2, you can observe how 4 AI players compete against each other, providing insight into our AI's playstyle.

2. On your profile page, you can perform various user management tasks such as changing your password, deleting your account, or adding a 2FA token.

3. You can join a lobby and wait for other users to join. When the first player clicks "Start new game," the game session initializes, and other users in the lobby can join the game session by clicking "Start new game" as well. We also have a "Clear Lobby" button due to our suboptimal database/lobby setup, which removes every other player from the lobby.

4. At the top of the game session, you can see the active player (user email or "AI" for AI players). Only the active player can perform actions such as inserting blocks (drag and drop), rotating them (click the block and than press key R), and reflecting them (click the block and than press key M). Additionally, you can always see the remaining blocks of the active player. If an AI player is the active player, anyone in the lobby can press "AI Move," and the AI will make its next move.

5. You can choose to surrender the game and watch until the end or leave the lobby using the designated button or by disconnecting from the site.

6. We initially implemented UI intelligence to show valid moves, but the drag-and-drop actions resulted in too many requests, leading to poor performance. Consequently, we decided to remove this feature from our client-side JavaScript. The server-side code is still available in lobby.py at line 462.



