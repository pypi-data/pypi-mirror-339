# Django Signal Handler Framework

This package provides a base class, `SignalHandler`, for simplifying the handling of Django model signals. It streamlines the process of responding to `pre_save`, `post_save`, `pre_delete`, and `post_delete` signals by categorizing them into more specific methods.

## Installation

You can install this framework using pip:

```bash
pip install django-signal-handler
```

## Usage

Create a subclass of `SignalHandler`:

```python
import logging
from typing import Any

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save

from signal_handler import SignalHandler
from your_app.models import MyModel

logger = logging.getLogger(__name__)

class MyModelSignalHandler(SignalHandler):
    def pre_save_new(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Pre-save new: {instance}")
        # Add your logic here

    def post_save_new(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Post-save new: {instance}")
        # Add your logic here

    def pre_save_update(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Pre-save update: {instance}")
        # Add your logic here

    def post_save_update(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Post-save update: {instance}")
        # Add your logic here

    def pre_delete(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Pre-delete: {instance}")
        # Add your logic here

    def post_delete(self, instance: Any, **kwargs: Any) -> None:
        logger.info(f"Post-delete: {instance}")
        # Add your logic here
```

Connect the signal handlers to your model:

```python
from django.dispatch import receiver
from your_app.models import MyModel

from .signal_handlers import MyModelSignalHandler

handler = MyModelSignalHandler()

@receiver(pre_save, sender=MyModel)
@receiver(post_save, sender=MyModel)
@receiver(pre_delete, sender=MyModel)
@receiver(post_delete, sender=MyModel)
def my_model_signals(sender, instance, **kwargs):
    handler.run(sender, instance, **kwargs)
```

## Class Overview

### `SignalHandler`

- **`run(sender: type, instance: Any, **kwargs: Any) -> None`**: 
  - Determines the signal type and dispatches to the appropriate handler method.
- **`pre_save_new(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `pre_save` signals when a new instance is being created.
- **`post_save_new(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `post_save` signals when a new instance is created.
- **`pre_save_update(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `pre_save` signals when an existing instance is being updated.
- **`post_save_update(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `post_save` signals when an existing instance is updated.
- **`pre_delete(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `pre_delete` signals.
- **`post_delete(instance: Any, **kwargs: Any) -> None`**: 
  - Handler for `post_delete` signals.

## Benefits

- **Organization**: Separates signal handling logic into distinct methods, improving code readability and maintainability.
- **Clarity**: Makes it clear which signal is being handled (new vs. update for save signals).
- **Reusability**: The base class can be extended for different models, reducing code duplication.
- **Logging**: Includes basic logging for unknown or missing signals.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.