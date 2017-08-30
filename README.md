# Toy Catalog
Basic catalog made with Flask and utilising Google' Sign in api 
It also implements an sqlite database, managed with SQLAlchemy
### Dependancies
You will require Vagrant, the [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) and Virtualbox
### How to run the project:
1. Clone the repo to your device: [https://github.com/RoseannaM/catalog](../)
1. Install Vagrant and Virtual box, and clone the vagrantfile into your directory.
2. cd into your directory and spin up and sign into vagrant with  ```vagrant up``` and ```vagrant ssh``` respectively
3. Once in, cd /vagrant and run ```python database.py``` to create the database, then ```python data.py``` to fill it with data
1. Create a Google API Console project [here] (https://console.developers.google.com/projectselector/apis/library), create your client id and secret. 
3. Add the secret and client id and urls in the empty fields in the client_secrets.json file.
4. Type the command ```python main.py``` in your terminal.
[Refer to the docs for troubleshooting](https://developers.google.com/identity/sign-in/web/devconsole-project)

### Endpoints
Endpoints have been included to create json blobs for the toys and toystore data
