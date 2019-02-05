function nav(x){
	$('.pressed').toggleClass('pressed');
	//var obj = $(this);
	//obj.setAttribute('id', 'pressed');
	//var attr = obj.attr('id'); 
	//alert(obj);
	if (x===1){
		document.getElementById("homeForm").style.display="block";
		document.getElementById("vlanMove").style.display="none";
		document.getElementById("WiFi").style.display="none";
		document.getElementById("contact").style.display="none";
		document.getElementById("alerts").style.display="none";
		$('#homebtn').toggleClass('pressed');
	
    } 
	else if (x===2){
		document.getElementById("homeForm").style.display="none";
		document.getElementById("vlanMove").style.display="block";
		document.getElementById("WiFi").style.display="none";
		document.getElementById("contact").style.display="none"; 
		document.getElementById("alerts").style.display="none";
		$('#vlanbtn').toggleClass('pressed');
	
    } 
	else if (x===3){
		document.getElementById("homeForm").style.display="none";
		document.getElementById("vlanMove").style.display="none";
		document.getElementById("WiFi").style.display="block";
		document.getElementById("contact").style.display="none"; 
		document.getElementById("alerts").style.display="none";
		$('#wifibtn').toggleClass('pressed');
	
    } 
	else if (x===4){
		document.getElementById("homeForm").style.display="none";
		document.getElementById("vlanMove").style.display="none";
		document.getElementById("WiFi").style.display="none";
		document.getElementById("contact").style.display="block"; 
		document.getElementById("alerts").style.display="none";
		$('#contactbtn').toggleClass('pressed');
    } 
}

function Navigate(x){
	if (x===1){
		document.getElementById("guestWiFi").style.display="block";
		document.getElementById("guestSearch").style.display="none";
		document.getElementById("guestDelete").style.display="none";
		document.getElementById("guestExtend").style.display="none";
		document.getElementById("alerts").style.display="none";
	} else if (x===2){
		document.getElementById("guestWiFi").style.display="none";
		document.getElementById("guestSearch").style.display="block";
		document.getElementById("guestDelete").style.display="none";
		document.getElementById("guestExtend").style.display="none";
		document.getElementById("alerts").style.display="none";
	} else if (x===3){
		document.getElementById("guestWiFi").style.display="none";
		document.getElementById("guestSearch").style.display="none";
		document.getElementById("guestDelete").style.display="block";
		document.getElementById("guestExtend").style.display="none";
		document.getElementById("alerts").style.display="none";
	} else if (x===4){
		document.getElementById("guestWiFi").style.display="none";
		document.getElementById("guestSearch").style.display="none";
		document.getElementById("guestDelete").style.display="none";
		document.getElementById("guestExtend").style.display="block";
		document.getElementById("alerts").style.display="none";
	}
}