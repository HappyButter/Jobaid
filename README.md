# Job*aid*

![](jobaid.gif)

## Application demo is available on heroku: 

[link to our demo](https://jobaid.herokuapp.com/)

## Participants 
 - Adrian Furman - Team Leader
 - Konrad Walas
 - Mateusz Górczany
 - Michał Ćwierz
 - Mikołaj Marchewa

### Do you need more people: No

## Short description of the idea
Jobaid is web application that helps people to find a job in IT [1] matching specific job offers from the internet to thier abilities and technologies they use at daily basis. ML algorithm will estimate salary that given user could potentialy earn at specific position . Prediction will be based on level of expirience, knowledge of given programming language, company size and location etc.

## User stories:
### job offers list combined from many websites
- User can receive job offers properly filtered according to his preferences and skills
### salary estimation with ML
- User will get estimated salary based on his skills, programming language, city, company size etc.
### gather data from anonymous visitors
- visitor will be able to fill form about their work conditions (salary, company size, location, skills etc) and send it to our data base in order to enlarge our dataset
### statistics and Chart
- User will be given lots of statistics parameters and plots representing current situation in each city, demand for programming language and so on

[1] - IT is good start thanks to amount of job offers available on the internet, if it succeed we can widen our app to other job sectors.

## Tech stack:
- backend => Python, Django
- frontend => Django templates
- database => MongoDB

## Project roadmap

sprint == 1 week

### sprint 0 (done):
- discuss and choose technologies (database, frontend etc.)
- set trello and meeting days

### sprint 1:
- learn basics of web scraping
- play around with django basics
- research on specific webpage offering jobs to gather information about data present at that website - done by every team member
- create basic django project setup
- create-react-app

### sprint 2:
- find suitable ML type/algorithm for our idea
- design major universal WebScrapper class
- attempt to scrap some usefull data
- design frontend 

### sprint 3:
- adjust WebScrapper class
- inspect corresponding  job offers webpage and create model containing crucial info about jobs offers structure (info for web scraping like class or id attributes etc.) - done by every team member
- get to know with LinkedIn Job Search API

### sprint 4:
- start work with ML (assuming we gather any/enough data)
- continue work with frontend
- design basics django routes

### sprint 5:
- integrate frontend with backend
- improve ML - if necessary

### sprint 6:
- SAFE WEEK (we can be sure that something will delay and land in this or in the next sprint)

### sprint 7:
- SAFE WEEK (final touches)
