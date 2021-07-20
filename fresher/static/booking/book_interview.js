
console.log('reacehed');

var skills =[]
var meets  =[]

function skill(s){
    if (skills.includes(s))
    {
        skills.pop(s)
    }
    else{
        skills.push(s)
    }

    if (s === 'java'){
        
        // document.getElementById('id_price').value = 100;
        document.getElementById('id_price').value = 100;
        console.log(document.getElementById('id_price').value);

    }

    console.log(skills);
}


function meet(s){
    console.log(s);
}

