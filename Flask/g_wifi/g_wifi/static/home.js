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
		document.getElementById("test2").style.display="none";
        document.getElementById("alerts").style.display="none";
        $('#addbtn').toggleClass('wifipressed');
		document.getElementById("test2").style.display="none";
    } else if (x===2){
        document.getElementById("guestWiFi").style.display="none";
        document.getElementById("guestSearch").style.display="block";
        document.getElementById("alerts").style.display="none";
        $('#searchbtn').toggleClass('wifipressed');
		document.getElementById("test2").style.display="block";
     } 
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

//search function
/* function searchData(){
data="config paging disable (ptor2nww01) >show netuser summary Maximum logins allowed for a given user name..... Unlimited User Name WLAN Id User Type Lifetime Description ------------------------ -------- --------- ------------------------------ -------------------------------- amy.a.butler@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0078709 angelina_tan@mckinsey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec REQ0072570 bobby.j.thompson@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0082431 carol.gibbs@economical.com WLAN 2 Guest 180 days 0 hrs 0 mins 0 sec RIT001422 carson.brett@ca.ey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec TASK0088056 dalton.roth@ca.ey.com WLAN 2 Guest 90 days 0 hrs 0 mins 0 secs TASK0088059 edwin.marquez@seb-admin.com WLAN 2 Guest 0 days 8 hrs 0 mins 0 secs RITM0073177 eigbmember@economical.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec RITM0072341 frank.morassut@adastragrp.com WLAN 2 Guest 180 days 0 hrs 0 mins 0 sec Task0084621 gorda@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0073163 greg.demacio@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0082432 hans.reidl@economical.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec Cut-overto-CISCO jacque.friedland@gmail.com WLAN 2 Guest 180 days 0 hrs 0 mins 0 sec TASK0085371 jacque.friendland@gmail.com WLAN 2 Guest 180 days 0 hrs 0 mins 0 sec TASK0085371 jacqueline.tse@fsco.gov.on.ca WLAN 2 Guest 14 days 0 hrs 0 mins 0 secs TASK0089174 janice.c.deganis@ca.ey.com WLAN 2 Guest 90 days 0 hrs 0 mins 0 secs TASK0088054 kamal@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 karen.vacciana@fsco.gov.on.ca WLAN 2 Guest 14 days 0 hrs 0 mins 0 secs TASK0089183 kristen.nolan@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0078711 kristypryma@gmail.com WLAN 2 Guest 136 days 21 hrs 0 mins 0 sec RITM0066847 larry.penn@seb-admin.com WLAN 2 Guest 0 days 8 hrs 0 mins 0 secs N/A lbawtinh@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec foronsiteworking-RITM0062132 lucy.shao@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0067032 madelaine.fielding@ca.ey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec TASK0088317 mariam.merchant@ca.ey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec TASK0088312 markin@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 marymcna@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 michael.tin@fsco.gov.on.ca WLAN 2 Guest 14 days 0 hrs 0 mins 0 secs TASK0089177 michelle.forster@seb-admin.com WLAN 2 Guest 1 days 0 hrs 0 mins 0 secs REQ0073177 miki.amakawa@fsco.gov.on.ca WLAN 2 Guest 14 days 0 hrs 0 mins 0 secs TASK0089171 nick.magyar@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0082433 peniel.efechaobor@ca.ey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec TASK0088060 philip.henville@hubio.ca WLAN 2 Guest 90 days 0 hrs 0 mins 0 secs REQ0070802 robpicc@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 ruby.leung@fsco.gov.on.ca WLAN 2 Guest 14 days 0 hrs 0 mins 0 secs REQ0072281 sarah.mukhtiyar@ca.ey.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0078712 sergepok@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 spanchal@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0062123 tanya.k.kaushal@pwc.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec REQ0071973 tho.huynh@economical.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec REQ0071973 wpgguest WLAN 2 Guest Infinity Winnipeg wsteele@ca.ibm.com WLAN 2 Guest 365 days 0 hrs 0 mins 0 sec TASK0084208 zach.ramsay@ca.ey.com WLAN 2 Guest 120 days 0 hrs 0 mins 0 sec TASK0088309 (ptor2nww01) >";
//data;
$.get("/search", function(data){
	data = $.parseJSON()
	var people=[]; //this array will store the names of all the people
	lines=data.split(" "); //this separates the data word by word

	for(i=0;i<lines.length;i++){   //this for loop will cycle through the lines array 
		var rowCount=1;  //this will be where the new row is added in the table, the first row will start at 1
		var table=document.getElementById("table1");   //this finds the table element in the html
		
		for(i=0;i<lines.length;i++){   //goes through the lines array
			if(lines[i].indexOf(".com")!=-1 || lines[i].indexOf(".ca")!=-1){   //this checks for .com and .ca since every email address in the system will end in one of the 2
				people.push(lines[i]);  //pushes the name into the people array
				start=data.indexOf(lines[i]);  //this is where to start searching					
				if (rowCount%2==1){//this will change the background colour in the table
					var coloring = "rgb(96, 194, 233)";  
					var fontColor="white";
					var bording="none";
				} else {
					var coloring = "white";
					var fontColor="rgb(96, 194, 233)";
					var bording="1px solid rgb(96, 194, 233)";
				}
				var date=data.slice(data.indexOf("Guest",start)+6, data.indexOf("sec",start)+3); //slices the date out
				var row=table.insertRow(rowCount);  //inserts a row at the position of rowCount
				var cell1=row.insertCell(0);   //left hand column 
				var cell2=row.insertCell(1);   //middle column
				var cell3=row.insertCell(2);   //right hand column
				
				var column1=document.createElement("p");  //creates a p element
				column1.style.backgroundColor=coloring;   //sets the background colour of the p element
				column1.style.color=fontColor;            //sets the font color of the p element
				column1.style.border=bording;             //sets the border of the p element
				var names=document.createTextNode(lines[i]);  //creates a text node with the value of the persons name
				column1.appendChild(names);    //appends the text node into the p element
				cell1.appendChild(column1);    //appends the p element to the left hand cell in the table
				
				var column2=document.createElement("p");  //creates a p element
				column2.style.backgroundColor=coloring;   //sets the background color of the p element
				column2.style.color=fontColor;            //sets the font color of the p element
				column2.style.border=bording;             //sets the border of the p element
				var date=document.createTextNode(date);   //creates a text node with a value of the date
				column2.appendChild(date);                //appends the date to the p elememt 
				cell2.appendChild(column2);               //appends the p element to the middle cell of the table
				
				var column3=document.createElement("p");  //creates a p element
				column3.style.backgroundColor=coloring;    //sets the background colour of the p element
				column3.style.color=fontColor;             //sets the font color of the p element
				column3.style.border=bording;              //sets the border of the p element
				column3.style.textAlign= center;			//center the button in the column
				var selects=document.createElement("input");  //creates an input element
				selects.type="radio";           //sets the type of the input to radio
				selects.name="radioButtons"    //the radio buttons all need to have the same name in a table or else they act like check boxes and users would be able to select multiple people at one time
				selects.id=lines[i];           //sets the id of the radio button to the persons name --> this will be used in the function "checker"
				selects.className="radioButtons"
				column3.appendChild(selects);   //appends the radio button to the p element
				cell3.appendChild(column3);     //appends the p element to the right hand cell of the table
				
				rowCount++;  //increases the row count by one so the next name will be added into the next row
			}
		}
	}
})

} */
	
/* function checker(){ //this function finds which radio button was selected
	for (i=0;i<people.length;i++){  //loops through all of the people on the list to see if they are checked
		x=document.getElementById(people[i]);   // this finds the checkbox
		if (x.checked==true){  //checks if the checkbox is checked
			document.getElementById("testing").innerHTML=people[i];
			//the following three lines are used to reset the page if the user decides to select another person from the list
			document.getElementById("three").style.display="none";
			document.getElementById("four").style.display="none";
			document.getElementById("five").style.display="none";
			//document.getElementById("two").style.marginBottom="200px";
		} 
	}
} */

function navigate(x){
	para=document.getElementById("three");
	para.style.display="block";
	var str=document.getElementById("testing").textContent;
	if (str=="Please select a user from the list above"){ //this if checks if the user has selected a name from the list
		window.alert("Please select a person");   //if they have not selected a name from the list they get an alert telling them to select a user
	}else{
		if (x==1){  //if they selected delete
			para.innerHTML="Would you like to delete "+str;
			document.getElementById("four").style.display="none";   //if the extend time select drop down is on the screen it is hidden
			document.getElementById("five").style.display="block";  //places the button on the screen
			document.getElementById("five").value="Confirm Deletion";  //sets the value of the button to 'Confirm Deletion'
			//document.getElementById("two").style.marginBottom="10px";
		} else if (x==2){ //if they select extend
			document.getElementById("four").style.display="block";   //shows the select time drop down
			para.innerHTML="How long would you like to extend "+str;
			document.getElementById("five").style.display="block";    //places the button on the screen
			document.getElementById("five").value="Confirm Time Extension";  //sets the value of the button to 'Confirm Time Extension'
			//document.getElementById("two").style.marginBottom="80px";
		}
	}
}