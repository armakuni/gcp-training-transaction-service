from unittest.mock import patch

import pytest

from transaction_service.app.infrastructure.project_id_fetcher import \
    ProjectIDFetcher, MetadataServerError


class MockResponse:
    def __init__(self, body, status_code):
        self.text = body
        self.status_code = status_code


@patch('requests.get')
def test_it_sets_the_project_id_and_topic(request_get):
    request_get.return_value = MockResponse('example-id', 200)
    fetcher = ProjectIDFetcher()
    assert fetcher.fetch_project_id() == 'example-id'
    request_get.assert_called_with(
        'http://metadata.google.internal/computeMetadata/v1/project/project-id',  # noqa
        headers={"Metadata-Flavor": 'Google'}
    )


@patch('requests.get')
def test_it_raises_an_error_if_project_id_empty(request_get):
    request_get.return_value = MockResponse('', 200)
    with pytest.raises(MetadataServerError, match=r'project-id is missing'):
        ProjectIDFetcher().fetch_project_id()


@patch('requests.get')
def test_it_raises_an_exception_for_unexpected_status_code(request_get):
    request_get.get.return_value = MockResponse("Not found", 404)
    fetcher = ProjectIDFetcher()
    with pytest.raises(MetadataServerError):
        fetcher.fetch_project_id()


@patch('requests.get')
@patch('logging.error')
def test_it_logs_an_error_for_unexpected_status_code(log_error, request_get):
    request_get.return_value = MockResponse("Not found", 404)
    try:
        ProjectIDFetcher().fetch_project_id()
    except MetadataServerError:
        pass

    log_error.assert_called_with(
        'Metadata server request failed with status code 404')


@patch('requests.get')
@patch('logging.error')
def test_it_logs_an_error_if_project_id_is_missing(log_error, request_get):
    request_get.return_value = MockResponse('', 200)
    try:
        ProjectIDFetcher().fetch_project_id()
    except MetadataServerError:
        pass

    log_error.assert_called_with(
        'Metadata server request failed; project-id is missing')  # noqa
