function nav(x){
	$('.pressed').toggleClass('pressed');
	if (x===1){
		document.getElementById("vlanMove").style.display="block";
		document.getElementById("WiFi").style.display="none";
		document.getElementById("alerts").style.display="none";
		$('#vlanbtn').toggleClass('pressed');
	
    } 
	else if (x===2){
		document.getElementById("vlanMove").style.display="none";
		document.getElementById("WiFi").style.display="block";
		document.getElementById("alerts").style.display="none";
		$('#wifibtn').toggleClass('pressed');
	
    } 
	else if (x===3){
		document.getElementById("vlanMove").style.display="none";
		document.getElementById("WiFi").style.display="none";
		document.getElementById("alerts").style.display="none";
		$('#cwlanbtn').toggleClass('pressed');
    } 
}

function Navigate(x){
	$('.wifipressed').toggleClass('wifipressed');
	if (x===1){
		document.getElementById("guestWiFi").style.display="block";
		document.getElementById("guestSearch").style.display="none";
		document.getElementById("guestDelete").style.display="none";
		document.getElementById("guestExtend").style.display="none";
		document.getElementById("alerts").style.display="none";
		$('#addbtn').toggleClass('wifipressed');
	} else if (x===2){
		document.getElementById("guestWiFi").style.display="none";
		document.getElementById("guestSearch").style.display="block";
		document.getElementById("guestDelete").style.display="none";
		document.getElementById("guestExtend").style.display="none";
		document.getElementById("alerts").style.display="none";
		$('#searchbtn').toggleClass('wifipressed');
	} else if (x===3){
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
	}
}