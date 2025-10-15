
var lock = new PatternLock("#patternContainer",{
   onDraw:function(pattern){
      word();
    }
});
var lock1 = new PatternLock("#patternContainer1",{
   onDraw:function(pattern){
      word1();
    }
});
var lock2 = new PatternLock("#patternContainer2",{
   onDraw:function(pattern){
      word2();
    }
});
function word()
{
  var pat=lock.getPattern();
  $("#patterncode").val(pat);
  $('#patterncode').valid()
}
function word1()
{
 var pat=lock1.getPattern();
  $("#id_old_pattern").val(pat);
  $('#id_old_pattern').valid()
}
function word2()
{
 var pat=lock2.getPattern();
  $("#id_pattern").val(pat);
  $('#id_pattern').valid()
}
$(document).ready(function(){
  setTimeout(function() {
    $('.alert').fadeOut('fast');
  }, 3000); // <-- time in milliseconds
});

$('#login_form').validate({
  ignore:"",
  rules:{
    username:{
      required:true,
      // validEmail:true,
    },
    password:{
      required:true,
    },
    pattern_code:{
      required:true,
    }
  },
  messages:{
     username:{
      required:"Enter Email",
      // remote:"Email not exists",
    },
    password:{
      required:"Enter password",
    },
    pattern_code:{
      required:"Draw pattern",
    }
  }
});


$('#changepatternid').validate({
  ignore:"",
  rules:{
    
    old_pattern_code:{
      required:true,
    },
    pattern_code:{
      required:true,
    }
  },
  messages:{
   
    old_pattern_code:{
      required:"Draw Old Pattern",
    },
    pattern_code:{
      required:"Draw New pattern",
    }
  }
});


function login_loader_show(){ 
 if ($('#login_form').valid() == true) {
   $('#login_submit').attr('disabled',true);
   $('#login_submit').html('Loading <i class="fa fa-spinner fa-spin"></i>');
   } else {
   $('#login_submit').attr('disabled',false);
   $('#login_submit').html("Submit");
   }
}

