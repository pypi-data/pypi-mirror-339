from projectal import api
from projectal.entity import Entity


class Webhook(Entity):
    """
    Implementation of the [Webhook](https://projectal.com/docs/latest/#tag/Webhook) API.
    """

    _path = "webhook"
    _name = "webhook"

    @classmethod
    def update(cls, entities):
        # The webhook API differs from the rest of the system. We need to send some
        # mandatory fields over even if they haven't changed. Do this by faking
        # the change history to always include the required fields.
        if isinstance(entities, dict):
            e_list = [entities]
        else:
            e_list = entities

        for e in e_list:
            if isinstance(e, Webhook):
                e._Entity__old.pop("entity", None)
                e._Entity__old.pop("action", None)
                e._Entity__old.pop("url", None)
        return super(Webhook, cls).update(e_list)

    @classmethod
    def list(cls, start=0, limit=1000, ksort="entity", order="asc"):
        """
        Get a list of registered webhooks.

        Optionally specify a range for pagination.
        """
        url = "/api/webhook/list?start={}&limit={}&ksort={}&order={}".format(
            start, limit, ksort, order
        )
        return api.get(url)

    @classmethod
    def list_events(cls, **kwargs):
        """
        Get a list of webhook events.
        Use parameter format=False to return eventTime as UTC timestamp.
        """

        url = "/api/webhookevent/list"

        params = [f"{k}={v}" for k, v in kwargs.items()]
        if len(params) > 0:
            url += "?" + "&".join(params)
        response = api.get(url)
        return response
