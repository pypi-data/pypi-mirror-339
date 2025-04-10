# KatapultAPI

katapultAPI is a Python module designed to handle requests made to the Katapult API.

## Installation & Setup

```bash
pip install katapult-api
```

To develop and iterate upon the Katapult API module first clone the repo:

```shell
git clone https://github.com/TechServ-Consulting-Training-Ltd/katapult-api
```

then run the following commands from the project root:

```shell
python -m venv ./.venv
./.venv/Scripts/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Usage

[//]: # (todo maybe a usage of this in a mainly sychronous process)

[//]: # (todo probably short explaination to expand below usage)

### Getting a Job list and Job Details

```python
import logging.config
import asyncio

# Not required but the client itself has logging functionality to help track requests.
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
)

from katapult_api.katapult import Katapult
from katapult_api.utils import task_handler


async def main():
    # Sets up the aiohttp session and closes it after finishing.
    async with Katapult(api_key="YOURAPIKEY") as katapult:
        # Returns a Response object that contains attributes such as return status, content, and even a json() method.
        job_lists = await katapult.job_lists()

        # Here we build 20 payloads that will be sent out at the same time.
        job_ids = [{"job_id": key} for key in list(job_lists.json().keys())[:20]]

        # Not required but makes setting up async tasks easy, pass in a job name and a list of dicts that contain
        # expected params.
        response = await task_handler(katapult.job, job_ids)
    return response


if __name__ == '__main__':
    logger.info(f"Getting jobs...")
    jobs = asyncio.run(main())
    logger.info(f"Finished, got {len(jobs)} jobs.")
```

### Creating and Updating a Node

```python
import asyncio

# Possible logging...

from katapult_api.katapult import Katapult


async def main():
    async with Katapult(api_key="YOURAPIKEY") as katapult:
        # Get job id from job_lists endpoint...
        job_id = "-ABC123"

        # Create a node by passing job id, lat/long, and a flat dict of attributes to write to the node.
        response = await katapult.create_node(job_id, 30.0817, -97.843, {"OID": 123, "my_custom_attr": "howdy partner"})
    return response


if __name__ == '__main__':
    results = asyncio.run(main())
```

The above should result in something like this:

![create_node_example.png](docs/attachments/create_node_example.png)

Similarly, a node can be updated by passing both job and node ids:
```python
import asyncio

# Possible logging...

from katapult_api.katapult import Katapult


async def main():
  async with Katapult(api_key="YOURAPIKEY") as katapult:
    # Get job id from job_lists endpoint...
    job_id = "-ABC123"

    # Get node id from parsing job from job endpoint...
    node_id = "-EFG456"

    # Similar to the create node method but needs a nodeid. Note that lat/long and attributes are
    # technically optional; in this example lat/long are not included.
    response = await katapult.update_node(jobid=job_id, nodeid=node_id, attributes={"my_fav_pokemon": "jigglypuff"})

  return response


if __name__ == '__main__':
  results = asyncio.run(main())
```

### KatapultNice Usage

```python
import logging.config
import asyncio

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

from katapult_api.katapult_nice import KatapultNice
from katapult_api.utils import task_handler


async def main(api_key: str):
    async with KatapultNice(api_key=api_key) as nice:
        job_lists = await nice.job_lists()
        job_ids = [{"job_id": key} for key in list(job_lists.json().keys())[:20]]
        response = await task_handler(nice.job_nodes, job_ids)
    return response


if __name__ == '__main__':
    api_key = "api_key"
    logger.info(f"Getting jobs...")
    jobs = asyncio.run(main(api_key))
    logger.info(f"Finished, got {len(jobs)} jobs.")

```

### Testing

Integration and unit tests are available. All tests can be ran with normal python or coverage using the following commands:
```shell
# run all tests
python -m unittest
# OR
coverage run -m unittest

# run tests in given folder
python -m unittest discover tests/unit
# OR
coverage run -m unittest discover tests/unit

# run a specific test
python -m unittest tests.unit.test_client.TestClient.test_various_methods_and_responses
# OR
coverage run -m unittest tests.unit.test_client.TestClient.test_various_methods_and_responses
```
A coverage report can then be generated afterwords. Note that only unit tests are automatically ran with github actions.

#### Utils

There is a command to clear all jobs from the test folder (```Techserv/TEST```) that can ran by using the following
command:
```shell
python -m tests.utils.clear_test_folder
```
This should not typically be needed but is available.

### Building

For building and updating the PYPI project found here: https://pypi.org/project/katapult-api/, just create a new release
on GitHub. There is a GitHub Action that will automatically deploy to PYPI. You will need to create a new tag such as
```v.0.0.0```:

![build1.png](docs/attachments/build1.png)
![build2.png](docs/attachments/build2.png)
![build3.png](docs/attachments/build3.png)


## Resources

- https://documenter.getpostman.com/view/9081167/SVtVV93W: Katapultpro API V1
- https://github.com/KatapultDevelopment/katapult-pro-api-documentation?tab=readme-ov-file: Katapultpro Github

## TODOS
- [Maybe a use a custom exception or see if aiohttp has one.](https://github.com/TechServ-Consulting-Training-Ltd/katapult-api/blob/main/katapult_api/client.py#L86)
- [May need to reach out to katapult on how to do this for the write job data method.](https://github.com/TechServ-Consulting-Training-Ltd/katapult-api/blob/main/tests/integration/test_katapult.py#L115)
  - [Can not figure out how to set attributes; may not be worthwhile.](https://github.com/TechServ-Consulting-Training-Ltd/katapult-api/blob/main/katapult_api/katapult.py#L65)
- Maybe add a list of currently supported methods to the README?
- Do we want the methods named get_*, post_*, del_*, etc.?
