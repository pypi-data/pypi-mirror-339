from collections import namedtuple
import time
from typing import Dict, Any, Optional, Callable

import requests
from requests.structures import CaseInsensitiveDict

from opendors.abc import WorkflowRule
from opendors.model import VersionType, SourceCodeRepository, Corpus

SwhIdentifiers = namedtuple("IDs", ["swh_id", "swh_dir_id"])


class SWHIdError(Exception):
    pass


# class APIQueryError(Exception):
#     """Custom exception for API query failures."""
#
#     pass


# class RateLimitExceededError(Exception):
#     """Custom exception for rate limit exceeded scenarios."""
#
#     pass


class SWHIdRetriever(WorkflowRule):
    """
    TODO
    """

    def __init__(
        self,
        corpus: Corpus,
        swh_token: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.corpus = corpus
        self.base_url = "https://archive.softwareheritage.org/api/1"
        self.auth_token = swh_token
        self.headers = {
            "Authorization": f"Bearer {swh_token}",
            "Content-Type": "application/json",
        }
        self.rate_limit = 1200  # Default rate limit (calls per hour)
        self.rate_limit_remaining = 1200  # Default remaining calls
        self.rate_limit_reset = 0  # Default reset time (Unix timestamp)

    def run(self) -> Corpus:
        software = self.corpus.research_software[0]

        for repo in software.repositories:
            if repo.accessible and repo.latest is not None:
                swh_identifiers = self.retrieve_swh_ids(repo)
                if swh_identifiers is not None:
                    repo.latest.swh_id = swh_identifiers.swh_id
                    repo.latest.swh_dir_id = swh_identifiers.swh_dir_id

        return self.corpus

    def retrieve_swh_ids(self, repo: SourceCodeRepository) -> SwhIdentifiers:
        latest = repo.latest
        if latest.version_type == VersionType.TAG:
            if latest.tag_sha is not None:
                return self._retrieve_swh_ids_release(repo)
            else:
                return self._retrieve_swh_ids_revision(repo)
        elif latest.version_type == VersionType.REVISION:
            return self._retrieve_swh_ids_revision(repo)

    def _retrieve_swh_ids_release(
        self, repo: SourceCodeRepository, new_snp: bool = False
    ) -> SwhIdentifiers | None:
        def handle_missing_snapshot():
            if new_snp:
                self.log.warning(
                    f"Release {repo.latest.tag_sha} could not be found in newly created snapshot."
                )
                return
            snp_id = self.save_swh_snapshot(repo)
            if snp_id is not None:
                return self._retrieve_swh_ids_release(repo, True)

        try:
            response = self.get(
                f"release/{repo.latest.tag_sha}/",
                not_found_handler=handle_missing_snapshot,
            )
            if response is not None:
                data = response.json()
                revision_id = self.extract_revision_id(data)
                if revision_id is not None:
                    swh_ids = self._retrieve_swh_ids_revision(repo, revision_id)
                    if swh_ids is not None:
                        return SwhIdentifiers(
                            swh_ids.swh_id,
                            swh_ids.swh_dir_id,
                        )
                self.log.debug(
                    f"In lieu of revision + directory SWH ids, "
                    f"constructing release id for latest version of {repo.clone_url}."
                )
                return SwhIdentifiers(self.construct_swh_id("rel", data["id"]), None)
        except Exception as he:
            self.log.warning(
                f"Something went wrong retrieving SWH IDs for latest version {repo.latest.tag_sha} "
                f"of repo {repo.clone_url}: {he}"
            )
            # case 400:
            #     self.log.warning(f"Bad request for: 'release/{repo.latest.tag_sha}'.")
            #     return None

    def _retrieve_swh_ids_revision(
        self, repo: SourceCodeRepository, revision_id: str = None, new_snp: bool = False
    ) -> SwhIdentifiers | None:
        if revision_id is None and repo.latest.commit_sha is not None:
            revision_id = repo.latest.commit_sha

        def handle_missing_snapshot():
            if new_snp:
                self.log.warning(
                    f"Revision {revision_id} could not be found in newly created snapshot."
                )
                return
            snp_id = self.save_swh_snapshot(repo)
            if snp_id is not None:
                self._retrieve_swh_ids_revision(repo, revision_id, True)

        try:
            response = self.get(
                f"revision/{revision_id}/", not_found_handler=handle_missing_snapshot
            )
            if response is not None:
                data = response.json()
                self.log.debug(
                    f"Successfully retrieved revision + directory SWH ids for latest version of {repo.clone_url}."
                )
                return SwhIdentifiers(
                    self.construct_swh_id("rev", data["id"]),
                    self.construct_swh_id("dir", data["directory"]),
                )
        except Exception as he:
            self.log.warning(
                f"Something went wrong retrieving SWH IDs for latest version {repo.latest.tag_sha} "
                f"of repo {repo.clone_url}: {he}"
            )
            # case 400:
            #     self.log.warning(f"Bad request for: 'revision/{revision_id}'.")
            #     return None

    @staticmethod
    def construct_swh_id(typ: str, sha: str) -> str:
        return f"swh:1:{typ}:{sha}"

    def save_swh_snapshot(self, repo: SourceCodeRepository) -> str | None:
        url_path = f"origin/save/{repo.vcs.value}/url/{str(repo.clone_url).removesuffix('.git')}/"
        response = self.post(url_path)
        data = response.json()
        # if response.status_code == 400:
        #     self.log.warning(
        #         f"Bad request. An invalid visit type or origin URL has been provided: {repo.clone_url}."
        #     )
        if response.status_code == 403:
            self.log.warning(
                f"The repository URL is blacklisted for the Software Heritage Archive: {repo.clone_url}."
            )
        elif response.status_code == 200:
            if data["save_request_status"] == "accepted":
                visit = self.track_swh_request(data["id"])
                if visit is not None:
                    if visit["save_task_status"] == "succeeded":
                        self.log.info(
                            f"Successfully created new SWH snapshot for {repo.clone_url}."
                        )
                        return visit["snapshot_swhid"]
                    elif visit["save_task_status"] == "failed":
                        note = "No failure note"
                        if "note" in visit:
                            note = visit["note"]
                        self.log.warning(
                            f"Creating a new SWH snapshot for {repo.clone_url} failed: "
                            f"{note if note is not None else 'reason unclear'}."
                        )
                        return None
                else:
                    self.log.warning(
                        f"Could not check completion status for snapshot request {data['id']}."
                    )
                    return None

    def track_swh_request(self, request_id: str) -> dict | None:
        while True:
            try:
                has_completed, result = self.save_completed(
                    f"origin/save/{request_id}/"
                )
                if has_completed:
                    return result
                else:
                    self.log.info("Save not completed, waiting 30 secs.")
                    time.sleep(30)
            except SWHIdError:
                return None

    def save_completed(self, url_path: str) -> (bool, dict | None):
        response = self.get(url_path)
        if response.status_code == 200:
            data = response.json()
            if data["save_task_status"] in ["succeeded", "failed"]:
                return True, data
            else:
                return False, data
        else:
            raise SWHIdError(
                f"Non 200 status code for querying SWH API with {url_path}."
            )

    @staticmethod
    def extract_revision_id(release_data: dict) -> str | None:
        if release_data["target_type"] == "revision":
            return release_data["target"]
        else:
            return None

    ###################################################################

    def _update_rate_limit_info(self, headers: CaseInsensitiveDict[str, str]) -> None:
        """
        Update rate limit information from response headers.
        """
        if "X-RateLimit-Limit" in headers:
            self.rate_limit = int(headers["X-RateLimit-Limit"])

        if "X-RateLimit-Remaining" in headers:
            self.rate_limit_remaining = int(headers["X-RateLimit-Remaining"])

        if "X-RateLimit-Reset" in headers:
            self.rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _wait_for_rate_limit_reset(self) -> None:
        """
        Wait until the rate limit resets if necessary.
        """
        if self.rate_limit_remaining <= 0:
            current_time = time.time()
            if self.rate_limit_reset > current_time:
                wait_time = (
                    self.rate_limit_reset - current_time + 1
                )  # Add 1 second buffer
                self.log.info(
                    f"Rate limit reached. Waiting {wait_time:.2f} seconds for reset."
                )
                time.sleep(wait_time)
                self.rate_limit_remaining = self.rate_limit  # Reset the counter
            else:
                # If reset time is in the past, just wait a short time and try again
                self.log.warning(
                    "Rate limit reset time is in the past. Waiting 5 seconds."
                )
                time.sleep(5)

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay: int = 2,
        not_found_handler: Optional[Callable[[str], Any]] = None,
    ) -> requests.Response:
        """
        Make an API request, respecting rate limits.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/').rstrip('/')}/"
        retries = 0

        while retries <= max_retries:
            # Check and wait for rate limit if necessary
            self._wait_for_rate_limit_reset()

            try:
                self.log.debug(f"Making {method} request to {url}.")
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    data=data,
                    json=json_data,
                    timeout=30,  # Set a reasonable timeout
                )

                # Update rate limit information
                self._update_rate_limit_info(response.headers)

                # Log remaining rate limit
                self.log.debug(
                    f"Rate limit remaining: {self.rate_limit_remaining}/{self.rate_limit}."
                )

                # Handle 404
                if response.status_code == 404 and not_found_handler is not None:
                    self.log.info(
                        f"Resource not found (404) at {url}. Calling handler function."
                    )
                    return not_found_handler()

                # Raise an exception for 4XX/5XX responses
                response.raise_for_status()

                return response

            except requests.exceptions.HTTPError as he:
                status_code = he.response.status_code

                # Handle 404 errors with custom handler if provided
                if status_code == 404 and not_found_handler is not None:
                    self.log.info(
                        f"Resource not found (404) at {url}. Calling handler function."
                    )
                    return not_found_handler(endpoint)

                # Handle rate limiting (status code 429)
                if status_code == 429:
                    self._update_rate_limit_info(he.response.headers)
                    self.log.warning(
                        "Rate limit exceeded (429 response). Waiting for reset."
                    )
                    self._wait_for_rate_limit_reset()
                    retries += 1
                    continue

                # Server errors might be temporary
                elif 500 <= status_code < 600:
                    if retries < max_retries:
                        wait_time = retry_delay * (2**retries)  # Exponential backoff
                        self.log.warning(
                            f"Server error {status_code}. Retrying in {wait_time} seconds."
                        )
                        time.sleep(wait_time)
                        retries += 1
                        continue
                    else:
                        self.log.error(
                            f"Failed after {max_retries} retries with server error {status_code}."
                        )
                        raise

                # Client errors (4XX) other than 429 are likely not going to be resolved by retrying
                else:
                    self.log.error(f"Client error: {status_code} - {he.response.text}.")
                    raise

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ):
                if retries < max_retries:
                    wait_time = retry_delay * (2**retries)
                    self.log.warning(
                        f"Connection error or timeout. Retrying in {wait_time} seconds."
                    )
                    time.sleep(wait_time)
                    retries += 1
                    continue
                else:
                    self.log.error(
                        f"Failed after {max_retries} retries with connection error"
                    )
                    raise

        # Should not reach here, but just in case
        raise requests.exceptions.RequestException("Maximum retries exceeded.")

    def get(
        self, endpoint: str, not_found_handler: Optional[Callable[[str], Any]] = None
    ) -> requests.Response:
        return self.make_request("GET", endpoint, not_found_handler=not_found_handler)

    def post(
        self, endpoint: str, json_data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        return self.make_request("POST", endpoint, json_data=json_data)


# Example usage
# if __name__ == "__main__":
#     # Initialize the client
#     api_client = RateLimitedAPIClient(
#         base_url="https://api.example.com/v1", auth_token="your_auth_token_here"
#     )
#
#     # Example of making API calls
#     try:
#         # Make a GET request
#         response = api_client.get("resources", params={"limit": 100})
#         print(f"Response status: {response.status_code}")
#         print(f"Data: {response.json()}")
#
#         # Make a POST request
#         create_response = api_client.post(
#             "resources", json_data={"name": "New Resource"}
#         )
#         print(f"Create response: {create_response.status_code}")
#
#         # Simulate making many API calls to demonstrate rate limiting
#         for i in range(10):
#             print(f"Making request {i + 1}")
#             response = api_client.get(f"resources/{i}")
#             print(f"Rate limit remaining: {api_client.rate_limit_remaining}")
#
#     except Exception as e:
#         print(f"Error: {e}")
