"""
Mock tests for cluster deployment and workflow
"""
import pytest
from .deploy_remote_real_test import cloud_params_const, run_single_remote
import vcr
from unittest.mock import patch


@pytest.mark.parametrize('cloud_params', cloud_params_const)
def test_remote(cloud_params, tmp_path):
    cassette_path = f"cassettes/test_remote_{cloud_params['name'].lower()}.yaml"
    with vcr.use_cassette(cassette_path):
        with patch("dh_pyspark.services.remote.base.get_id", return_value="1234"):
            run_single_remote(cloud_params)

