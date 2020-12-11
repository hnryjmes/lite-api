import uuid

from django.db import models
from separatedvaluesfield.models import SeparatedValuesField

from api.cases.models import CaseType
from api.common.models import TimestampableModel
from api.flags.enums import FlagStatuses
from api.flags.models import Flag
from api.queues.models import Queue
from api.staticdata.countries.models import Country
from api.staticdata.statuses.models import CaseStatus
from api.teams.models import Team
from api.users.models import GovUser
from api.workflow.routing_rules.enum import RoutingRulesAdditionalFields


class RoutingRuleManager(models.Manager):
    def get_by_natural_key(self, team, queue, status, tier, additional_rules, active, user, country):
        return self.get(
            team=team,
            queue=queue,
            status=status,
            tier=tier,
            additional_rules=additional_rules,
            active=active,
            user=user,
            country=country,
        )


class RoutingRule(TimestampableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, related_name="routing_rules", on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, related_name="routing_rules", on_delete=models.DO_NOTHING,)
    status = models.ForeignKey(CaseStatus, related_name="routing_rules", on_delete=models.DO_NOTHING,)
    tier = models.PositiveSmallIntegerField()  # positive whole number, that decides order routing rules are applied
    additional_rules = SeparatedValuesField(
        choices=RoutingRulesAdditionalFields.choices, max_length=100, blank=True, null=True, default=None
    )
    active = models.BooleanField(default=True)

    # optional fields that are required depending on values in additional_rules
    user = models.ForeignKey(GovUser, related_name="routing_rules", on_delete=models.DO_NOTHING, blank=True, null=True)
    case_types = models.ManyToManyField(CaseType, related_name="routing_rules", blank=True)
    flags = models.ManyToManyField(Flag, related_name="routing_rules", blank=True)
    country = models.ForeignKey(
        Country, related_name="routing_rules", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    objects = RoutingRuleManager()

    class Meta:
        indexes = [models.Index(fields=["created_at", "tier"])]
        ordering = ["team__name", "tier", "-created_at"]
        unique_together = ["team", "queue", "status", "tier", "additional_rules", "active", "user", "country"]

    def natural_key(self):
        return (
            self.team,
            self.queue,
            self.status,
            self.tier,
            self.additional_rules,
            self.active,
            self.user,
            self.country,
        )

    natural_key.dependencies = ["teams.Team", "queues.Queue", "users.GovUser", "countries.Country"]

    def parameter_sets(self):
        """
        Generate a list of sets, containing all the possible subsets of the rule which are true to the condition
            of routing rules. We generate one set for each case_type as we can not have multiple case_types in the set
            (would cause all rules to fail)
        :return: list of sets
        """

        parameter_sets = []

        # Exclude the rule by returning and empty list if there are any inactive flags in the rule
        if self.flags.exclude(status=FlagStatuses.ACTIVE).exists():
            return parameter_sets

        if self.country:
            country_set = {self.country}
        else:
            country_set = set()

        flag_and_country_set = set(self.flags.all()) | country_set

        for case_type in self.case_types.all():
            parameter_set = flag_and_country_set | {case_type}
            parameter_sets.append(parameter_set)

        if not parameter_sets:
            parameter_sets = [flag_and_country_set]

        return parameter_sets
