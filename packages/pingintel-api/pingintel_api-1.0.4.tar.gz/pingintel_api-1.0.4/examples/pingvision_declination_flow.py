import pathlib
import site
from pprint import pprint
import time

from pingintel_api.utils import set_verbosity
from pingintel_api.pingvision import types as t

site.addsitedir("../src")

from pingintel_api import PingVisionAPIClient

SCRIPT_DIR = pathlib.Path(__file__).parent
set_verbosity(3)

division_id = 11
division_short_name = "WKFC"
team_short_name = "WKFC"

api_client = PingVisionAPIClient(environment="dev")

ret = api_client.get_teams()
pprint(ret)
breakpoint()

ret = api_client.create_submission(
    filepaths=[SCRIPT_DIR / "test_sov.xlsx"], delegate_to_division=division_short_name, delegate_to_team=team_short_name
)
pingid = ret["id"]
url = ret["url"]

print(f"pingid: {ret['id']}")

ret = api_client.get_submission_events(page_size=10, division_id=division_id, pingid=pingid)
pprint(ret)


# def handler():
#     if event_type != t.SUBMISSION_EVENT_LOG_TYPE.SUBMISSION_STATUS_CHANGE:
#         continue


pingid = "p-as-wkfc-21cw2qt"

while True:

    submission_detail = api_client.list_submission_activity(pingid=pingid)

    submission_ret = submission_detail["results"][0]
    if submission_ret["workflow_status__name"] == "Waiting for scrubbing":
        break

    print(f"Current status: {submission_ret['workflow_status__name']}")
    for job in submission_ret["jobs"]:
        job: t.PingVisionListActivityDetailJobResponse
        if job["processing_status"] == t.DOCUMENT_PROCESSING_STATUS.COMPLETED:
            pass
        elif job["processing_status"] == t.DOCUMENT_PROCESSING_STATUS.FAILED:
            print(
                f"Job {job['job_type']} is failed, status: {job['processing_status']}, {job.get('processing_pct_complete', 'n/a')}%"
            )
        elif job["processing_status"] != "C":
            print(
                f"Job {job['job_type']} is not complete, status: {job['processing_status']}, {job.get('processing_pct_complete', 'n/a')}%"
            )

    time.sleep(5)

# download the document
for document in submission_ret["documents"]:
    if document["document_type"] == "SOVFIXER_JSON":
        filename = document["filename"]
        document_url = document["url"]
        break
else:
    raise ValueError("No JSON document found")

output_filename = "downloaded-" + filename
api_client.download_document(output_filename, document_url=document_url)

print(f"Downloaded file to {output_filename}")

# make some decisions...

print("Valid actions:")
pprint.pprint(submission_ret["actions"]["transition_to"])

# These are subject to change based on how we configure your workflow
WORKFLOW_STATUS_PLEASE_SCRUB = 3
WORKFLOW_STATUS_DECLINE = 7

api_client.change_status(pingid=pingid, workflow_status_id=WORKFLOW_STATUS_DECLINE)
