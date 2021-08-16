from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
import re
from user.models import OTP,Phonenumber



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
            
            

            
           
            if field_name != 'description' and field_name != 'requirement' and field_name != 'skills' and field_name != 'question1' and field_name != 'question2' and field_name != 'question3':
                
                # add form-control class to all fields
                field.widget.attrs['class'] = 'input100'
            

class JobPostForm(BootstrapModelForm):

    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        self.fields['min_salary'].widget.attrs['min'] = 100000
        self.fields['max_salary'].widget.attrs['min'] = 300000
        self.fields['min_experience'].widget.attrs['min'] = 0
        self.fields['max_experience'].widget.attrs['min'] = 0
        self.fields['min_experience'].widget.attrs['max'] = 3
    
    designation     = forms.CharField( max_length = 60 , required = True )
    role            = forms.CharField(max_length = 60, required = True )
    industry_type   = forms.CharField(max_length = 60, required = True )
    employment_type = forms.CharField(max_length = 60, required = True )
    edu_ug          = forms.CharField(max_length = 60, required = True )
    edu_pg          = forms.CharField(max_length = 60, required = True )
    edu_doc         = forms.CharField(max_length = 60, required = True )
    city            = forms.CharField(max_length = 100, required = True)
    skills          = forms.CharField( max_length = 150 ,required=True, widget=forms.Textarea(attrs={'rows': 2,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Skills Set"}) )
    description     = forms.CharField(max_length = 800 ,required=True, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Description about the Job Role."}) )
    requirement     = forms.CharField( max_length = 800 ,required=True,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Requirement"})) 
    min_experience  = forms.IntegerField(required=True) 
    max_experience  = forms.IntegerField(required=True) 
    min_salary      = forms.FloatField(required=True) 
    max_salary      = forms.FloatField(required=True) 
    question1       = forms.CharField( max_length = 400 ,required=False, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;","type":'text','value':"(Optional) Recognisable task done in related Job?"}) )
    question2       = forms.CharField( max_length = 400 ,required=False,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"(Optional)Any sample work to submit?"}) )
    question3       = forms.CharField( max_length = 400 ,required=False,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"(Optional)Any sample work to submit?"}) )


    class Meta:
        fields = ('designation', 'skills', 'description','city', 'requirement', 'min_experience','max_experience','min_salary','max_salary','role', 'industry_type', 'employment_type' ,   'edu_ug',  'edu_pg' ,'edu_doc', 'question1','question2','question3')
        place_holder = {
        'designation':'Django/Backend Developer', 
        'skills':'Python,SQl,..',
        'description':'About the job',
        'requirement':'Requirements about the candidate',
        'min_experience':'Years',
        'max_experience': 'Years',
        'min_salary' : 'Minimum Salary Per Anum',
        'max_salary' : 'Maximum salary Per Anum',
        'role'      :  'Role Defined',
    'industry_type':  'Industry Type',
    'employment_type' : 'Permanent or Contract',
    'edu_ug'   :        'Under Gradutae Stream',
    'edu_pg'    :      'Post Graduate Stream',
    'edu_doc' :     'Docrate required or not',
    'city'  : 'Online / City Name'
        }



class JobApplyForm(BootstrapModelForm):

    def __init__(self, ques1='', ques2='', ques3='', *args, **kwargs):
        super(JobApplyForm, self).__init__(*args, **kwargs)
        self.fields['question1'].label = ques1
        self.fields['question2'].label = ques2
        self.fields['question3'].label = ques3


    question1       = forms.CharField( max_length = 400 ,required=False, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;","type":'text','value':"(Optional) Recognisable task done in related Job?"}) )
    question2       = forms.CharField( max_length = 400 ,required=False,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"(Optional)Any sample work to submit?"}) )
    question3       = forms.CharField( max_length = 400 ,required=False,widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"(Optional)Any sample work to submit?"}) )
    
    class Meta:
            fields = ( 'question1','question2','question3')
            place_holder = {
                'question1':'What to do now',
                'question2':'What to dno t onow',
                'question3':'What happend'
            }


