# Books and Authors Database

## Description
This project is a simple database system that manages books and authors using SQLAlchemy and SQLite. It uses Faker library to generate random data for the tables.
The system includes also queries to retrieve information such as the book with the most pages, the youngest author, author who hasn't any books at all and who has more than three books. 

## Project Structure
- db_objects.py -  Defines the database and populatesw the tabled with randomly generated data using Faker
- queries.py - contains SQLAlchemy queries to retrieve various data from the database
- connections.py - manages the connection to the SQLite database


## Requirements
- Faker==29.0.0
- python-dateutil==2.9.0.post0
- SQLAlchemy==2.0.35
- SQLAlchemy-Utils==0.41.2
You can install thses dependencies using pip:
** pip install sqlalchemy sclalchemy-utils Faker **

## Database Structure
**Tables**
1. Authors
   - id: Integer, Primary Key
   - first_name: String
   - last_name: String
   - date_of_birth: Date
   - place_of_birth: String
   - Relation with Books
  
2. **Books**
   - id: Integer, Primary Key
   - title: String
   - pages: Integer
   - publishing_date: Date
   - author_id: Integer (Foreign Key)
   - Relationship with Authors

3. association_table
   - Many-to-many relationship between books and Authors


## How to use
- clone the repository or download the script: git clone **https://github.com/MarBifrost/sqlalch_db**
- cd to the repository folder
- install required dependencies which are provided above:
- run db_objects.py to create database and tables
- run queries.py to retrieve data from the tables
- run the command **cat results.txt** to read the file with query results
