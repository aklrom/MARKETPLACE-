from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=[
            "text",
            "rating"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget=field.widget
            if isinstance(widget,forms.CheckboxInput):
                widget.attrs["class"]="form-check-input"
            elif isinstance(widget, forms.Select):
                widget.attrs["class"]="form-select"
            else:
                widget.attrs["class"]="form-control"
        self.fields["text"].widget.attrs["rows"]=4                    