"""Echo: a transport test action for HA AI Studio."""
import copy


async def execute(data, settings):
    """Return independent JSON data without side effects or app dependencies."""
    if settings != {}:
        raise ValueError('Echo has no configurable settings.')
    return copy.deepcopy(data)
