export AA_DEPLOYMENT_ENV='dev'
uvicorn app.main:app --reload --access-log
