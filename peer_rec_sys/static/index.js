function cbChange(obj) {
    var cbs = document.getElementsByClassName("cb");
    for (var i = 0; i < cbs.length; i++) {
        cbs[i].checked = false;
    }
    obj.checked = true;
}

function cbCompare(obj) {
    var strengths = document.getElementsByClassName("strength")
    var sitems = strength.getElementsByTagName('li')
    for (var i = 0; i < sitems.length; ++i) {
        if (document.getElementById('strength-'+i).checked == true){
            if (document.getElementById('weakness-'+i).checked == true)
                document.getElementById('weakness-'+i).checked = false
        }
    }

//    document.getElementById('strength').getElementsByTagName('li')[0].firstChild.value
}