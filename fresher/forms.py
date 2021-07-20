from django import forms

class ClassFlyInterviewForm(forms.Form):
    technologies =    forms.MultipleChoiceField(required = True, choices=[],widget=forms.CheckboxSelectMultiple( attrs={'onclick':"skill(value)"}) )
    date_time    =    forms.MultipleChoiceField(required = True, choices=[],widget=forms.RadioSelect( attrs={'onclick':"meet(value)"}))
    price        =    forms.IntegerField(required = True)

    def __init__(self,skills, dates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # waypoint_choices = [(o.id, str(o)) for o in Waypoint.objects.filter(user=user)]
        waypoint_choices = [(i,i) for i in skills.split(',')]
        self.fields['technologies'].choices = waypoint_choices

        self.fields['date_time'].choices = dates

    class Meta:
        fields = ('technologies','date_time','price')

    class Media:
        js = ('booking/book_interview.js',)
