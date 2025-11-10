from fastapi import FastAPI

app = FastAPI(title='API Gateway')


@app.get('/')
def root():
    return {'status': 'ok'}
