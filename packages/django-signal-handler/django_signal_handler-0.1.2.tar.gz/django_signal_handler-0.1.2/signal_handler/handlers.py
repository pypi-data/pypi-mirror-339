import logging
from typing import Any

from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

logger = logging.getLogger(__name__)


class SignalHandler:
    """
    A base class for handling Django model signals.

    This class provides methods to handle Django signals related to model saving and deleting
    (pre_save, post_save, pre_delete, and post_delete). It determines the appropriate handler
    based on the signal type and invokes the corresponding method.
    """

    def run(self, sender: type, instance: Any, **kwargs: Any) -> None:
        """
        Determines the signal type and calls the appropriate handler method.

        Based on the received signal (pre_save, post_save, pre_delete, post_delete), this method
        routes the execution to the appropriate handler method for either a new or existing instance.

        Args:
            sender (type): The model class that sent the signal.
            instance (Any): The instance of the model that is being processed.
            **kwargs (dict): Additional keyword arguments from the signal, such as the signal itself
                             and properties like 'created' for post_save.
        """
        signal_obj = kwargs.get("signal")

        if signal_obj == pre_save:
            if instance.pk is None:
                self.pre_save_new(instance, **kwargs)
            else:
                self.pre_save_update(instance, **kwargs)
        elif signal_obj == post_save:
            if kwargs.get("created", False):
                self.post_save_new(instance, **kwargs)
            else:
                self.post_save_update(instance, **kwargs)
        elif signal_obj == pre_delete:
            self.pre_delete(instance, **kwargs)
        elif signal_obj == post_delete:
            self.post_delete(instance, **kwargs)
        else:
            logger.warning("Unknown or missing signal in kwargs: %s", signal_obj)

    def pre_save_new(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for pre_save signals when a new instance is being created.

        This method is called just before a new instance of the model is saved to the database.
        You can override this method to add custom logic for new model instances before saving.

        Args:
            instance (Any): The model instance that is about to be created.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_save_new(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for post_save signals when a new instance is created.

        This method is called after a new instance of the model has been saved to the database.
        You can override this method to add custom logic after saving a new model instance.

        Args:
            instance (Any): The model instance that was just created.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def pre_save_update(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for pre_save signals when an existing instance is being updated.

        This method is called just before an existing instance of the model is saved (updated).
        You can override this method to add custom logic before updating an existing model instance.

        Args:
            instance (Any): The model instance that is about to be updated.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_save_update(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for post_save signals when an existing instance is updated.

        This method is called after an existing instance of the model has been updated in the database.
        You can override this method to add custom logic after updating an existing model instance.

        Args:
            instance (Any): The model instance that was just updated.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def pre_delete(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for pre_delete signals.

        This method is called just before a model instance is deleted from the database.
        You can override this method to add custom logic before a model instance is deleted.

        Args:
            instance (Any): The model instance that is about to be deleted.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_delete(self, instance: Any, **kwargs: Any) -> None:
        """
        Handler for post_delete signals.

        This method is called after a model instance has been deleted from the database.
        You can override this method to add custom logic after deleting a model instance.

        Args:
            instance (Any): The model instance that has been deleted.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass
