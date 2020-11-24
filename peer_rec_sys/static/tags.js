

if (userstrengths.length != 0){
    for (var i = 0; i < strength.getElementsByTagName('li').length; ++i) {
        for (var j = 0; j < userstrengths.length; ++j){
            if (document.getElementById('strength-'+i).value == userstrengths[j]){
                document.getElementById('strength-'+i).checked = true
            }
        }
    }
}

if (userweakness.length != 0){
    for (var i = 0; i < weakness.getElementsByTagName('li').length; ++i) {
        for (var j = 0; j < userweakness.length; ++j){
            if (document.getElementById('weakness-'+i).value == userweakness[j]){
                document.getElementById('weakness-'+i).checked = true
            }
        }
    }
}

function cbCompare(obj) {
var strengths = document.getElementById('strength')
    var sitems = strength.getElementsByTagName('li')
    for (var i = 0; i < sitems.length; ++i) {
        if (document.getElementById('strength-'+i).checked == true){
            if (document.getElementById('weakness-'+i).checked == true)
                document.getElementById('weakness-'+i).checked = false
        }
    }

//    document.getElementById('strength').getElementsByTagName('li')[0].firstChild.value
}