from datetime import timedelta
from typing import List, Dict

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, F, Q, Value
from django.db.models.functions import Concat
from django.utils import timezone

from api.applications.models import HmrcQuery, PartyOnApplication
from api.audit_trail.models import Audit
from api.audit_trail.serializers import AuditSerializer
from api.cases.enums import CaseTypeEnum, CaseTypeSubTypeEnum, AdviceType
from api.cases.models import Case
from api.common.dates import working_days_in_range, number_of_days_since, working_hours_in_range
from api.flags.serializers import CaseListFlagSerializer
from api.organisations.models import Organisation
from api.staticdata.statuses.enums import CaseStatusEnum
from api.users.enums import UserStatuses
from api.users.models import GovUser
from api.cases.enums import CaseTypeTypeEnum
from api.parties.serializers import PartySerializer


def get_case_status_list() -> List[Dict]:
    return CaseStatusEnum.as_list()


def get_case_type_type_list() -> List[Dict]:
    return CaseTypeEnum.case_types_to_representation()


def get_gov_users_list():
    return (
        GovUser.objects.filter(status=UserStatuses.ACTIVE)
        .annotate(full_name=Concat("baseuser_ptr__first_name", Value(" "), "baseuser_ptr__last_name"))
        .values("full_name", id=F("baseuser_ptr_id"))
    )


def get_advice_types_list():
    return AdviceType.to_representation()


def populate_other_flags(cases: List[Dict]):
    from api.flags.models import Flag

    case_ids = [case["id"] for case in cases]

    union_flags = set(
        [
            *Flag.objects.filter(cases__id__in=case_ids).annotate(case_id=F("cases__id")),
            *Flag.objects.filter(organisations__cases__id__in=case_ids).annotate(case_id=F("organisations__cases__id")),
        ]
    )

    for case in cases:
        case_id = str(case["id"])
        flags = [flag for flag in union_flags if str(flag.case_id) == case_id]
        case["flags"] = CaseListFlagSerializer(flags, many=True).data
    return cases


def populate_goods_flags(cases: List[Dict]):
    from api.flags.models import Flag

    case_ids = [case["id"] for case in cases]
    qs1 = Flag.objects.filter(goods__goods_on_application__application_id__in=case_ids).annotate(
        case_id=F("goods__goods_on_application__application_id"),
    )
    qs2 = Flag.objects.filter(goods_type__application_id__in=case_ids).annotate(
        case_id=F("goods_type__application_id"),
    )
    qs3 = Flag.objects.filter(goods__good__id__in=case_ids).annotate(
        case_id=F("goods__good__id"),
    )
    flags = qs1.union(qs2, qs3)

    for case in cases:
        case["goods_flags"] = CaseListFlagSerializer(
            {flag for flag in flags if str(flag.case_id) == str(case["id"])}, many=True
        ).data

    return cases


def populate_destinations_flags(cases: List[Dict]):
    from api.flags.models import Flag

    case_ids = [case["id"] for case in cases]

    flags = Flag.objects.filter(parties__parties_on_application__application_id__in=case_ids).annotate(
        case_id=F("parties__parties_on_application__application_id")
    )
    flags = flags.union(
        Flag.objects.filter(
            parties__parties_on_application__application_id__in=case_ids,
            parties__parties_on_application__deleted_at__isnull=True,
        ).annotate(case_id=F("parties__parties_on_application__application_id"))
    )
    flags = flags.union(
        Flag.objects.filter(countries_on_applications__application_id__in=case_ids).annotate(
            case_id=F("countries_on_applications__application_id")
        )
    )
    flags = flags.union(
        Flag.objects.filter(countries__countries_on_application__application_id__in=case_ids).annotate(
            case_id=F("countries__countries_on_application__application_id")
        )
    )
    flags = flags.union(
        Flag.objects.filter(parties_on_application__application__pk__in=case_ids).annotate(
            case_id=F("parties_on_application__application_id")
        )
    )

    for case in cases:
        # It would seem sensible here to do flags.filter(case_id=case["id"]) however one cannot do further filtering on
        # union queries
        case_flags = {flag for flag in flags if str(flag.case_id) == str(case["id"])}
        case["destinations_flags"] = CaseListFlagSerializer(case_flags, many=True).data

    return cases


def populate_organisation(cases: List[Dict]):
    from api.organisations.serializers import OrganisationCaseSerializer

    case_ids = [case["id"] for case in cases]
    organisations = (
        Organisation.objects.filter(cases__id__in=case_ids)
        .annotate(case_id=F("cases__id"))
        .select_related("primary_site")
        .prefetch_related(
            "primary_site__address",
            "primary_site__address__country",
            "primary_site__site_records_located_at",
            "primary_site__site_records_located_at__address",
            "primary_site__site_records_located_at__address__country",
        )
    )

    for case in cases:
        organisation = next(
            organisation for organisation in organisations if str(organisation.case_id) == str(case["id"])
        )
        case["organisation"] = OrganisationCaseSerializer(organisation).data

    return cases


def populate_is_recently_updated(cases: List[Dict]):
    """
    Given a dictionary of cases, annotate each one with the field "is_recently_updated"
    If the case was submitted less than settings.RECENTLY_UPDATED_WORKING_DAYS ago, set the field to True
    If the case was not, check that it has audit activity less than settings.RECENTLY_UPDATED_WORKING_DAYS
    ago and return True, else return False
    """
    now = timezone.now()
    recent_audits = (
        Audit.objects.filter(
            target_content_type=ContentType.objects.get_for_model(Case),
            target_object_id__in=[
                case["id"]
                for case in cases
                if working_days_in_range(case["submitted_at"], now) > settings.RECENTLY_UPDATED_WORKING_DAYS
            ],
            actor_content_type=ContentType.objects.get_for_model(GovUser),
            created_at__gt=now - timedelta(days=number_of_days_since(now, settings.RECENTLY_UPDATED_WORKING_DAYS)),
        )
        .values("target_object_id")
        .annotate(Count("target_object_id"))
    )

    audit_dict = {audit["target_object_id"]: audit["target_object_id__count"] for audit in recent_audits}

    for case in cases:
        case["is_recently_updated"] = bool(
            working_days_in_range(case["submitted_at"], now) < settings.RECENTLY_UPDATED_WORKING_DAYS
            or audit_dict.get(case["id"])
        )


def get_hmrc_sla_hours(cases: List[Dict]):
    hmrc_cases = [case["id"] for case in cases if case["case_type"]["sub_type"]["key"] == CaseTypeSubTypeEnum.HMRC]
    hmrc_cases_goods_not_left_country = [
        str(id)
        for id in HmrcQuery.objects.filter(id__in=hmrc_cases, have_goods_departed=False).values_list("id", flat=True)
    ]

    for case in cases:
        if case["id"] in hmrc_cases_goods_not_left_country:
            case["sla_hours_since_raised"] = working_hours_in_range(case["submitted_at"], timezone.now())


def populate_destinations(cases: List[Dict]):
    for case in cases:
        id = case["id"]
        destinations = []

        if case["case_type"]["type"]["key"] == CaseTypeTypeEnum.APPLICATION:
            for poa in PartyOnApplication.objects.filter(application=id, deleted_at=None):
                serializer = PartySerializer(poa.party)
                data = serializer.data
                destinations.append(data)

        case["destinations"] = destinations

    return cases


def populate_activity_updates(cases: List[Dict]):
    obj_type = ContentType.objects.get_for_model(Case)
    case_ids = [case["id"] for case in cases]
    ## case_id can be present against 1 of 2 fields so filters required
    obj_as_action_filter = Q(action_object_object_id__in=case_ids, action_object_content_type=obj_type)
    obj_as_target_filter = Q(target_object_id__in=case_ids, target_content_type=obj_type)
    ## get all data related to all cases
    activities_qs = Audit.objects.filter(obj_as_action_filter | obj_as_target_filter).order_by("-updated_at")
    case_id_indexes = {case["id"]: i for i, case in enumerate(cases)}
    ## iterate over audit records once and add if less than 2 records are present against the case
    for activity in activities_qs:
        case_id = None
        ## get case id from either of the audit record fields
        if activity.target_object_id in case_ids:
            case_id = activity.target_object_id
        elif activity.action_object_object_id in case_ids:
            case_id = activity.action_object_object_id
        ## skips record if case not in case_ids i.e. already has 2 records
        if not case_id:
            continue
        activity_obj = AuditSerializer(activity).data
        if "activity_updates" in cases[case_id_indexes[case_id]]:
            ## add second record and remove case_id for case_ids
            cases[case_id_indexes[case_id]]["activity_updates"].append(activity_obj)
            case_ids.remove(case_id)
        else:
            ## add first record against case
            cases[case_id_indexes[case_id]]["activity_updates"] = [activity_obj]
        if not case_ids:
            break

    ## double for loop but easier to follow, iterates over more records
    # all_activities = list(activities_qs)
    # case_ids = [case["id"] for case in cases]
    # obj_as_action_filter = Q(action_object_object_id__in=case_ids, action_object_content_type=obj_type)
    # obj_as_target_filter = Q(target_object_id__in=case_ids, target_content_type=obj_type)
    # activities_qs = Audit.objects.filter(obj_as_action_filter | obj_as_target_filter).order_by("-updated_at")
    # all_activities = list(activities_qs)
    # for case in cases:
    #     for activity in all_activities:
    #         if activity.target_object_id != case["id"] and activity.action_object_object_id  != case["id"]:
    #             continue
    #         activity_obj = AuditSerializer(activity).data
    #         if "activity_updates" in case:
    #             case["activity_updates"].append(activity_obj)
    #             break
    #         else:
    #             case["activity_updates"] = [activity_obj]
    #     all_activities = [activity for activity in all_activities if activity.target_object_id != case["id"] and activity.action_object_object_id  != case["id"]]

    ## several queries but simpler
    # for case in cases:
    #     obj_as_action_filter = Q(action_object_object_id=case["id"], action_object_content_type=obj_type)
    #     obj_as_target_filter = Q(target_object_id=case["id"], target_content_type=obj_type)
    #     activities_qs = Audit.objects.filter(obj_as_action_filter | obj_as_target_filter).order_by("-updated_at")[:2]
    #     activity_objs = AuditSerializer(activities_qs, many=True).data
    #     case["activity_updates"] = activity_objs

    return cases
