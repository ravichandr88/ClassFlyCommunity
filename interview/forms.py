from django import forms
from .models import Experience,Professinal_Account_Details
 


#Class to add Bootstrap for input fields in HTML
class BootstrapModelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        place_holder = getattr(self.Meta, 'place_holder', dict())

        for field_name, field in self.fields.items():
            # add form-control class to all fields
            

            if field_name != 'about_yourself' and field_name != 'about' and field_name !='address' and field_name !='project' and field_name != 'exp_work_1'and field_name != 'exp_work_2'and field_name != 'exp_work_3':
                
                field.widget.attrs['class'] = 'input100'
            
           
           
           
            if field_name in icons:
                field.icon = icons[field_name]

            if field_name in place_holder:
                field.widget.attrs['placeholder'] = place_holder[field_name]
            
            if field_name == 'resume':
                field.widget.attra['accept'] = "application/pdf"

            if field_name == 'idcard':
                field.widget.attra['accept'] = "image/*"
            
            
class StudentForm(BootstrapModelForm):

    pre_college = forms.CharField(label='Pre University/ Diploma College',required = True,max_length=40)
    pre_branch  = forms.CharField(label='PreUniversity/Diploma Branch',required = True,max_length = 50)
    city_1       = forms.CharField(label="Place of study", max_length = 30, required = True)
    pre_passout = forms.CharField(label='PreUniversity/Diploma Passout Year',required = False, widget=forms.TextInput(attrs={'min':2010,'max': 2030,'type': 'number'}))
    college = forms.CharField(max_length=40,required = True)
    city_2       = forms.CharField(label="Place of study", max_length = 30, required = True)
    branch = forms.CharField(max_length = 50,required = False)
    language_spoke = forms.CharField(label='Language Spoken(Enter comma seperated',max_length = 60)
    passout_year = forms.CharField(label='Passout Year',required = False, widget=forms.TextInput(attrs={'min':2016,'max': 2030,'type': 'number'}))
    master_college = forms.CharField(label='Master Degree College',max_length=40, required = False)
    city_3      = forms.CharField(label="Place of study", max_length = 30, required = False)
    master_branch = forms.CharField(label='Master Branch',max_length = 50, required = False)
    master_passout = forms.CharField(label='Master Degree Passout Year', required = False ,widget=forms.TextInput(attrs={'min':2016,'max': 2030,'type': 'number'}))
    about_yourself = forms.CharField(required=False,max_length=500, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'id':"exampleFormControlTextarea1"}))
    city           = forms.CharField(label='Current Living Place',max_length = 50, required = True)
    total_experience = forms.CharField(label='Experience in Months', widget=forms.TextInput(attrs={'min':2,'max': 48,'type': 'number'}))
    about_yourself = forms.CharField(required=False,max_length=500, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'id':"exampleFormControlTextarea1"}))
    exp_company_1 = forms.CharField(max_length=80, required=False)
    exp_work_1 = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Technologies used and project done."}))
    exp_period_1 = forms.CharField(label='From - To Date',max_length=40, required=False)
    exp_company_2 = forms.CharField(max_length=80, required=False) 
    exp_work_2 = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Technologies used and project done."}))
    exp_period_2 = forms.CharField(label='From - To Date',max_length=40, required=False)
    exp_company_3 = forms.CharField(max_length=80, required=False)
    exp_work_3 = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Technologies used and project done."}))
    exp_period_3 = forms.CharField(label='From - To Date',max_length=40,required=False)
    

    def exp(self,n):
        if len(self.cleaned_data['exp_company_'+str(n)]) == 0 and len(self.cleaned_data['exp_work_'+str(n)]) and len(self.cleaned_data['exp_period_'+str(n)]) == 0:
            
            return 0

        return Experience(
            exp_company = self.cleaned_data['exp_company_'+str(n)],
            exp_work = self.cleaned_data['exp_work_'+str(n)],
            exp_period = self.cleaned_data['exp_period_'+str(n)]
        )
    



    class Meta:
        fields = ['college','branch','passout_year','about_yourself','exp_company_1','exp_work_1','exp_period_1','exp_company_2','exp_work_2','exp_period_2','exp_company_3','exp_work_3','exp_period_3']
        icons = {'password1': 'fa fa-lock','username':'fa fa-mobile','password2':'fa fa-lock','first_name':'fa fa-user'}
        place_holder = {'language_spoke':'English, Telugu, ','total_experience':"Months",'exp_period_1':'2 July 2016 - 3 March 2017','exp_period_2':'2 July 2016 - 3 March 2017','exp_period_3':'2 July 2016 - 3 March 2017','branch':"Branch"}
    
    class Media:
        js =("studentacc/tagscript.js",)
       

# class ResumeForm(forms.Form):
#     resume = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))


# class HRIDForm(forms.Form):
#     idcard = forms.FileField(widget=forms.FileInput(attrs={'accept':"image/*"}))



# https://stackoverflow.com/questions/50380769/how-to-create-a-autocomplete-input-field-in-a-form-using-django


class ProfessionalForm(BootstrapModelForm):
    # user 
    company         = forms.CharField(max_length=70, required=True)
    designation     = forms.CharField(max_length=60, required=True)
    city            = forms.CharField(max_length=60, required=True)
    college         = forms.CharField(max_length=80, required=True)
    stream          = forms.CharField(max_length=80, required=True)
    language_spoke  = forms.CharField(max_length = 150,required=True)
    about_yourself  = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"About Yourself"}))
    total_exp_year  = forms.CharField(label='Total Experience  Years', widget=forms.TextInput(attrs={'min':2,'max': 48,'type': 'number'}))
    total_exp_month = forms.CharField(label='Experience  Months(Optional)', widget=forms.TextInput(attrs={'min':0,'max': 12,'type': 'number','value':0}))
    
    class Meta:
        fields = ('company','designation','city','college','stream','language_spoke','about_yourself','total_exp_year','total_exp_month','experience')
        place_holder = {'stream':"MCA , BCA",'college':'College Name','language_spoke':'English, Hindi,'}
    
    class Media:
        js =("studentacc/tagscript.js",)
       


RELEVANCE_CHOICES=(
    (1,'JAN'),
    (2,'FEB'),
    (3,'MAR'),
    (4,'APR'),
    (5,'MAY'),
    (6,'JUN'),
    (7,'JUL'),
    (8,'AUG'),
    (9,'SEP'),
    (10,'OCT'),
    (11,'NOV'),
    (12,'DEC'),
)

class Experienc(BootstrapModelForm): 
    company = forms.CharField(max_length=60)
    designation = forms.CharField(max_length=60)
    project = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Work details"}))
    from_Month =  forms.ChoiceField(choices = RELEVANCE_CHOICES)
    from_Year = forms.CharField(label='From Year', widget=forms.TextInput(attrs={'min':2000,'max': 2022,'type': 'number'}))
    to_Month =  forms.ChoiceField(choices = RELEVANCE_CHOICES)
    to_Year = forms.CharField(label='To Year', widget=forms.TextInput(attrs={'min':2000,'max': 2022,'type': 'number'}))
    
    class Meta:
        fields = ('company','project','fromMonth')



class DateInput(forms.DateInput):
    input_type = 'date'



#Form to get professional initial meeting available timings,
class ProIntervTime(BootstrapModelForm):
    meet1_date  = forms.DateTimeField(widget = DateInput, required=False)
    meet1_time  = forms.TimeField(input_formats=["%H.%M.%S", "%H.%M"], required=False)
    meet2_date  = forms.DateTimeField(widget = DateInput, required=False)
    meet2_time  = forms.TimeField(input_formats=["%H.%M.%S", "%H.%M"], required=False)
    meet3_date  = forms.DateTimeField(widget = DateInput, required=False)
    meet3_time  = forms.TimeField(input_formats=["%H.%M.%S", "%H.%M"], required=False)

    class Meta:
        fields = ('meet1_date','meet1_time','meet2_date','meet2_time','meet3_date','meet3_time')

    class Media:
        js =("profinterview/script.js",)



class CompanyForm(BootstrapModelForm):
    company_name = forms.CharField(max_length = 100,required=True)
    about = forms.CharField(label="About Copmany(500 length )",max_length = 800,required=True, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"About Company "}))
    address = forms.CharField(label='Copmplete Address ',max_length = 500,required=True, widget=forms.Textarea(attrs={'rows': 5,'class' : 'form-control','style':"color: #666666;background: #e6e6e6;",'placeholder':"Company Address"}))    
    city = forms.CharField(max_length=50,required=True)
    state = forms.CharField(max_length = 100, required=True)
    company_linkedin_url = forms.URLField() 

    class Meta:
        fields = ('company_name','address','city','company_linkedin_url')


#This is the initial hr crating company account and only once is used
class HRForm(BootstrapModelForm):
    designation      = forms.CharField(max_length = 50,required=True)
    linkedin_url     = forms.URLField() 
    

    class Meta:
        fields = ('designation', 'linkedin_url','office_email')


WEEK_DAYS =(
    ('MON','MON'),
    ('TUE','TUE'),
    ('WED','WED'),
    ('THU','THU'),
    ('FRI','FRI'),
    ('SAT','SAT'),
    ('SUN','SUN'),
    ('NULL','NULL')
)

class ProfTimeTableForm(BootstrapModelForm):
    day = forms.ChoiceField(choices = WEEK_DAYS) 
    time  = forms.TimeField(input_formats=["%H.%M.%S", "%H.%M"], required=False)

    class Meta:
        fields = ('day','time')
    
    class Media:
        js =("profinterview/timetable.js",)

    
class ProfessionalBankForm(BootstrapModelForm):
    ifsc = forms.CharField(max_length=11, required = True)
    account_number = forms.CharField(max_length=18, required = True)
    name = forms.CharField(max_length = 40, required = True)
    upi  = forms.CharField(max_length = 40)


    class Meta:
        fields = ('name','ifsc','account_number','upi')
