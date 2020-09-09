# Applied Affect - app backend
## Setup instructions
### Create a conda environment aa_app
`conda create -n aa_app python`
### Activate the conda environment
`conda activate aa_app`
### Install dependencies 
`pip install -r requirements.txt`
### Launch the service
`./run.sh`

### Documentation
By default the documentation will open at <http://127.0.0.1:8000/docs> 

### Build Docker container
`docker build -t aa_app ./`

### Setting up MongoDB to inspect data
- Download Mongodb compass from <https://www.mongodb.com/try/download/compass>
- Connection string: 
`mongodb+srv://tip_user:tip_password@aa.jiqjp.mongodb.net/test`
- Use database `indus_1`

### Docker containers for grading
`docker login registry.gitlab.com`

`docker pull registry.gitlab.com/n0t0/hermes_containers:allennlp_fact_scorer-v0.0.1_demo`

`docker pull registry.gitlab.com/n0t0/hermes_containers:allennlp_fact_extractor-v0.0.1_demo`

`docker run -it -p 32500:5000 registry.gitlab.com/n0t0/hermes_containers:allennlp_fact_extractor-v0.0.1_demo`

`docker run -it -p 42500:5000 registry.gitlab.com/n0t0/hermes_containers:allennlp_fact_scorer-v0.0.1_demo`


## Caveats
- Only `/users/me` end point is under authorization. 

## Sample Data
### Teacher
**username**: <chitranakra@indus.com>

**password**: foobar