from django import forms

# Reordering Form and View


class PositionForm(forms.Form):
    name = forms.CharField(required = True)

    name.widget.attrs.update({'class': "form-control d-xl-flex flex-grow-1 align-items-center align-content-center justify-content-xl-center align-items-xl-center form-control ps-4 pe-4 rounded-pill", 'type': "text", 'name': "search", 'placeholder': "Search..."})