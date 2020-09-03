# applied_affect_app
# Create a conda environment aa
conda create -n aa python
# Activate the conda environment
conda activate aa
# Install dependencies 
pip install -r requirements.txt
# Launch the service
./run.sh

# Documentation
Add /docs to the URL outputted by run.sh for example 127.0.0.1:8000/docs


# Sample Data
## Teacher
username: latashahenry36@indus.com
password: foobar

## Session
5f427f3d293d7b69b5716d1f

## Camera
5f427f37293d7b69b5716cf1

## Assignments
- See sub_quest.yaml to see question and answers that are seeded

# Setting up MongoDB to look into seed data
- Download Mongodb compass from https://www.mongodb.com/try/download/compass
- Use this connection string : mongodb+srv://tip_user:tip_password@aa.jiqjp.mongodb.net/test
- Use database indus_1

# Caveats
- As if now, only /users/me end point is under authorization. 