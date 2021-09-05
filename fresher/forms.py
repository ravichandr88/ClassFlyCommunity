from django import forms



#Class to add Bootstrap for input fields in HTML
class BootstrapModelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        place_holder = getattr(self.Meta, 'place_holder', dict())

        
        for field_name, field in self.fields.items():
            # code to placholder assign
            if field_name in place_holder:
                field.widget.attrs['placeholder'] = place_holder[field_name]
             
           
            if field_name != 'technologies' and field_name != 'date_time' :
                
                # add form-control class to all fields
                field.widget.attrs['class'] = 'input100'
            


class ClassFlyInterviewForm(BootstrapModelForm):
    designation  =    forms.CharField(max_length = 50, label = 'Designation',required = True)
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
        place_holder = {
                'designation':'What position',
                'price':'Total Price'
            }
        

    class Media:
        js = ('booking/book_interview.js',)
