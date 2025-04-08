from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PaymentFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    SEMI_ANNUALLY = "semi-annually"


class LeaseType(str, Enum):
    FIXED = "fixed"
    MONTH_TO_MONTH = "month-to-month"
    YEAR_TO_YEAR = "year-to-year"


class SpaceType(str, Enum):
    OFFICE = "office"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    MIXED_USE = "mixed-use"


class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank-transfer"
    CHECK = "check"
    DIRECT_DEPOSIT = "direct-deposit"
    WIRE_TRANSFER = "wire-transfer"


class Address(BaseModel):
    street: Optional[str] = Field(
        None, description="Street address including building number and street name (e.g., '456 Park Ave Apt 789')"
    )
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State two-letter code (e.g., 'CA', 'NY', 'TX')")
    zip_code: Optional[str] = Field(None, description="ZIP code (e.g., '12345', '12345-6789')")


class ContactInfo(BaseModel):
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Contact email address")
    additional: Optional[str] = Field(None, description="Other contact details")


class Party(BaseModel):
    name: Optional[str] = Field(None, description="Name of the party (e.g., Landlord or Tenant)")
    address: Optional[Address] = Field(None, description="Address details for the party")
    contact: Optional[ContactInfo] = Field(None, description="Contact information for the party")
    identifier: Optional[str] = Field(None, description="Any additional identifier (e.g., registration number)")


class Parties(BaseModel):
    landlord: Optional[Party] = Field(None, description="Information about the landlord")
    tenant: Optional[Party] = Field(None, description="Information about the tenant")


class PropertyDetails(BaseModel):
    address: Optional[Address] = Field(None, description="Property address details")
    square_footage: Optional[float] = Field(None, description="Square footage of the leased space")
    square_footage_unit: Optional[str] = Field(
        None, description="Unit of measurement for square footage (e.g., 'sqft', 'm2')"
    )
    space_type: Optional[SpaceType] = Field(None, description="Type of space")
    parking_spaces: Optional[int] = Field(None, description="Number of parking spaces")
    floor: Optional[int] = Field(None, description="Floor number of the leased premises (e.g., 1, 2, 3, etc.)")
    year_built: Optional[int] = Field(None, description="Year the property was built (e.g., 2020)")
    description: Optional[str] = Field(
        None,
        description="General description of the leased premises including any use restrictions or additional details",
    )


class RenewalOption(BaseModel):
    renewal_period_years: Optional[int] = Field(None, description="Renewal period in years", ge=0)
    notice_period_days: Optional[int] = Field(
        None, description="Notice period in days required to exercise the renewal option", ge=0
    )
    renewal_rent: Optional[float] = Field(None, description="Renewal rent amount", ge=0)
    currency: Optional[str] = Field(None, description="Three-letter currency code (e.g., USD)", pattern="^[A-Z]{3}$")


class LeaseTerm(BaseModel):
    lease_type: Optional[LeaseType] = Field(None, description="Type of lease")
    start_date: Optional[date] = Field(None, description="Lease commencement date")
    end_date: Optional[date] = Field(None, description="Termination date of the lease agreement")
    renewal_options: Optional[RenewalOption] = Field(None, description="Structured details for renewal option")
    yearly_rent_increase_percentage: Optional[float] = Field(
        None, description="Yearly rent increase percentage (e.g., 0.05 for 5%)"
    )
    termination_conditions: Optional[str] = Field(None, description="Conditions and rights regarding early termination")


class Rent(BaseModel):
    base_rent: Optional[float] = Field(None, description="Monthly base rent amount", ge=0)
    rent_calculation_method: Optional[str] = Field(
        None, description="Method for calculating rent (e.g., 'square footage', 'fixed amount')"
    )
    currency: Optional[str] = Field(
        None, description="Three-letter currency code (e.g., USD) for the base rent", pattern="^[A-Z]{3}$"
    )
    frequency: Optional[PaymentFrequency] = Field(None, description="Payment frequency (e.g., monthly, quarterly)")
    adjustments: Optional[str] = Field(None, description="Details about any adjustments or increases to rent")


class SecurityDeposit(BaseModel):
    amount: Optional[float] = Field(None, description="Security deposit amount", ge=0)
    currency: Optional[str] = Field(
        None, description="Three-letter currency code (e.g., USD) for the security deposit", pattern="^[A-Z]{3}$"
    )
    return_timeline: Optional[str] = Field(
        None,
        description="Number of days for the return of the security deposit (e.g., '30 days after the lease end date')",
    )
    conditions: Optional[str] = Field(None, description="Conditions regarding the use and return of the deposit")


class PercentageRent(BaseModel):
    rate: Optional[float] = Field(None, description="Percentage rate for additional rent (e.g., 0.15 for 15%)")
    basis: Optional[str] = Field(None, description="Basis on which percentage rent is calculated")
    frequency: Optional[str] = Field(
        None, description="Frequency of percentage rent payments (e.g., weekly, monthly, quarterly)"
    )


class LateFees(BaseModel):
    fee_amount: Optional[float] = Field(None, description="Late fee amount")
    currency: Optional[str] = Field(
        None, description="Three-letter currency code (e.g., USD) for the late fee", pattern="^[A-Z]{3}$"
    )
    calculation_method: Optional[str] = Field(None, description="Method for calculating late fees")
    grace_period: Optional[str] = Field(None, description="Any applicable grace period for late payments in days")
    interest_rate: Optional[float] = Field(
        None, description="Interest rate applied on overdue payments (e.g., 0.15 for 15%)"
    )
    frequency: Optional[str] = Field(None, description="Frequency of late fees (e.g., daily, weekly, monthly)")
    waiver_conditions: Optional[str] = Field(None, description="Conditions under which late fees may be waived")


class PaymentSchedule(BaseModel):
    payment_method: Optional[PaymentMethod] = Field(None, description="Payment method")
    payment_due_day: Optional[int] = Field(None, description="Day of month payment is due", ge=1, le=31)
    additional_details: Optional[str] = Field(None, description="Any additional payment instructions")


class AdditionalCharges(BaseModel):
    property_expenses: Optional[str] = Field(
        None, description="Other property expenses (e.g., real estate taxes, CAM charges, insurance)"
    )
    details: Optional[str] = Field(None, description="Breakdown or further description of additional charges")


class FinancialTerms(BaseModel):
    rent: Optional[Rent] = Field(None, description="Rent details")
    security_deposit: Optional[SecurityDeposit] = Field(None, description="Security deposit details")
    percentage_rent: Optional[PercentageRent] = Field(None, description="Percentage rent details")
    payment_schedule: Optional[PaymentSchedule] = Field(None, description="Payment schedule")
    late_fees: Optional[LateFees] = Field(None, description="Late fees")
    additional_charges: Optional[AdditionalCharges] = Field(None, description="Additional charges")


class Utilities(BaseModel):
    responsibility: Optional[str] = Field(None, description="Party responsible for utility payments")
    service_interruption_liability: Optional[str] = Field(
        None, description="Liability provisions for interruption or failure of utility services"
    )


class CommonAreas(BaseModel):
    description: Optional[str] = Field(None, description="Description of common areas included in the lease")
    management: Optional[str] = Field(None, description="Party responsible for managing common areas")
    usage_rules: Optional[str] = Field(None, description="Rules and restrictions for use of common areas")


class Signage(BaseModel):
    signage_requirements: Optional[str] = Field(None, description="Requirements for signage as set forth in the lease")
    approval_required: Optional[bool] = Field(None, description="Indicates if signage approval is required")


class MaintenanceAndRepairs(BaseModel):
    landlord_responsibility: Optional[str] = Field(
        None, description="Maintenance and repair responsibilities of the landlord"
    )
    tenant_responsibility: Optional[str] = Field(
        None, description="Maintenance and repair responsibilities of the tenant"
    )
    common_area_maintenance: Optional[str] = Field(None, description="Maintenance responsibilities for common areas")
    special_conditions: Optional[str] = Field(
        None, description="Any special provisions regarding maintenance and repairs"
    )
    repair_fund_details: Optional[str] = Field(
        None, description="Details on repair or restoration funds, if applicable"
    )


class ImprovementsAndAlterations(BaseModel):
    permitted_improvements: Optional[str] = Field(None, description="Conditions for making improvements or alterations")
    approval_requirements: Optional[str] = Field(None, description="Approval requirements for alterations")


class SublettingAndAssignment(BaseModel):
    allowed: Optional[bool] = Field(None, description="Indicator if subletting/assignment is allowed")
    restrictions: Optional[str] = Field(None, description="Any restrictions or conditions for subletting/assignment")
    assignment_notice_period: Optional[int] = Field(
        None, description="Notice period in days required for assignment or subletting"
    )
    assignment_costs: Optional[str] = Field(
        None, description="Details of any costs associated with assignment or subletting"
    )


class DefaultAndRemedies(BaseModel):
    events_of_default: Optional[str] = Field(None, description="Conditions that constitute default")
    notice_period: Optional[int] = Field(
        None, description="Required notice period in case of default in days (e.g., 30 days)"
    )
    remedies: Optional[str] = Field(None, description="Available remedies and dispute resolution methods")
    attorney_fees: Optional[float] = Field(None, description="Attorney fees if applicable")


class Indemnification(BaseModel):
    tenant_indemnification: Optional[str] = Field(None, description="Tenant's indemnification obligations")
    landlord_indemnification: Optional[str] = Field(None, description="Landlord's indemnification obligations")


class MiscellaneousProvisions(BaseModel):
    notices: Optional[str] = Field(None, description="Provisions regarding notices")
    amendments: Optional[str] = Field(None, description="Process for amendments to the lease")
    binding_effect: Optional[str] = Field(None, description="Binding effect and governing law")
    additional_clauses: Optional[str] = Field(None, description="Any additional clauses or miscellaneous provisions")
    miscellaneous_clauses: Optional[str] = Field(None, description="Additional free-text clauses as needed")


class Insurance(BaseModel):
    liability_coverage: Optional[float] = Field(None, description="Required liability insurance coverage amount")
    property_coverage: Optional[float] = Field(None, description="Required property insurance coverage amount")
    currency: Optional[str] = Field(
        None, description="Three-letter currency code (e.g., USD) for the insurance coverage", pattern="^[A-Z]{3}$"
    )
    additional_insureds: Optional[List[str]] = Field(None, description="Required additional insured parties")
    certificate_requirements: Optional[str] = Field(None, description="Insurance certificate requirements")


class LeaseAgreement(BaseModel):
    parties: Parties = Field(..., description="Details for the Landlord and Tenant")
    property_details: PropertyDetails = Field(..., description="Details of the leased property")
    lease_term: Optional[LeaseTerm] = Field(None, description="Lease term information")
    financial_terms: Optional[FinancialTerms] = Field(
        None, description="All financial terms including payment instructions"
    )

    utilities: Optional[Utilities] = Field(None, description="Utility service details")
    common_areas: Optional[CommonAreas] = Field(None, description="Common areas information")
    signage: Optional[Signage] = Field(None, description="Signage requirements and approval details")
    insurance: Optional[Insurance] = Field(None, description="Insurance requirements")
    maintenance_and_repairs: Optional[MaintenanceAndRepairs] = Field(None, description="Maintenance responsibilities")
    improvements_and_alterations: Optional[ImprovementsAndAlterations] = Field(None, description="Alterations clauses")
    subletting_and_assignment: Optional[SublettingAndAssignment] = Field(None, description="Subletting conditions")
    default_and_remedies: Optional[DefaultAndRemedies] = Field(None, description="Default and remedies")
    indemnification: Optional[Indemnification] = Field(None, description="Indemnification terms")
    dispute_resolution: Optional[str] = Field(None, description="Preferred method of dispute resolution")
    miscellaneous: Optional[MiscellaneousProvisions] = Field(None, description="Miscellaneous provisions")
