from typing import Any
import json
import requests

import six.moves.urllib.parse as urlparse

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ServerError(Exception):
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class Client:
    """
    Client to interface with simulation server
    """

    def __init__(self, remote_base):
        self.remote_base = remote_base
        self.session = requests.Session()
        self.session.headers.update({"Content-type": "application/json"})

    def _parse_server_error_or_raise_for_status(self, resp):
        j = {}
        try:
            j = resp.json()
        except:
            # Most likely json parse failed because of network error, not server error (server
            # sends its errors in json). Don't let parse exception go up, but rather raise default
            # error.
            resp.raise_for_status()
        if (
            resp.status_code != 200 and "message" in j
        ):  # descriptive message from server side
            raise ServerError(message=j["message"], status_code=resp.status_code)
        resp.raise_for_status()
        return j

    def _post_request(self, route, data):
        url = urlparse.urljoin(self.remote_base, route)
        logger.info("POST {}\n{}".format(url, json.dumps(data)))
        resp = self.session.post(
            urlparse.urljoin(self.remote_base, route), data=json.dumps(data)
        )
        return self._parse_server_error_or_raise_for_status(resp)

    def _get_request(self, route):
        url = urlparse.urljoin(self.remote_base, route)
        logger.info("GET {}".format(url))
        resp = self.session.get(url)
        return self._parse_server_error_or_raise_for_status(resp)

    def env_create(self) -> str:
        """Create a new environment instance"""
        route = "/envs/"
        resp = self._post_request(route, {})
        instance_id = resp["instance_id"]
        return instance_id

    def env_build(self, instance_id: str, simulation_schema: dict[str, Any]) -> None:
        """Build the environment with the given simulation schema"""
        route = f"/envs/{instance_id}/build/"
        data = {"simulation_schema": simulation_schema}
        self._post_request(route, data)

    def env_run(self, instance_id: str, simulation_time: float) -> dict[str, Any]:
        """Run the environment for a given amount of time"""
        route = f"/envs/{instance_id}/run/"
        data = {"simulation_time": simulation_time}
        resp = self._post_request(route, data)
        return resp

    def env_close(self, instance_id: str) -> None:
        """Close the environment"""
        route = f"/envs/{instance_id}/close/"
        self._post_request(route, None)

    def shutdown_server(self):
        """Shutdown the server (if supported)"""
        route = "/shutdown/"
        try:
            self._post_request(route, None)
        except:
            pass


if __name__ == "__main__":
    # Example usage

    remote_base = "http://127.0.0.1:5000"
    client = Client(remote_base)

    # Create environment
    instance_id = client.env_create()
    print(f"Created environment with instance_id: {instance_id}")

    # Build environment with a simple schema
    schema = {"sample_parameter": 123}
    client.env_build(instance_id, schema)
    print("Built environment with sample schema")

    # Run simulation
    simulation_time = 10.0
    result = client.env_run(instance_id, simulation_time)
    print(f"Simulation result: {result}")

    # Close environment
    client.env_close(instance_id)
    print("Closed environment")
