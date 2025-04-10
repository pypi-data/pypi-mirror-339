import asyncio
import logging.config

from katapult_api.katapult import Katapult
from katapult_api.utils import task_handler
from tests.settings import KATAPULT_API_KEY, TEST_DIR_PATH

logging.getLogger("asyncio").setLevel(logging.WARNING)
logger = logging.getLogger("clear_test_folder.main")
logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
)


async def main():
    # Fairly defensive but just in case TEST_DIR_PATH gets changed in the settings.py, really want to confirm what they are doing.
    confirm_string = str(TEST_DIR_PATH)
    user_input = input(
        f"WARNING: This will permanently delete all jobs from:\n"
        f"    {confirm_string}\n\n"
        f"To confirm, please type the full path exactly as shown above:\n"
        f"> "
    )

    if user_input.strip() == confirm_string:
        logger.info("Confirmation matched. Proceeding with deletion...")
        async with Katapult(KATAPULT_API_KEY) as katapult:
            jobs_in_folder = await katapult.jobs_in_folder(TEST_DIR_PATH)
            if jobs_in_folder.status == 200:
                await task_handler(
                    katapult.archive_job,
                    [{"jobid": job_id} for job_id in jobs_in_folder.json()],
                )
            else:
                logger.error(jobs_in_folder.content)
    else:
        logger.info("Confirmation did not match. Operation canceled.")


if __name__ == "__main__":
    asyncio.run(main())
