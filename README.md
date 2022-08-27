# AffectiveStimuliScraper
Stimuli Scraper GUI for Youtube/Reddit. Uses depth tree search through a network to find stimulus using given keywords. 

<img width="799" alt="Screen Shot 2022-02-27 at 11 20 32 PM" src="https://user-images.githubusercontent.com/34172433/155924242-07a15d9b-eea1-47c1-8783-53f40965f856.png">


# Steps to Setup

Download the python and requirements file

Use pip3 install -r requirements.txt to install dependencies

Go to https://console.cloud.google.com/ 

Log in with your Google account

Under dashboard, click on Create Project

Name and select an organization for your project

Go to OAuth consent screen and fill out the registration form

On the second screen (scopes), select the YouTube Data API v3: ./auth/youtube.readonly, ./auth/youtube, and ./auth/youtube.force-ssl

Click on Credentials, then create credentials → API key

Download clients_secrets.json file created by the credentials and place in the python directory

Input the corresponding information when prompted by the GUI

NOTE: In first run, the terminal will provide a link to autheticate the google API service. Paste that link in the browser and follow the steps. Paste the key generated in the end in terminal.


# GUI Parameters Fields Descriptions

Source of scraping -- Select source as Youtube or Reddit
Developer Key -- Generate your google accounts Developer Key using steps mentioned above
Write to File -- Creates a CSV files with all the results

Seed Key -- ID of the first video to start from. It is 'dQw4w9WgXcQ' from an example URL https://www.youtube.com/watch?v=dQw4w9WgXcQ

Depth of Search -- How indepth search do you wanna perform. Level 1 means searching 5 neighbouring videos of the seed. Level 2 means searching 125 videos wrt seed and its neighbours

Keywords -- The keywords to be looked for in the comments.

Threshold -- The minimum keyword hits for the stimulus to be considered. Default is 10.

