# applied_affect_app
# Create a conda environment aa
conda create -n aa python
# Activate the conda environment
conda activate aa
# Install dependencies 
pip install -r requirements.txt
# Launch the service
uvicorn app.main:app --reload
