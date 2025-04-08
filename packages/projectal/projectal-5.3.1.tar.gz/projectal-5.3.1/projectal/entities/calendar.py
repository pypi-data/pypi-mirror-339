import copy

from projectal.errors import UnsupportedException

from projectal.entity import Entity


class CalendarItem(Entity):
    """
    This object represents entries within a calendar, like holidays or leaves.
    They are referred to as "Calendar Exceptions" in the web client.
    """

    _path = "calendar"
    _name = "calendar"


class Calendar(Entity):
    """
    Implementation of the [Calendar](https://projectal.com/docs/latest/#tag/Calendar) API.

    The Calendar object acts as a "container" of calendar items based on type. Types of
    calendars are distinguished by name ("base_calendar", "location", "staff") and
    may contain a set of calendar items either for itself ("location", "staff") or
    for its holder ("base_calendar").
    """

    _path = "calendar"
    _name = "calendar"

    def __init__(self, data):
        super(Calendar, self).__init__(data)

        # Override the inner "calendarList" with the expected type (they are CalendarItems
        # within the Calendar). We have to do this because the built-in conversion assumes
        # they are Calendars because of the name of the list.
        if self.get("calendarList"):
            cals_as_obj = []
            for cal in self.get("calendarList", []):
                cals_as_obj.append(CalendarItem(cal))
            self["calendarList"] = cals_as_obj

    @classmethod
    def create(
        cls,
        holder,
        entity,
        batch_linking=True,
        disable_system_features=True,
        enable_system_features_on_exit=True,
    ):
        """Create a Calendar

        `holder`: `uuId` of the owner

        `entity`: The fields of the entity to be created
        """
        holder_id = holder["uuId"] if isinstance(holder, dict) else holder
        params = "?holder=" + holder_id
        out = super().create(
            entity,
            params,
            batch_linking,
            disable_system_features,
            enable_system_features_on_exit,
        )
        # Calendars use "empty linkers" during creation which don't go through our
        # usual linker pipeline where the internal list is updated. Do it here
        # manually.
        if isinstance(holder, Entity):
            cl = holder.get("calendarList", [])
            cl.append(out)
            holder.set_readonly("calendarList", copy.deepcopy(cl))
        return out

    @classmethod
    def list(cls, expand=False, links=None):
        raise UnsupportedException("Calendar list is not supported by the API.")
