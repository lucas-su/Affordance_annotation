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
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".uncon_move").change(function(){
    if(this.checked) {
    document.getElementById('uncon_move').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".dir_affs").change(function(){
    if(this.checked) {
    document.getElementById('dir_affs').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".indir_affs").change(function(){
    if(this.checked) {
    document.getElementById('indir_affs').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".observe_affs").change(function(){
    if(this.checked) {
    document.getElementById('observe_affs').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".social_affs").change(function(){
    if(this.checked) {
    document.getElementById('social_affs').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(".no_affs").change(function(){
    if(this.checked) {
    document.getElementById('no_affs').checked = true;
    document.getElementById('no_clue').checked = false;
    }
    enable_disable_submit();
});

$(document.getElementById('con_move')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".con_move").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('uncon_move')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".uncon_move").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('dir_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".dir_affs").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('indir_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".indir_affs").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('observe_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".observe_affs").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('social_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".social_affs").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('no_affs')).change(function(){
    enable_disable_submit();
    if(this.checked == false){
    $(".no_affs").each(function(){
        this.checked = false;
    })
    } else {
    document.getElementById('no_clue').checked = false;
    }
});

$(document.getElementById('no_clue')).change(function(){
    if(this.checked == true){
        $(".aff_super_div").each(function(){
        this.hidden = true;
        })
    } else {
    $(".aff_super_div").each(function(){
        this.hidden = false;
        })
    }
    enable_disable_submit();
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

$(document.getElementById('no_clue')).change(function(){
    if (this.checked){
        $(".highlevel_aff").each(function(){
        this.checked = false;
        })
        $(".lowlevel_aff").each(function(){
            this.checked = false;
        })
    }
    if(document.getElementById('con_move').checked ||
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