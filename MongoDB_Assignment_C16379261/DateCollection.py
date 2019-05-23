# This code converts the Airplane_Crashes collection to be stored by year of the crash
# in a one to many design

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.Assignment
    DatesCol = db["Crash_Dates"]
    usedYears = []
    lastYear = '252651515526'
    year = 1908  # First year in records
    j = 0
    year = str(year)

    crashes = db.Airplane_Crashes.find()  # Cursor for crashes
    years = db.DatesCol.find()  # Cursor for years

    for crash in crashes:  # For each crash

        # Reset variables
        i = 0
        j = 0

        # Check if year of crash has been used already
        for i in usedYears:
            if i in crash['Date']:
                j = 1

        # Check if year has not been used and crash year has not been used
        if year not in usedYears and j != 1:

            year = str(year)

            # Check if there was a crash that year
            if year in crash['Date']:

                db.DatesCol.insert({"Year": year, "Crashes": [""]})  # Add if there was
                usedYears.append(year)
                j = 1
                year = int(year)
                year += 1
                year = str(year)
                i = 1
            else:  # If not increment until a year there was
                while year not in crash['Date']:
                    year = int(year)
                    year += 1
                    year = str(year)

            # Add newly incremented year
            if year in crash['Date'] and i == 0:

                db.DatesCol.insert({"Year": year, "Crashes": []})
                usedYears.append(year)
                year = int(year)
                year += 1

    year = '1908'
    #  New cursors for each collection
    crashes2 = db.Airplane_Crashes.find()
    years2 = db.DatesCol.find()
    crashes2.rewind()
    years2.rewind()

    for crash2 in crashes2:

        years2.rewind()  # Reset the cursor

        for year2 in years2:

            if year2['Year'] in crash2['Date']:
                
                # Update year with crash
                db.DatesCol.update({'Year': year2['Year']}, {'$push': {'Crashes': crash2}}, upsert=True)
                break  # Break once all for that year have been added





