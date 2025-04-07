import logging
from unittest.mock import MagicMock

import pytest
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save

from signal_handler.handlers import SignalHandler


class MockModel:
    """
    A mock model class to simulate Django model instances.

    This class is used in the tests to mimic the behavior of a Django model instance
    without needing to interact with an actual database.
    """

    def __init__(self, pk=None):
        self.pk = pk


@pytest.fixture
def signal_handler():
    """
    Fixture that provides a SignalHandler instance for the tests.

    This ensures a new instance of SignalHandler is available for each test case.
    """
    return SignalHandler()


@pytest.fixture
def mock_instance():
    """
    Fixture that provides a mock instance of MockModel for testing.

    This creates a mock model instance that can be passed into the SignalHandler's methods.
    """
    return MockModel()


def test_run_pre_save_new(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the pre_save signal for a new instance.

    This test ensures that the `pre_save_new` method is called with the correct arguments
    when the `run` method is invoked with the pre_save signal for a new instance (without a pk).
    """
    signal_handler.pre_save_new = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=pre_save)
    signal_handler.pre_save_new.assert_called_once_with(mock_instance, signal=pre_save)


def test_run_pre_save_update(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the pre_save signal for an updated instance.

    This test ensures that the `pre_save_update` method is called with the correct arguments
    when the `run` method is invoked with the pre_save signal for an updated instance (with a pk).
    """
    mock_instance.pk = 1
    signal_handler.pre_save_update = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=pre_save)
    signal_handler.pre_save_update.assert_called_once_with(
        mock_instance, signal=pre_save
    )


def test_run_post_save_new(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the post_save signal for a new instance.

    This test ensures that the `post_save_new` method is called with the correct arguments
    when the `run` method is invoked with the post_save signal and the created flag set to True.
    """
    signal_handler.post_save_new = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=post_save, created=True)
    signal_handler.post_save_new.assert_called_once_with(
        mock_instance, signal=post_save, created=True
    )


def test_run_post_save_update(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the post_save signal for an updated instance.

    This test ensures that the `post_save_update` method is called with the correct arguments
    when the `run` method is invoked with the post_save signal and the created flag set to False.
    """
    signal_handler.post_save_update = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=post_save, created=False)
    signal_handler.post_save_update.assert_called_once_with(
        mock_instance, signal=post_save, created=False
    )


def test_run_pre_delete(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the pre_delete signal.

    This test ensures that the `pre_delete` method is called with the correct arguments
    when the `run` method is invoked with the pre_delete signal.
    """
    signal_handler.pre_delete = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=pre_delete)
    signal_handler.pre_delete.assert_called_once_with(mock_instance, signal=pre_delete)


def test_run_post_delete(signal_handler, mock_instance):
    """
    Test the behavior of the SignalHandler when handling the post_delete signal.

    This test ensures that the `post_delete` method is called with the correct arguments
    when the `run` method is invoked with the post_delete signal.
    """
    signal_handler.post_delete = MagicMock()
    signal_handler.run(MockModel, mock_instance, signal=post_delete)
    signal_handler.post_delete.assert_called_once_with(
        mock_instance, signal=post_delete
    )


def test_run_unknown_signal(signal_handler, mock_instance, caplog):
    """
    Test the behavior of the SignalHandler when an unknown signal is provided.

    This test ensures that a warning is logged when the `run` method is invoked with
    an unrecognized signal.
    """
    unknown_signal = "unknown_signal"
    with caplog.at_level(logging.WARNING):
        signal_handler.run(MockModel, mock_instance, signal=unknown_signal)
    assert f"Unknown or missing signal in kwargs: {unknown_signal}" in caplog.text


def test_default_pre_save_new(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for pre_save_new.

    This test verifies that the default implementation of the `pre_save_new` method
    does not raise any errors when invoked.
    """
    signal_handler.pre_save_new(mock_instance)


def test_default_post_save_new(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for post_save_new.

    This test verifies that the default implementation of the `post_save_new` method
    does not raise any errors when invoked.
    """
    signal_handler.post_save_new(mock_instance)


def test_default_pre_save_update(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for pre_save_update.

    This test verifies that the default implementation of the `pre_save_update` method
    does not raise any errors when invoked.
    """
    signal_handler.pre_save_update(mock_instance)


def test_default_post_save_update(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for post_save_update.

    This test verifies that the default implementation of the `post_save_update` method
    does not raise any errors when invoked.
    """
    signal_handler.post_save_update(mock_instance)


def test_default_pre_delete(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for pre_delete.

    This test verifies that the default implementation of the `pre_delete` method
    does not raise any errors when invoked.
    """
    signal_handler.pre_delete(mock_instance)


def test_default_post_delete(signal_handler, mock_instance):
    """
    Test the default behavior of the SignalHandler for post_delete.

    This test verifies that the default implementation of the `post_delete` method
    does not raise any errors when invoked.
    """
    signal_handler.post_delete(mock_instance)
