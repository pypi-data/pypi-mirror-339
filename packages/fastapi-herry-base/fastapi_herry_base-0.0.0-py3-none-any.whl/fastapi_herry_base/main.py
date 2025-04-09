from justasimpletest import BaseFactory

class MyFactory(BaseFactory):
    def get_app_config(self):
        """
        Define the application configuration.
        """
        return {
            'DOCS_URL': '/docs',
            'REDOC_URL': '/redoc',
            'OPENAPI_URL': '/openapi.json'
        }

app = MyFactory().create_app()
@app.get("/")
async def read_root():
    return {"Hello": "World"}
