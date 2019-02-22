<?php
ini_set('error_reporting', E_ALL);
// echo $path = exec('pwd')
$var1 = "1";
$var2 = "2";
$var3 = "3";
//echo $_POST["guestemail"];
//echo $_POST["guestfullname"];
//echo $_POST["guestcompany"];
//echo $_POST["guestphone"];
//echo $_POST["guestcomment"];
//echo $_POST["HOURS"];
//echo $_POST["sponsordepartment"];
//echo $_POST["sponsoremail"];
//echo $_POST["login"];
//echo $_POST["password"];

//$guestemail = $_POST["guestemail"]=HOURS;
//$GUESTUSERNAME = $_POST["GUESTUSERNAME"]="GUEST";
//$GUESTPASSWORD =  $_POST["GUESTPASSWORD"]="3";
//$username = $_POST["username"]="thh";
//$pwd = $_POST["pwd"]="Cantho99";
//$REQUESTNUMBER = $_POST["REQUESTNUMBER"]="6";
//$SPONSOR= $_POST["HOURS"]="HOURS";




$guestemail = $_POST["guestemail"];
$guestfullname = $_POST["guestfullname"];
$guestfullname = preg_replace('/\s+/', '', $guestfullname );
$guestcompany =  $_POST["guestcompany"];
$guestcompany = preg_replace('/\s+/', '', $guestcompany );
$guestphone = $_POST["guestphone"];
$guestphone = preg_replace('/\s+/', '', $guestphone );
$guestcomment = $_POST["guestcomment"];
$guestcomment = preg_replace('/\s+/', '', $guestcomment );
$HOURS = $_POST["HOURS"];
$sponsordepartment = $_POST["sponsordepartment"];
$sponsordepartment = preg_replace('/\s+/', '', $sponsordepartment );
$sponsoremail = $_POST["sponsoremail"];
$login = $_POST["login"];
$password =  $_POST["password"];
// 5months

if ($_POST["HOURS"] > "604800" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
	
}
if ($_POST["HOURS"] > "604800" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
	
}

elseif ($_POST["HOURS"] == "11826000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
	
}
elseif ($_POST["password"] == "4Wifi_Aut@mate" && $_POST["login"] == "wifiadmin"){
	$login = "thh";
	$password = "Wongsun9";
	
}
elseif ($_POST["password"] == "SDesk_Aut@mate" && $_POST["login"] == "servicedesk") {
    $login = "thh";
	$password = "Wongsun9";
}




elseif ($_POST["HOURS"] == "5184000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "5184000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}
elseif ($_POST["HOURS"] == "7776000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "7776000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}
elseif ($_POST["HOURS"] == "10368000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "10368000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}
elseif ($_POST["HOURS"] == "15552000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "15552000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}

elseif ($_POST["HOURS"] == "2592000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "2592000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}

elseif ($_POST["HOURS"] == "31536000" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "31536000" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}

elseif ($_POST["HOURS"] == "1209600" && $_POST["login"] == "servicedesk"){
	exit ("Permision denied");
}	
elseif ($_POST["HOURS"] == "1209600" && $_POST["login"] == "wifiadmin"){
	exit ("Permision denied");
}

elseif ($_POST["password"] == "4Wifi_Aut@mate" && $_POST["login"] == "wifiadmin"){
	$login = "thh";
	$password = "Wongsun9";
	
}
elseif ($_POST["password"] == "SDesk_Aut@mate" && $_POST["login"] == "servicedesk") {
    $login = "thh";
	$password = "Wongsun9";
}



function random_password( $length = 8 ) {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    $password = substr( str_shuffle( $chars ), 0, $length );
    return $password;
}
$GUESTPASSWORD1 = random_password(8); 
//echo $GUESTPASSWORD1
//if ($pwd == "123" && $username == "brian"){
//	$username = "thh";
//	$pwd = "Cantho99";
	
//}
//else {
//	echo "not valid password";
//}
//echo $var1,$var2,$var3;
//$command = escapeshellcmd("python3.4 /var/www/cgi-bin/work/excecute.py $macaddress $deviceip $changeticket $username $pwd $location $description $vlanx $selectchoice");
//$tho = shell_exec($command);
//echo $tho

//if ($pwd == "Cantho99" && $username == "thh"){
//	$username = "thh";
//	$pwd = "";
	//echo $var1,$var2,$var3;
//    $command = escapeshellcmd("python3.4 /var/www/html/ntw/SANDBOX/WIFI/work/excecute.py $HOURS $GUESTUSERNAME $GUESTPASSWORD $username  $pwd $REQUESTNUMBER $SPONSOR");
//    $tho = shell_exec($command);
//    echo $tho;
	
//}
//else {
//	echo "FAILED NOT VALID password FAILED";
//}
#echo $_POST["password"];
    
    $command = escapeshellcmd("python3.4 /var/www/html/ntw/SANDBOX/WIFI/work/excecute.py $guestemail $guestfullname $guestcompany $guestphone $HOURS $sponsordepartment $sponsoremail $login  $password $GUESTPASSWORD1 $guestcomment ");
    $tho = shell_exec($command);
    echo $tho;
?>
