import logging

import requests


class ProjectIDFetcher:
    def fetch_project_id(self):
        metadata_url = 'http://metadata.google.internal/computeMetadata/v1/project/project-id' # noqa

        response = requests.get(metadata_url,
                                headers={'Metadata-Flavor': 'Google'})

        if response.status_code != 200:
            logging.error(
                f'Metadata server request failed with status code {response.status_code}')  # noqa
            raise MetadataServerError(
                f'${response.status_code} received from metadata server')

        project_id = response.text

        if len(project_id) < 1:
            message = 'Metadata server request failed; project-id is missing'
            logging.error(message)
            raise MetadataServerError(message)

        return project_id


class MetadataServerError(Exception):
    pass
