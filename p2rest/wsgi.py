import os
from p2rest.src import create_app

config_name = 'prod'
if 'P2REST_CONFIG_NAME' in os.environ.keys():
    config_name = os.environ['P2REST_CONFIG_NAME']

app = create_app(config_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
