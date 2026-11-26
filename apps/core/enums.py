"""Enumerations for the core app."""

from django.db import models


class InstitutionType(models.TextChoices):
    UNIVERSITY = "university", "University"
    COMPANY = "company", "Company"
    NON_PROFIT = "non_profit", "Non-Profit"
    RESEARCH_INSTITUTE = "research_institute", "Research Institute"
    GOVERNMENTAL_AGENCY = "governmental_agency", "Governmental Agency"
    FEDERAL_AGENCY = "federal_agency", "Federal Agency"
    STATE_AGENCY = "state_agency", "State Agency"
    INDEPENDENT_RESEARCHER = "independent_researcher", "Independent Researcher"
