function enable_disable_submit(){
    if(document.getElementById('no_clue').checked ||
    document.getElementById('con_move').checked ||
    document.getElementById('uncon_move').checked ||
    document.getElementById('dir_affs').checked ||
    document.getElementById('indir_affs').checked ||
    document.getElementById('observe_affs').checked ||
    document.getElementById('social_affs').checked ||
    document.getElementById('no_affs').checked
    ){
    document.getElementById('main_form_submit').disabled = false;
    document.getElementById('submit_message').hidden = true;
    } else{
    document.getElementById('submit_message').hidden = false;
    document.getElementById('main_form_submit').disabled = true;
    }
}

$(".con_move").change(function(){
    if(this.checked) {
    document.getElementById('con_move').checked = true;
    }
    enable_disable_submit();
});

$(".uncon_move").change(function(){
    if(this.checked) {
    document.getElementById('uncon_move').checked = true;
    }
    enable_disable_submit();
});

$(".dir_affs").change(function(){
    if(this.checked) {
    document.getElementById('dir_affs').checked = true;
    }
    enable_disable_submit();
});

$(".indir_affs").change(function(){
    if(this.checked) {
    document.getElementById('indir_affs').checked = true;
    }
    enable_disable_submit();
});

$(".observe_affs").change(function(){
    if(this.checked) {
    document.getElementById('observe_affs').checked = true;
    }
    enable_disable_submit();
});

$(".social_affs").change(function(){
    if(this.checked) {
    document.getElementById('social_affs').checked = true;
    }
    enable_disable_submit();
});

$(".no_affs").change(function(){
    if(this.checked) {
    document.getElementById('no_affs').checked = true;
    }
    enable_disable_submit();
});

$(document.getElementById('con_move')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".con_move").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('uncon_move')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".uncon_move").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('dir_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".dir_affs").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('indir_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".indir_affs").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('observe_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".observe_affs").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('social_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".social_affs").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('no_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".no_affs").each(function(){
        this.checked = false;
    })
    }
});

$(document.getElementById('main_form_submit')).click(function(){
    if(document.getElementById('no_clue').checked ||
    document.getElementById('con_move').checked ||
    document.getElementById('uncon_move').checked ||
    document.getElementById('dir_affs').checked ||
    document.getElementById('indir_affs').checked ||
    document.getElementById('observe_affs').checked ||
    document.getElementById('social_affs').checked ||
    document.getElementById('no_affs').checked
    ){
    document.getElementById('mainform').submit();
    }
});

$(document).ready(function() {
    document.getElementById('main_form_submit').disabled = true;
});


//$(document).ready(function() {
//    //set initial state.
//    document.getElementById('empathyType-6').checked = true;
//    document.getElementById('empathyValence-7').checked = true;
//    $(document.querySelectorAll('input[type=checkbox]')).prop("checked", false);
//    $(document.getElementById('empathyType-1')).parent().parent().parent().parent().hide();
//});

//$(document.getElementById('isEmpathy')).change(function() {
//    if(this.checked) {
//        $(document.getElementById('empathyType-1')).parent().parent().parent().parent().show();
//        $(document.getElementById('empathyType-6')).parent().hide();
//        $(document.getElementById('empathyValence-7')).parent().hide();
//        document.getElementById("outputsentence").innerHTML = "";
//        $(document.getElementById('errormessage')).show();
//        document.getElementById('submit').disabled = true;
//    }
//    else {
//        $(document.getElementById('empathyType-1')).parent().parent().parent().parent().hide();
//        document.getElementById('empathyType-6').checked = true;
//        document.getElementById('empathyValence-7').checked = true;
//        $(document.getElementById('errormessage')).hide();
//        document.getElementById('submit').disabled = false;
//    }
//});
//
//$('[name=antecedent]').focusin( function(){
//document.getElementById('submit').disabled = true;
//});
//
//$('[name=antecedent]').focusout( function(){
//    if ((parseInt(document.getElementById("postIndex").value)+1) > parseInt(document.getElementById('antecedent').value)){
//        document.getElementById('submit').disabled = false;
//    }
//});
//
//$('[name=antecedent]').change(function() {
//    var output = document.getElementById("antecedentMessage");
//    if ((parseInt(document.getElementById("postIndex").value)+1) <= parseInt(document.getElementById('antecedent').value)){
//        output.style.color = "red";
//        output.innerHTML = "Het berichtnummer moet kleiner dan of gelijk aan " + (parseInt(document.getElementById("postIndex").value)) + " zijn.";
//    } else{
//        output.style.color = "black";
//        output.innerHTML = "Je hebt bericht nummer " + (document.getElementById('antecedent').value) + " geselecteerd.";
//        ReplyButton("replytext" + (parseInt(document.getElementById('antecedent').value-1)));
//    }
//});
//
//$('[name=empathyValence]').change(function() {
//    var output = document.getElementById("outputsentence");
//    output.innerHTML = updateSentence();
//    if (document.querySelector("input[name=empathyType]:checked").value == "EmpathyOption7" || document.querySelector("input[name=empathyValence]:checked").value == 'ValenceOption8'){
//        document.getElementById('submit').disabled = true;
//        $(document.getElementById('errormessage')).show();
//    } else {
//    document.getElementById('submit').disabled = false;
//    $(document.getElementById('errormessage')).hide();
//    }
//});
//$('[name=empathyType]').change(function() {
//    var output = document.getElementById("outputsentence");
//    output.innerHTML = updateSentence();
//    if (document.querySelector("input[name=empathyType]:checked").value == "EmpathyOption7" || document.querySelector("input[name=empathyValence]:checked").value == "ValenceOption8"){
//        document.getElementById('submit').disabled = true;
//        $(document.getElementById('errormessage')).show();
//    } else {
//    document.getElementById('submit').disabled = false;
//    $(document.getElementById('errormessage')).hide();
//    }
//});
//
//function updateSentence() {
//    var empathy = document.querySelector("input[name=empathyType]:checked").value;
//    var valenceVal = document.querySelector("input[name=empathyValence]:checked").value;
//
//    switch(valenceVal) {
//        case 'ValenceOption1':
//        valence = 'blij';
//        break;
//        case 'ValenceOption2':
//        valence = 'opgewekt';
//        break;
//        case 'ValenceOption3':
//        valence = 'emotieloos';
//        break;
//        case 'ValenceOption4':
//        valence = 'geraakt';
//        break;
//        case 'ValenceOption5':
//        valence = 'gekwetst';
//        break;
//        case 'ValenceOption6':
//        valence = 'verdrietig';
//        break;
//        case 'ValenceOption7':
//        valence = 'boos';
//        break;
//        case 'ValenceOption8':
//        return "";
//        break;
//
//    }
//    switch(empathy) {
//        case 'EmpathyOption1':
//        return 'Ik begrijp dat je je ' + valence + ' voelt';
//        break;
//        case 'EmpathyOption2':
//        return 'Ik kan me voorstellen dat je je '+ valence + ' voelt';
//        // code block
//        break;
//        case 'EmpathyOption3':
//        return 'Ik zou me ' + valence + ' voelen als ik in jouw schoenen stond';
//        break;
//        case 'EmpathyOption4':
//        return 'Ik voel me zelf ook ' + valence;
//        break;
//        case 'EmpathyOption5':
//        return 'Ik voel me ' + valence + ' door de situatie waarin je je bevindt';
//        break;
//        case 'EmpathyOption6':
//        return 'Ik voel me ' + valence + ' door wat je hebt meegemaakt';
//        break;
//        case 'EmpathyOption7':
//        return "";
//        break;
//    }
//}


//function ReplyButton(id){
//    var items = document.getElementsByName('replybutton');
//    for (var i=0; i < items.length; i++) {
//        items[i].style.color = '#000000';
//        document.getElementById('replytext'+i).style.backgroundColor = '#FFFFFF';
//      }
//    postnumber = id.slice(9)
//    document.getElementById("replybttn"+postnumber).style.color = '#77DD77';
//    document.getElementById("replytext"+postnumber).style.backgroundColor = '#dfffb3'; //
//    document.getElementById('antecedent').value = parseInt(postnumber) +1;
//    document.getElementById('antecedentMessage').style.color = 'black';
//    document.getElementById('antecedentMessage').innerHTML = "Je hebt bericht nummer " + (parseInt(postnumber) + 1) + " geselecteerd.";
//    if (!(document.getElementById("isEmpathy").checked) || !(document.querySelector("input[name=empathyType]:checked").value == "EmpathyOption7" || document.querySelector("input[name=empathyValence]:checked").value == "ValenceOption8")){
//        document.getElementById('submit').disabled = false;
//    }
//}

//$(document.getElementById("submit")).click(function(){
//    if (!(document.getElementById('antecedent').value.length == 0)){
//        if (!(document.getElementById("isEmpathy").checked) || !(document.querySelector("input[name=empathyType]:checked").value == "EmpathyOption7" || document.querySelector("input[name=empathyValence]:checked").value == "ValenceOption8")){
//            document.getElementById('submitmessage').innerHTML = "Reactie wordt verzonden, dit kan soms even duren.<br>";
//        }
//    }
//});
