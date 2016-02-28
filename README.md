# README #

### Overview ###
    
 * The app can help network administrators to take notice of users that exceed certain amount of network traffic

### How do I get set up? ###

 * Create a new virtual env for the project: virtualenv eduroam_abusers
 * Change to the eduroam_abusers directory
 * Clone the code from bitbucket: git clone https://rbuzatu90@bitbucket.org/rbuzatu90/eduroam_abusers.git
 * Activate the virtualenv defined before: source bin/activate
 * Install the necessary requirements: pip install -r requirements.txt
 * At this point you can use this tool by calling: main.py auto

### Configuration ###

* Use -P as argument in order to set the password for further uses

### Examples ###

 * List users that exceed 50GB size for download trafic
  
  main.py auto -l 50gb
  
 * Search for user using MAC address and go back 5 days in time
  
  main.py mac -m 11:22:33:44:55:66 -d 5