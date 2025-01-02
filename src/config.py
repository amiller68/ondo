from dotenv import load_dotenv
import os


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value


class Secrets:

    def __init__(self):

        # Load the environment variables
        load_dotenv()


# TODO: getopt() for cmd line arguments
class Config:
    dev_mode: bool
    host_name: str
    listen_address: str
    listen_port: int
    debug: bool
    log_path: str | None
    leaky_url: str

    secrets: Secrets

    def __init__(self):
        # Load the environment variables
        load_dotenv()

        self.dev_mode = os.getenv("DEV_MODE", "False") == "True"

        self.host_name = os.getenv("HOST_NAME", "http://localhost:8000")

        self.listen_address = os.getenv("LISTEN_ADDRESS", "0.0.0.0")

        self.listen_port = int(os.getenv("LISTEN_PORT", 8000))

        # Set the log path
        self.log_path = empty_to_none("LOG_PATH")

        self.leaky_url = empty_to_none("LEAKY_URL")

        # Determine if the DEBUG mode is set
        debug = os.getenv("DEBUG", "True")
        self.debug = debug == "True"

        self.secrets = Secrets()

    def show(self, deep: bool = False):
        if deep:
            secrets = self.secrets.__dict__
            print(self.__dict__)
            print(secrets)
        else:
            print(self.__dict__)
