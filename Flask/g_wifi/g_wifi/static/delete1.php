<?php
ini_set('error_reporting', E_ALL);
// echo $path = exec('pwd')

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

//is_null($result['column'])

//$result['column'] === NULL


$account = $_POST["account"];
$login = $_POST["login"];
$password =  $_POST["password"];
//* echo $account;
//echo $login;
//echo $password; 
//$guestfullname = $_POST["guestfullname"];
//$guestfullname = preg_replace('/\s+/', '', $guestfullname );
//$guestcompany =  $_POST["guestcompany"];
//$guestcompany = preg_replace('/\s+/', '', $guestcompany );
//$guestphone = $_POST["guestphone"];
//$guestphone = preg_replace('/\s+/', '', $guestphone );
//$guestcomment = $_POST["guestcomment"];
//$guestcomment = preg_replace('/\s+/', '', $guestcomment );
//$HOURS = $_POST["HOURS"];
//$sponsordepartment = $_POST["sponsordepartment"];
//$sponsordepartment = preg_replace('/\s+/', '', $sponsordepartment );
//$sponsoremail = $_POST["sponsoremail"];
//$login = $_POST["login"];
//$password =  $_POST["password"];
// 5months

//$search = "test";

//if (empty ($search))
//{

//$search = "empty";

//}






    
    $command = escapeshellcmd("python3.4 /var/www/html/ntw/SANDBOX/WIFI/work/delete1.py $account $login $password ");
    $tho = shell_exec($command);
	echo $tho
?>
