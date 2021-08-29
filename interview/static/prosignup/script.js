$(document).ready(function(){

  // remove required from all the lements
  $('#id_company').removeAttr('required');
  $('#id_designation').removeAttr('required');
  $('#id_project').removeAttr('required');
  $('#id_from_Month').removeAttr('required');
  $('#id_from_Year').removeAttr('required');
  $('#id_to_Month').removeAttr('required');
  $('#id_to_Year').removeAttr('required');



  $(document).delegate('#butn', 'click', function()
  {

      $('#company'+ $(this).attr('name')).remove();
      $('#designation'+ $(this).attr('name')).remove();
      $('#project'+ $(this).attr('name')).remove();
      $('#from'+ $(this).attr('name')).remove();
      $('#to'+ $(this).attr('name')).remove();
      $(this).remove();

    });

  });


  
  $(document).ready(function(){

    var mon = ['','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    $("#add").click(function(){
      var company =     $("#id_company").val();
      var designation = $('#id_designation').val();
      var project =     $('#id_project').val();
      var from =        mon[$('#id_from_Month').val()]  + ' ' + $('#id_from_Year').val();
      var to =          mon[$('#id_to_Month').val()]  + ' ' + $('#id_to_Year').val();


      console.log($('#id_to_Year').val());


      $('#expcard').append('<cdiv class="go" id="butn" name="'+ window.cardno +'"><br>'+
        '<h3>'+  company +'</h3>'+
        '<h1>'+ designation +'</h1>'+
        '<p>'+ project +'</p>'+
        '<span>'+ from + '  -  ' + to +'</span>'+
        '<br>'+
        '</cdiv>');

      $('#invisible').append("<input name='company"+ window.cardno+ "'  id='company"+ window.cardno+ "' value='"+ company +"' style='display:none'></input>")
      $('#invisible').append("<input name='designation"+ window.cardno+ "'  id='designation"+ window.cardno+ "'  value='"+ designation +"' style='display:none'></input>")
      $('#invisible').append("<input name='project"+ window.cardno+ "'  id='project"+ window.cardno+ "' value='"+ project +"' style='display:none'></input>")
      $('#invisible').append("<input name='from"+ window.cardno+ "'  id='from"+ window.cardno+ "' value='"+ mon[$('#id_from_Month').val()]+','+ JSON.stringify($('#id_from_Year').val()) +"' style='display:none'></input>")
      $('#invisible').append("<input name='to"+ window.cardno+ "' id='to"+ window.cardno+ "' value='" + mon[$('#id_to_Month').val()]+','+ JSON.stringify($('#id_to_Year').val()) +"' style='display:none'></input>")
      
      // variable to record the numbers of card we have
      
      window.cardno = window.cardno + 1;

      //to reset the values of input afer adding new card
      $("#id_company").val('');
      $('#id_designation').val('');
      $('#id_project').val('');
      $('#id_from_Year').val(null) ;
      $('#id_to_Year').val(null) ;



    

        

    });
  });


 
console.log("Started");










/*

@login_required
def pro_bank(request, edit = 0):
    # edit = 1 is for updating the bank details
    form = ProfessionalBankForm()
    prof = Prfessional.objects.get(user__username = request.user)

    if edit == 1:
      
      form.initial['ifsc']              = prof.pro_bank_account.ifsc
      form.initial['account_number']    = prof.pro_bank_account.account_number
      form.initial['name']              = prof.pro_bank_account.name
      form.initial['upi']               = prof.pro_bank_account.upi

    
    if request.method == 'POST':
        form = ProfessionalBankForm(request.POST)
        if form.is_valid():
          if Prfessional.objects.filter(user__username = request.user).count == 0:
              return HttpResponse('Sorry you are not signed up for porfessional person')

          pro = Professinal_Account_Details()

          if edit == 1:
            pro = prof.pro_bank_account
            

          if Professinal_Account_Details.objects.filter(pro = Prfessional.objects.get(user__username = request.user)).count() != 0:
              pro = Professinal_Account_Details.objects.get(pro = Prfessional.objects.get(user__username = request.user))
          

              
          pro.pro  = Prfessional.objects.get(user__username = request.user)
          pro.ifsc =           form.cleaned_data['ifsc']
          pro.account_number = form.cleaned_data['account_number']
          pro.name =           form.cleaned_data['name']
          pro.upi  =           form.cleaned_data['upi']
          
          pro.save()

          return redirect('pro_dashboard')
    
    return render(request,'form.html',context={'form':form})


*/