//used to switch which form is visable on navbtn putton press


var macAddress = $("#macAddress");
var cwlanmacAddress = $("#cwlanmacAddress");

function formatMAC(e) {
    var r = /([a-f0-9]{2})([a-f0-9]{2})/i,
        str = e.target.value.replace(/[^a-f0-9]/ig, "");

    while (r.test(str)) {
        str = str.replace(r, '$1' + ':' + '$2');
    }

    e.target.value = str.slice(0, 17);
};

macAddress.on("keyup", formatMAC);
cwlanmacAddress.on("keyup", formatMAC);


function nav(x){
    $('.pressed').toggleClass('pressed');
    if (x===1){
        document.getElementById("vlanMove").style.display="block";
        document.getElementById("WiFi").style.display="none";
        document.getElementById("alerts").style.display="none";
        document.getElementById("cwlan").style.display="none";
        $('#vlanbtn').toggleClass('pressed');
    
    } 
    else if (x===2){
        document.getElementById("vlanMove").style.display="none";
        document.getElementById("WiFi").style.display="block";
        document.getElementById("alerts").style.display="none";
        document.getElementById("cwlan").style.display="none";
        $('#wifibtn').toggleClass('pressed');
    
    } 
    else if (x===3){
        document.getElementById("vlanMove").style.display="none";
        document.getElementById("WiFi").style.display="none";
        document.getElementById("cwlan").style.display="block";
        document.getElementById("alerts").style.display="none";
        $('#cwlanbtn').toggleClass('pressed');
    } 
}



//used for the guest wifi tabs to change which subform is active 
function Navigate(x){
    $('.wifipressed').toggleClass('wifipressed');
    if (x===1){
        document.getElementById("guestWiFi").style.display="block";
        document.getElementById("guestSearch").style.display="none";
        /* document.getElementById("guestDelete").style.display="none";
        document.getElementById("guestExtend").style.display="none"; */
        document.getElementById("alerts").style.display="none";
        $('#addbtn').toggleClass('wifipressed');
    } else if (x===2){
        document.getElementById("guestWiFi").style.display="none";
        document.getElementById("guestSearch").style.display="block";
       /*  document.getElementById("guestDelete").style.display="none";
        document.getElementById("guestExtend").style.display="none"; */
        document.getElementById("alerts").style.display="none";
        $('#searchbtn').toggleClass('wifipressed');
     } 
		/*else if (x===3){
        document.getElementById("guestWiFi").style.display="none";
        document.getElementById("guestSearch").style.display="none";
        document.getElementById("guestDelete").style.display="block";
        document.getElementById("guestExtend").style.display="none";
        document.getElementById("alerts").style.display="none";
        $('#deletebtn').toggleClass('wifipressed');
    } else if (x===4){
        document.getElementById("guestWiFi").style.display="none";
        document.getElementById("guestSearch").style.display="none";
        document.getElementById("guestDelete").style.display="none";
        document.getElementById("guestExtend").style.display="block";
        document.getElementById("alerts").style.display="none";
        $('#extendbtn').toggleClass('wifipressed');
    } */
}
$('#WiFi').submit(function()
 {
    $("input[type='submit']", this)
      .val("Please Wait...")
      .attr('disabled', 'disabled');
 
    return true;
  });
  $('#vlanMove').submit(function()
 {
    $("input[type='submit']", this)
      .val("Please Wait...")
      .attr('disabled', 'disabled');
 
    return true;
  });
 $('#cwlan').submit(function()
 {
    $("input[type='submit']", this)
      .val("Please Wait...")
      .attr('disabled', 'disabled');
 
    return true;
  });


function cwlan(x){
    $('.cwlanpressed').toggleClass('cwlanpressed');
    if (x===1){
        document.getElementById("addcwlan").style.display="block";
        document.getElementById("searchcwlan").style.display="none";
        document.getElementById("alerts").style.display="none";
        $('#cwlanaddbtn').toggleClass('cwlanpressed');
    } else if (x===2){
        document.getElementById("addcwlan").style.display="none";
        document.getElementById("searchcwlan").style.display="block";
        document.getElementById("alerts").style.display="none";
        $('#cwlansearchbtn').toggleClass('cwlanpressed');
	}
}