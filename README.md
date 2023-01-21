# overatch-team-randomizer

Generate random teams for custom games with the homies <3 
Can be configured for balanced (2v2, 3v3) and unbalanced matchups (i.e 2v3, 3v4, 4v5)

This script uses **json** entries to determine player names and role compositions for teams. 
Edit the values in the json file to configure players and roles. 
A different format is used for *BALANCED* vs *UNBALANCED* teams so edit the file accordingly

To run the script with a *BALANCED* team just run `python index.py` once you have finished updating *team_comp_balanced.json*
To run the script with a *UNBALANCED* team just run `python index.py u` once you have finished updating *team_comp_balanced.json* (I am using the letter 'u' here but any letter EXCEPT the letter 'b' can be used)

After the script runs it will print the hero selections to the terminal. ENJOI