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
            

class MeetingFeedbackForm(BootstrapModelForm):
    feedback =forms.CharField( max_length = 1000 ,required=True,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Regarding every skills interviewed"}) )
    skills   = forms.CharField(max_length = 500,required=True,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Skills which are good(Seperated with comma)."}))
    result   = forms.ChoiceField(label='Result',required = True, choices=[('pass','Passed'),('fail','Failed')],widget=forms.RadioSelect( attrs={}) )
    
    class Meta:
        fields = ('feedback','result','skills')
        place_holder = {}
