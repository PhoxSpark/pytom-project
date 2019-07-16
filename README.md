# Python + Atom
Project for collect atom data from PDB database for the Barcelona Supercomputing Center.

## Objectives:
This project has the objective of turn in to an API to download a PDB as a JSON file, applying filters to it and selecting the data that interest the user. The main idea was to select and filter atoms, but in the future this can filter more data inside a PDB.

## Actual features:
This is the updated list of features of this program:

### Download PDB and insert it on a Database
For offline and fast use, Pytom download the PDB of the file one time and inserts it in to a database SQL implemented with Flask. It can handle every PDB on PDB databases (despites the fact that it's only looking for atoms at this moment).

### Manipulate many times the JSON dictionary
You can manipulate many times the same dictionary to apply different filters a lot of times.

### Convert the database in to a JSON
Pytom transforms the created database in to a dictionary, this dictionary is easly manipulated and can be converted as a JSON file. Thats the main objective of the API.

### Select statement
At the moment, Pytom has this statement that allows to select a camp or a list of camps and a value, a non-accurate value (ignoring decimals) or a range of values. Also, allows to apply this select filter to more than one PDB at the same time.

### Nice UI app web
It's under development but the app web explains the main pourpose and origin of the program. The main objective of this app web is to allow more user friendly interactions with Pytom but this can be ignored completly and only use the API part of Pytom.

## API Commands and URL's
Pytom can handle some arguments to edit your JSON output. Those arguments are used in the URL bar.

### Main function, organism
The main function of the Pytom is the look for organism function. This is the syntax:

***localhost:5000/pytom?organism=2ki5***

This will return the JSON file of the PDB 2KI5. Pretty simple to use, every program that handle URL downloads can use it as an API.

***NOTE: The first argument starts with ?, every next argument has to start with &.***

### Species
A working on function, actually you can add the specie of the organism that you are requesting. In the future this is intended to get all the organisms of the specified specimen.

### New statement
If you want to clear your database or the working dictionary, you can do it with the New statement. It's simple, if you write ***?newdb=y***, the whole database will be droped. If you write ***?newdict=y*** the whole working dictionary will be deleted.
This don't limits the program usage, if you delete any of this data, Pytom will create it all the next time you make a query.

### Save statement
Even if you don't use it, it's allways in use because the default output of this statement is "y", in other words, every time you make a query, a ***&save=y*** is "added" to your consult. If you ***don't want to modify the working dictionary*** you can add &save=n to your query. With that done, you can observe the changes that will apply to the dictionary without modifying it.

### Select statement
The select statement allows the user to apply filters. It's used on a concrete way but it's relatively simple and flexible. Here is the syntax:

***localhost:5000/pytom?organism=2ki5&select=CA;name;accurate***

or:

***localhost:5000/pytom?organism=2ki5&select=mode:range;camp:x;value:1,5***

the next is ***not allowed***, if you specify the type you can't use non specified values:

***localhost:5000/pytom?organism=2ki5&select=value:CA;name;accurate***

The select statement has 3 modes: Normal (it will ignore decimals), Accurate (it looks for exact value) and range (it takes two values and select everything between). Normally, you can add more than one values on a camp and even more than one organism, but at this moment it only accepts one camp at the same time.

### Rollback statement
This statement allows the user to go back on his changes. It's very useful in case the user query don't show any results and want to go to before results.

## To-do list
Pytom can do some things, still is a bit empty. There are some to do things that I wan't to implement (the list can be expanded):

  1. Species classification
  2. All organism of a specie download
  3. Multi camp filter
  4. Read the docs documentation
  5. Forms on Pytom URL for easy query
  6. Read more data from the PDB
  7. Specify a different PDB URL download
  8. Make an "only API mode" for easy use without background processing (maybe can't be done)
