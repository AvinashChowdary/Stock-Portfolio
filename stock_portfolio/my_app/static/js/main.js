jQuery(function(){
    
    var temp, j , i, obj , flag = false;

    jQuery('.calculate-side-form').on('submit',function(e){
        
        flag = false;    

        if( jQuery.trim(jQuery('#amount').val())  === "") {
            flag = true;
            temp = 'Please enter amount to invest' ;
        }else if( jQuery.trim(jQuery('#amount').val()) < 5000) {
            flag = true;
            temp = 'Please enter amount greater than $5000';
        }

        i = 0;
        jQuery('.investment_choices_area input[type="checkbox"]').each(function(){

             if( jQuery(this).is(':checked') )
                i++;

        });

        if(i > 2) {
             temp = 'You can select only 2 options atmost';
             flag = true;   
        }

         if(i === 0) {
             temp = 'Please select atleast one option';
             flag = true;   
        }


       if(flag === true) {
            alert(temp)

            return false; 
       }    

       
        
    })
         jQuery('.steps li').each(function(i){


                jQuery(this).css({

                    "-webkit-animation-duration" : (i+0.5)*0.4+"s",
                    "animation-duration" : (i+0.5)*0.4+"s",

                });

         });

         jQuery('.steps li').addClass('fadeInLeft'); 

});


