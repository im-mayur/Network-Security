'''
This program tests if MongoDB is connecting with program successsfully.

--> First complete the signup for mongoDB if you dont have account already. 
--> Crete a cluster for this project. 
--> Set your username and password, this can be done by clicking on "Quickstart" on home page.
--> Ensure you have 'pymongo' installed.

Note:If you encounter error while connecting, consider upgrading 'pymongo' as some functionality maybe deprecated 
     in python version 3.10 and above.
     pip install --upgrade pymongo
'''



from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://<username>:<password>@cluster0.ket73.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)