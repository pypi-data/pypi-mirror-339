from datetime import datetime

import projectal
from projectal.entity import Entity
from projectal.linkers import *
from projectal.errors import UsageException
from projectal.enums import DateLimit


class Staff(
    Entity,
    LocationLinker,
    ResourceLinker,
    SkillLinker,
    FileLinker,
    CompanyLinker,
    DepartmentLinker,
    TaskLinker,
    TaskTemplateLinker,
    NoteLinker,
    CalendarLinker,
    TagLinker,
    ContractLinker,
):
    """
    Implementation of the [Staff](https://projectal.com/docs/latest/#tag/Staff) API.
    """

    _path = "staff"
    _name = "staff"
    _links = [
        LocationLinker,
        ResourceLinker,
        SkillLinker,
        FileLinker,
        NoteLinker,
        CalendarLinker,
        TagLinker,
        ContractLinker,
    ]
    _links_reverse = [CompanyLinker, DepartmentLinker, TaskLinker, TaskTemplateLinker]

    @classmethod
    def calendar(cls, uuId, begin=None, until=None):
        """
        Returns the calendar of the staff with `uuId`.

        `begin`: Start date in `yyyy-MM-dd`.

        `until`: End date in `yyyy-MM-dd`.


        Optionally specify a date range. If no range specified, the
        minimum and maximum dates are used (see projectal.enums.DateLimit).
        """
        if begin:
            begin = datetime.strptime(begin, "%Y-%m-%d").date()
        if until:
            until = datetime.strptime(until, "%Y-%m-%d").date()

        url = "/api/staff/{}/calendar?".format(uuId)
        params = []
        params.append("begin={}".format(begin)) if begin else None
        params.append("until={}".format(until)) if until else None
        url += "&".join(params)

        cals = api.get(url)
        cals = [projectal.Calendar(c) for c in cals]
        return cals

    @classmethod
    def calendar_availability(cls, uuId, begin=None, until=None):
        """
        Returns the availability (in hours) of the staff in `uuId`
        for each day within the specified date range.

        `begin`: Start date in `yyyy-MM-dd`.

        `until`: End date in `yyyy-MM-dd`.

        If no range specified, the minimum and maximum dates are
        used (see projectal.enums.DateLimit).
        """
        if begin:
            begin = datetime.strptime(begin, "%Y-%m-%d").date()
        if until:
            until = datetime.strptime(until, "%Y-%m-%d").date()

        url = "/api/staff/{}/calendar/availability?".format(uuId)
        params = []
        params.append("begin={}".format(begin)) if begin else None
        params.append("until={}".format(until)) if until else None
        url += "&".join(params)

        return api.get(url)

    @classmethod
    def usage(
        cls,
        begin,
        until,
        holder=None,
        start=None,
        limit=None,
        span=None,
        ksort=None,
        order=None,
        staff=None,
    ):
        """
        Returns the staff-to-task allocations for all staff within the `holder`.

        See [Usage API](https://projectal.com/docs/latest/#tag/Staff/paths/~1api~1staff~1usage/post)
        for full details.
        """
        url = "/api/staff/usage?begin={}&until={}".format(begin, until)
        params = []
        params.append("holder={}".format(holder)) if holder else None
        params.append("start={}".format(start)) if start else None
        params.append("limit={}".format(limit)) if limit else None
        params.append("span={}".format(span)) if span else None
        params.append("ksort={}".format(ksort)) if ksort else None
        params.append("order={}".format(order)) if order else None
        if len(params) > 0:
            url += "&" + "&".join(params)
        payload = staff if staff and not holder else None
        response = api.post(url, payload)
        # Do some extra checks for empty list case
        if "status" in response:
            # We didn't have a 'jobCase' key and returned the outer dict.
            return []
        return response

    @classmethod
    def auto_assign(
        cls,
        type="Recommend",
        over_allocate_staff=False,
        include_assigned_task=False,
        include_started_task=False,
        skills=None,
        tasks=None,
        staffs=None,
    ):
        """
        Automatically assign a set of staff (real or generic) to a set of tasks
        using various skill and allocation criteria.

        See [Staff Assign API](https://projectal.com/docs/latest/#tag/Staff-Assign/paths/~1api~1allocation~1staff/post)
        for full details.
        """
        url = "/api/allocation/staff"
        payload = {
            "type": type,
            "overAllocateStaff": over_allocate_staff,
            "includeAssignedTask": include_assigned_task,
            "includeStartedTask": include_started_task,
            "skillMatchList": skills if skills else [],
            "staffList": staffs if staffs else [],
            "taskList": tasks if tasks else [],
        }
        return api.post(url, payload)

    @classmethod
    def create_contract(
        cls,
        UUID,
        payload={},
        end_current_contract=False,
        start_new_contract=False,
    ):
        """
        Creates a new Contract for a staff, with updated fields from the payload

        end_current: Sets the end date of the current contract to today's date
        start_new_date: Sets the start date of the new contract to today's date

        See [Staff Clone API](https://projectal.com/docs/latest#tag/Staff/paths/~1api~1staff~1clone/post)
        for full details.
        """

        url = "/api/staff/clone?reference={}&as_contract=true".format(UUID)
        date_today = datetime.today().strftime("%Y-%m-%d")

        current_staff = None
        if end_current_contract:
            # Check if setting end date to today is
            # invalid for current Staff Contract
            current_staff = cls.get(UUID)
            if projectal.timestamp_from_date(
                current_staff.get("startDate")
            ) > projectal.timestamp_from_date(date_today):
                raise UsageException(
                    f"Cannot set endDate before startDate for current contract: {date_today}"
                )

        if start_new_contract:
            payload["startDate"] = date_today
            payload["endDate"] = DateLimit.Max

        response = api.post(url, payload)

        if end_current_contract and current_staff:
            current_staff["endDate"] = date_today
            current_staff.save()

        return response["jobClue"]["uuId"]
