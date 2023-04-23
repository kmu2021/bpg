from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_duns(value):
    if len(str(value)) != 9:
        raise ValidationError(_("DUNS must be 9 digits in length"),
                              params={"value": value},
                              )
# Create your models here.

# creating a form


class RegistrationForm(forms.Form):

    firstName = forms.CharField(max_length=50, min_length=2, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'First Name', 'placeholder': "Enter First Name", 'oninvalid': 'this.setCustomValidity("First Name should be 2-50 characters in length")', 'oninput': 'setCustomValidity("")'}))
    lastName = forms.CharField(max_length=50, min_length=2, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'Last Name', 'placeholder': "Enter Last Name", 'oninvalid': 'this.setCustomValidity("Last Name should be 2-50 characters in length")', 'oninput': 'setCustomValidity("")'}))
    workEmail = forms.EmailField(max_length=100, label='Work Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Work Email', 'placeholder': "Enter Work Email"}))
    company = forms.CharField(max_length=100, label='Company', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Company', 'placeholder': "Enter Company"}))
    scac = forms.CharField(min_length=2, max_length=4, label='SCAC', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'SCAC', 'placeholder': "Enter SCAC", 'oninvalid': 'this.setCustomValidity("SCAC should be 2-4 characters in length")', 'oninput': 'setCustomValidity("")'}))
    duns = forms.IntegerField(validators=[validate_duns], label='DUNS', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'DUNS', 'placeholder': "Enter DUNS"}))

    tncFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input checkbox-xl'}),
        required=True
    )


class UserMgmtSearchForm(forms.Form):
    lastName = forms.CharField(max_length=200, required=False, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Last Name', 'placeholder': "Search by Last Name"}))
    firstName = forms.CharField(max_length=200, required=False, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control search-form',  'aria-label': 'First Name', 'placeholder': "Search by First Name"}))
    workEmail = forms.CharField(max_length=400, required=False, label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Email', 'placeholder': "Search by Email"}))
    company = forms.CharField(max_length=200, required=False, label='Company', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Company', 'placeholder': "Search by Company"}))
    scac = forms.CharField(max_length=200, required=False, label='SCAC', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'SCAC', 'placeholder': "Search by SCAC"}))
    duns = forms.CharField(max_length=200, required=False, label='DUNS', widget=forms.TextInput(
        attrs={'class': 'form-control search-form',  'aria-label': 'DUNS', 'placeholder': "Search by DUNS"}))

    pendingInvitationFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Pending Invitation'}),
        required=False, label='Pending Invitation'
    )


class UserAccessControlForm_Old(forms.Form):
    activeUserFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Active User', 'data-group-name': 'NAT_AZURE'}),
        required=False, label='Active User'
    )
    adminFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Administrator'}),
        required=False, label='Administrator'
    )
    supplierContractsFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Supplier & Contracts'}),
        required=False, label='Supplier & Contracts'
    )

    manageMyRatesFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Manage My Rates'}),
        required=False, label='Manage My Rates'
    )

    sourcingEventsFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Sourcing Events'}),
        required=False, label='Sourcing Events'
    )

    manageMyTripsFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Manage My Trips'}),
        required=False, label='Manage My Trips'
    )

    transReportsFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Trans Reports'}),
        required=False, label='Trans Reports'
    )

    assesorialChargesFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Assesorial Charges'}),
        required=False, label='Assesorial Charges'
    )

    gpsTrackingFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'GPS Tracking'}),
        required=False, label='GPS Tracking'
    )

    electronicMessagingFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Electronic Messaging'}),
        required=False, label='Electronic Messaging'
    )


class UserAccessControlForm(forms.Form):
    activeUserFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Active User'}),
        required=False, label='Active User'
    )

    resendInvitationFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Resend Invitation'}),
        required=False, label='Resend Invitation'
    )

    adminFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Administrator'}),
        required=False, label='Administrator'
    )

    logisticsGatewayFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Logistics Gateway', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_BPG_ILE'}),
        required=False, label='Logistics Gateway'
    )
    freightAuctionFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Freight Auction', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_FA_ILE'}),
        required=False, label='Freight Auction'
    )

    stafFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'Surface Transportation', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_STAF_ILE'}),
        required=False, label='Surface Transportation'
    )

    clearSupplierFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'CLEAR Supplier Management', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_CLEAR_ILE'}),
        required=False, label='CLEAR Supplier Management'
    )

    clearRateFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'CLEAR Rate Management', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_CLEAR_ILE'}),
        required=False, label='CLEAR Rate Management'
    )

    fourKitesFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'aria-label': 'GPS Tracking', 'data-group-initial-status': "False", 'data-group-name': 'NAT_AZURE_FOURKITES_ILE'}),
        required=False, label='GPS Tracking'
    )


class UserDetails:
    uid: int
    user_id: str
    firstName: str
    lastName: str
    workEmail: str
    company: str
    scac: str
    duns: str
    invitationStatus: str
    supplierId: str
    responseText: str


class EmailDetail:
    email: str
    isVerified: bool
    counter: int
