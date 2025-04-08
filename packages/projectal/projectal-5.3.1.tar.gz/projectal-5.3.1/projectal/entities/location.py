from datetime import datetime

import projectal
from projectal.entity import Entity
from projectal.linkers import *


class Location(
    Entity,
    CompanyLinker,
    CustomerLinker,
    ProjectLinker,
    StaffLinker,
    NoteLinker,
    CalendarLinker,
    TagLinker,
):
    """
    Implementation of the [Location](https://projectal.com/docs/latest/#tag/Location) API.
    """

    _path = "location"
    _name = "location"
    _links = [NoteLinker, CalendarLinker, TagLinker]
    _links_reverse = [CompanyLinker, CustomerLinker, ProjectLinker, StaffLinker]

    def calendar(self, begin=None, until=None):
        """
        Get the location's calendar.
        `uuId`: The location `uuId`
        `begin`: Start date in `yyyy-MM-dd` format
        `until`: End date in `yyyy-MM-dd` format
        """
        if begin:
            begin = datetime.strptime(begin, "%Y-%m-%d").date()
        if until:
            until = datetime.strptime(until, "%Y-%m-%d").date()

        url = "/api/location/{}/calendar?".format(self["uuId"])
        params = []
        params.append("begin={}".format(begin)) if begin else None
        params.append("until={}".format(until)) if until else None
        url += "&".join(params)

        cals = api.get(url)
        cals = [projectal.Calendar(c) for c in cals]
        return cals
