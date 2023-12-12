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

3. Add our database as Volume and run the container (please add your absolute path instead of pwd)
    <pre>docker run -v /"pwd"/AdvancedSoftwareEngineering/database:/app/database -p 5000:5000 blokus-app</pre>

4. Visite the Website on
    <pre>http://127.0.0.1:5000</pre>


# Further Information

You can clean the database with /database/db_init.py

1. Navigate to the Repo Folder
    <pre>cd AdvancedSoftwareEngineering/</pre>

2. With python3
    <pre>python3 /database/db_init.py</pre>



