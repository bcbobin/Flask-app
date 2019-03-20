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

macAddress.on("keyup", formatMAC);											//used to format mac address inputs 
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
function Navigate(x, data, user){
    $('.wifipressed').toggleClass('wifipressed');
    if (x===1){
        document.getElementById("guestWiFi").style.display="block";
        document.getElementById("guestSearch").style.display="none";
		document.getElementById("test2").style.display="none";
        document.getElementById("alerts").style.display="none";
        $('#addbtn').toggleClass('wifipressed');
		document.getElementById("test2").style.display="none";
		document.getElementById("test3").style.display="none";
    } else if (x===2){
        document.getElementById("guestWiFi").style.display="none";
        document.getElementById("guestSearch").style.display="block";
        document.getElementById("alerts").style.display="none";
        $('#searchbtn').toggleClass('wifipressed');
		if (data != "" && data !="-1"){
			if(user == ""){
				document.getElementById("test2").style.display="block";
				document.getElementById("test3").style.display="none";
		
			} else{
				document.getElementById("test2").style.display="none";
				document.getElementById("test3").style.display="block";
			}
		}
    } 
}
$('#WiFi').submit(function()			//locks submit buttons after a click to prevent spam 
 {
    $("input[type='submit']", this)
      .val("Please Wait...")
      .attr('disabled', 'disabled');
 
    return true;
  });
  $('#guestSearch').submit(function()			//locks submit buttons after a click to prevent spam 
 {
    $("input[type='submit']", this)
      .val("...")
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
 $('#login').submit(function()
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


function navigat(x){
	para=document.getElementById("three");
	para.style.display="block";
	var str=document.getElementById("testing").textContent;
	if (str=="Please select a user from the list above"){ //this if checks if the user has selected a name from the list
		window.alert("Please select a person");   //if they have not selected a name from the list they get an alert telling them to select a user
	}else{
		if (x==1){  //if they selected delete
			para.innerHTML="Would you like to delete "+"<b>"+str+"</b>?";
			document.getElementById("four").style.display="none";   //if the extend time select drop down is on the screen it is hidden
			document.getElementById("five").style.display="block";  //places the button on the screen
			document.getElementById("five").value="Confirm Deletion";  //sets the value of the button to 'Confirm Deletion'
			//document.getElementById("two").style.marginBottom="10px";
		} else if (x==2){ //if they select extend
			document.getElementById("four").style.display="block";   //shows the select time drop down
			para.innerHTML="What is the time revision you would like to make to "+"<b>"+str+"</b>?";
			document.getElementById("five").style.display="block";    //places the button on the screen
			document.getElementById("five").value="Confirm Time Revision";  //sets the value of the button to 'Confirm Time Extension'
			//document.getElementById("two").style.marginBottom="80px";
		}
	}
}

function singleNavigate(x){
	para=document.getElementById("three1");
	para.style.display="block";
	var str=document.getElementById("nameHere").textContent;
	if (x==1){  //if they selected delete
		para.innerHTML="Would you like to delete "+"<b>"+str+"</b>?";
		document.getElementById("four1").style.display="none";   //if the extend time select drop down is on the screen it is hidden
		document.getElementById("five1").style.display="block";  //places the button on the screen
		document.getElementById("five1").value="Confirm Deletion";  //sets the value of the button to 'Confirm Deletion'
		//document.getElementById("two").style.marginBottom="10px";
	} else if (x==2){ //if they select extend
		document.getElementById("four1").style.display="block";   //shows the select time drop down
		para.innerHTML="What is the time revision you would like to make to "+"<b>"+str+"</b>?";
		document.getElementById("five1").style.display="block";    //places the button on the screen
		document.getElementById("five1").value="Confirm Time Revision";  //sets the value of the button to 'Confirm Time Extension'
		//document.getElementById("two").style.marginBottom="80px";
	}
}