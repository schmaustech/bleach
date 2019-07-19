#!/usr/bin/perl
# Copyright (C) June 2004 Benjamin Schmaus - Schmaustech
require CGI;
require CGI::Cookie;
require Net::POP3;
require DBI;
require GD::Graph::pie;
$dsn="DBI:mysql:database=spam";
$dbu="root";
$dbp="96?sas?b";
cgiquery();
variableinit();
if ($update >= 100 && $update < 199) {
	getcookie();
	validatecookie();
	configure();
}
if ($update >= 200 && $update < 299) {
        login();
}
if ($update >= 300 && $update < 399) {
	getcookie();
	validatecookie();
        logout();
}
if ($update >= 400 && $update < 499) {
	getcookie();
	validatecookie();
        sysquarantine();
}
if ($update >= 500 && $update < 599) {
	getcookie();
	validatecookie();
        status();
}
if ($update >= 600 && $update < 699) {
	getcookie();
	validatecookie();
        userquarantine();
}
if ($update >= 700 && $update < 799) {
        core();
}
exit;
#########################################
# Bleach Initialization Sub Routines	#
#########################################
#Getcookie Subroutine
sub getcookie {
	$cookieflag="0";
	%cookies = fetch CGI::Cookie;
	$cook = defined($cookies{'access'}) && $cookies{'access'}->value;
	(@cooktmp)=split(/:/,$cook);
	$cooksize = @cooktmp;
	if ($cooksize eq "2") {
		$cookieflag = "1";
		($cook1,$cook2)=split(/:/,$cook);
	} else {
		$cookieflag = "2";
		($username,$cook2,$domain)=split(/:/,$cook);
		$email = "$username\@$domain";
	        $username2 = "$username.$domain";	
	}
}
#Validatecookie Subroutine
sub validatecookie {
	if ($cookieflag eq "1") {
		$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
		$sth = $dbh->prepare("select * from customer where customer='$cook1'");
		$sth->execute();
		($tdomain,$tusername,$tpassword,$tvalidator,$taux1,$taux2)=$sth->fetchrow_array();
		$sth->finish();
		$dbh->disconnect;
		$tcook = "$tdomain:$tvalidator";
		if ($cook ne $tcook) {
        		print "Content-type: text/html\n\n";
        		print '<html>';
        		print '<body bgcolor="#CCCCCC" text="#000000">';
        		print '<center>';
        		print '<br>';
        		print '<br>';
        		print 'You must be logged in and have sufficient permissions to view this page!';
        		print '</center>';
        		print '</body>';
        		print '</html>';
        		exit;
		}	
		$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
	}
	if ($cookieflag eq "2") {
        	$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        	$sth = $dbh->prepare("select * from tmpaccess where customer='$cook'");
        	$sth->execute();
        	($tcook)=$sth->fetchrow_array();
        	$sth->finish();
        	$dbh->disconnect;
        	if ($cook ne $tcook || $cook eq "") {
                	print "Content-type: text/html\n\n";
                	print '<html>';
                	print '<body bgcolor="CCCCCC" text="#000000">';
                	print '<center>';
                	print '<br>';
                	print '<br>';
                	print 'You must be logged in and have sufficient permissions to view this page!';
                	print '</center>';
                	print '</body>';
                	print '</html>';
                	exit;
        	}
        	$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
	}
}
#Variableinit Subroutine
sub variableinit {
	$aux1="0";
	$aux2="0";
	$flag="";
	$pass="0";
	$temp="0";
	$userval="0";
	$email = "$username\@$domain";
	$username2 = "$username.$domain";
}
#Cgiquery Subroutine
sub cgiquery {
$query = new CGI;
$newattach = $query->param('newattach');
$newenavirus = $query->param('newenavirus');
$newover = $query->param('newover');
$newoveract = $query->param('newoveract');
$newaado = $query->param('newaado');
$newaddo = $query->param('newaddo');
$newaadot = $query->param('newaadot');
$newaddot = $query->param('newaddot');
$newssm = $query->param('newssm');
$newqage = $query->param('newqage');
$newthresh = $query->param('newthresh');
$newdiscard = $query->param('newdiscard');
$newaction = $query->param('newaction');
$newaux1 = $query->param('newaux1');
$newevirus = $query->param('newevirus');
$extensions = $query->param('extensions');
$userlist = $query->param('userlist');
$newfilter = $query->param('newfilter');
$white = $query->param('white');
$black = $query->param('black');
$exdom = $query->param('exdom');
$subject = $query->param('subject');
$newvisize = $query->param('newvisize');
$newssma = $query->param('newssma');
$newredhtml = $query->param('newredhtml');
$newqesh = $query->param('newqesh');
$newqesb = $query->param('newqesb');
$userlogin = $query->param('userlogin');
$passlogin = $query->param('passlogin');
$domainlogin = $query->param('domainlogin');
$loginchk = $query->param('loginchk');
$predate = $query->param('predate');
$update = $query->param('update');
$forward = $query->param('forward');
$sender = $query->param('sender');
$recipient = $query->param('recipient');
$date = $query->param('date');
$time = $query->param('time');
$sort = $query->param('sort');
$search  = $query->param('search');
$pcount = $query->param('pcount');
$ncount = $query->param('ncount');
}
#########################################
# Bleach Core Subroutines		#
#########################################
#####Configure Subroutine##### 
sub configure {
if ($update eq "101") {
        commitdata();
}
if ($update eq "102") {
        system "/usr/local/bleach/wrapper 1 D";
        $flag="Mail Filter Restarted Sucessfully";
}
if ($update eq "105") {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM counters where customer='$tdomain'");
        $dbh->do("INSERT INTO counters VALUES(0,0,0,0,'$tdomain')");
        $dbh->disconnect;
        $flag="Counters Cleared Successfully!";
}
refreshdata();
correctact();
if ($visize eq "") { $visize = 5000000; }
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<table border="0" width="100%">
<tr>
<td>
<center>
<form method=POST action="./bleach.cgi">
<INPUT TYPE="HIDDEN" NAME="update" VALUE="101">
<table border=2 bcolor="#000000">
<tr>
<td align=center colspan=4><h2><b>Configuration Settings</b></h2></td>
</tr>
<tr>
<td align=left colspan=2>Filter Level:</td>
<td align=left colspan=2><input type="radio" name="newfilter" value="1" $f1>Filter by Domain<input type="radio" name="newfilter" value="2" $f2>Filter by User</td>
</tr>
<tr>
<td align=left colspan=2>Filtered User Addresses:</td><td align=left colspan=2><textarea name="userlist" rows="3" cols="60">$usercontent</textarea></td>
</tr>
<tr>
<td align=left colspan=2>Action Level:</td>
<td align=left colspan=2><select name="newaction"></option>
<option selected value="$action">$a</option>
<option value="1">-----</option>
<option value="1">Attach Spam Report</option>
<option value="2">Quarantine Message</option>
<option value="6">Quarantine & Auto Discard Message</option>
<option value="3">Quarantine & Bounce Message</option>
<option value="4">Discard Message</option>
<option value="5">Bounce Message</option>
</select></td></tr>
<tr>
<td align=left colspan=2>Action Level Threshold:</td>
<td align=left colspan=2><select name="newthresh"></option>
<option selected value="$thresh">$thresh</option>
<option value="5">--</option>
HTML
$counter = 0;
while ($counter < 30.5) {
print "\<option value=\"$counter\"\>$counter\<\/option\>\n";
$counter = $counter + .5;
}
print<<HTML;
</select></td></tr>
<tr>
<td align=left colspan=2>Discard Level Threshold:</td>
<td align=left colspan=2><select name="newdiscard"></option>
<option selected value="$discard">$discard</option>
<option value="10">--</option>
HTML
$counter = 0;
while ($counter < 30.5) {
print "\<option value=\"$counter\"\>$counter\<\/option\>\n";
$counter = $counter + .5;
}
print<<HTML;
</select></td></tr>
<tr>
<td align=left colspan=2>Delete Quarantined Messages Level:</td>
<td align=left colspan=2><select name="newqage"></option>
<option selected value="$qage">$q</option>
<option value="3">-----</option>
<option value="1">1 Days</option>
<option value="2">2 Days</option>
<option value="3">3 Days</option>
<option value="4">4 Days</option>
<option value="5">5 Days</option>
</select></td>
</tr>
<tr>
<td align=left colspan=2>Filter Attachments:</td>
<td align=left colspan=2><input type="radio" name="newattach" value="1" $att1>Disabled<input type="radio" name="newattach" value="2" $att2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Filtered Attachments:</td><td align=left colspan=2><textarea name="extensions" rows="3" cols="60">$extcontent</textarea></td>
</tr>
<tr>
<td align=left colspan=2>Virus Scanning:</td>
<td align=left colspan=2><input type="radio" name="newenavirus" value="1" $enavi1>Disabled<input type="radio" name="newenavirus" value="2" $enavi2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Virus Action Level:</td>
<td align=left colspan=2><input type="radio" name="newevirus" value="1" $eva1>Clean Email<input type="radio" name="newevirus" value="2" $eva2>Clean Email & Add Message<input type="radio" name="newevirus" value="3" $eva3>Discard Email</td>
</tr>
<tr>
<td align=left colspan=2>Virus Email Scan Size Limit:</td>
<td align=left colspan=2><select name="newvisize"></option>
<option selected value="$visize">$visize</option>
<option value="50000">--</option>
HTML
$counter = 0;
while ($counter < 1000000) {
print "\<option value=\"$counter\"\>$counter\<\/option\>\n";
$counter = $counter + 25000;
}
print<<HTML;
</select></td></tr>
</tr>
<tr>
<td align=left colspan=2>Email/Domain Overrides:</td>
<td align=left colspan=2><input type="radio" name="newover" value="1" $tover1>Disabled<input type="radio" name="newover" value="1" $tover2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Allowed Email/Domain Overrides:</td><td align=left colspan=2><textarea name="white" rows="3" cols="60">$contentw</textarea></td>
</tr>
<tr>
<td align=left colspan=2>Denied Email/Domain Overrides:</td><td align=left colspan=2><textarea name="black" rows="3" cols="60">$contentb</textarea></td>
</tr>
<tr>
<td align=left colspan=2>Email/Domain Override Action:</td>
<td align=left colspan=2><input type="radio" name="newoveract" value="1" $toveract1>Quarantine Email<input type="radio" name="newoveract" value="2" $toveract2>Discard Email</td>
</tr>
<tr>
<td align=left colspan=2>Auto-Add Allowed Email/Domain Overrides:</td>
<td align=left colspan=2><input type="radio" name="newaado" value="1" $taado1>Disabled<input type="radio" name="newoveract" value="2" $taado2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Auto-Add Allow Threshold:</td>
<td align=left colspan=2><select name="newaadot"></option>
<option selected value="$aadot">$aadot</option>
<option value="0">--</option>
HTML
$counter = 0;
while ($counter < 30.5) {
print "\<option value=\"$counter\"\>$counter\<\/option\>\n";
$counter = $counter + .5;
}
print<<HTML;
</select></td>
</tr>
<tr>
<td align=left colspan=2>Auto-Add Denied Email/Domain Overrides:</td>
<td align=left colspan=2><input type="radio" name="newaddo" value="1" $taado1>Disabled<input type="radio" name="newoveract" value="2" $taddo2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Auto-Add Denied Threshold:</td>
<td align=left colspan=2><select name="newaddot"></option>
<option selected value="$addot">$addot</option>
<option value="0">--</option>
HTML
$counter = 0;
while ($counter < 30.5) {
print "\<option value=\"$counter\"\>$counter\<\/option\>\n";
$counter = $counter + .5;
}
print<<HTML;
</select></td>
</tr>
<tr>
<td align=left colspan=2>Exempt Auto-Add Email/Domains:</td><td align=left colspan=2><textarea name="exdom" rows="3" cols="60">$contentc</textarea></td>
</tr>
<tr>
<td align=left colspan=2>Remove Redundant HTML:</td>
<td align=left colspan=2><input type="radio" name="newredhtml" value="1" $tredhtml1>Disabled<input type="radio" name="newredhtml" value="2" $tredhtml2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Quarantine Emails with Suspicious Header:</td>
<td align=left colspan=2><input type="radio" name="newqesh" value="1" $tqesh1>Disabled<input type="radio" name="newqesh" value="2" $tqesh2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Quarantine Emails with Suspicious Body:</td>
<td align=left colspan=2><input type="radio" name="newqesb" value="1" $tqesb1>Disabled<input type="radio" name="newqesb" value="2" $tqesb2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Subject Matching:</td>
<td align=left colspan=2><input type="radio" name="newssm" value="1" $tssm1>Disabled<input type="radio" name="newssm" value="2" $tssm2>Enabled</td>
</tr>
<td align=left colspan=2>Subject Matching Action:</td>
<td align=left colspan=2><input type="radio" name="newssma" value="1" $tssma1>Disabled<input type="radio" name="newssma" value="2" $tssma2>Enabled</td>
</tr>
<tr>
<td align=left colspan=2>Subject Lines to Match:</td><td align=left colspan=2><textarea name="subject" rows="3" cols="60">$contents</textarea></td>
</tr>
<tr><td align=center colspan=4>
<input type=image src="../gifs/update.gif" value="Update Configuration">
</td>
</tr>
</table>
</form>
<table border="0" bcolor="#000000">
<tr>
<td align=center colspan=4><b>Other Settings</b></td>
</tr>
<tr>
<td>
<table border="0" bcolor="#000000">
<form method=POST action="./bleach.cgi";>
<INPUT TYPE="HIDDEN" NAME="update" VALUE="150">
<input type=image src="../gifs/advanced.gif" value="Advanced">
</form>
</table>
</td>
<td>
<table border="0" bcolor="#000000">
<form method=POST action="./bleach.cgi";>
<INPUT TYPE="HIDDEN" NAME="update" VALUE="105">
<input type=image src="../gifs/counters.gif" value="Clear Counters">
</form>
</table>
</td>
<td>
<table border="0" bcolor="#000000">
<form method=POST action="./bleach.cgi";>
<INPUT TYPE="HIDDEN" NAME="update" VALUE="102">
<input type=image src="../gifs/restart.gif" value="Restart Filter">
</form>
</table>
</td>
<td>
<table border="0" bcolor="#000000">
<form method=POST action="./bleach.cgi";>
<INPUT TYPE="HIDDEN" NAME="update" VALUE="103">
<input type=image src="../gifs/reboot.gif" value="Reboot Filter">
</form>
</table>
</td>
</tr>
</table>
</center>
</td></tr>
</table>
<center>
<p>$flag</p>
</center>
</body>
</html>
HTML
exit;
}
 
sub commitdata {
        @usertmp = split(/\r\n/,$userlist);
        @whitetmp = split(/\r\n/,$white);
        @exdomtmp = split(/\r\n/,$exdom);
        @blacktmp = split(/\r\n/,$black);
        @extentmp = split(/\r\n/,$extensions);
        @subjecttmp = split(/\r\n/,$subject);
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer='$tdomain'");
        $sth = $dbh->prepare("select * from userlist where customer='$tdomain'");
        $sth->execute();
        while (($tempdomain,$tempuser,$tempaux1)=$sth->fetchrow_array()) {
                $dbh->do("INSERT INTO tmpdb VALUES('$tempdomain','$tempuser','$tempaux1','0','0')");
        }
        $sth->finish();
        $dbh->do("DELETE FROM extensions where customer='$tdomain'");
        $dbh->do("DELETE FROM domain where customer='$tdomain'");
        $dbh->do("DELETE FROM userlist where customer='$tdomain'");
        $dbh->do("DELETE FROM subject where customer='$tdomain'");
        $dbh->do("DELETE FROM configuration where customer='$tdomain'");
        $dbh->do("INSERT INTO configuration VALUES('$tdomain','$newfilter','$newaction','$newthresh','$newdiscard','$newqage','$newevirus','$newattach','$newenavirus','$newover','$newssm','$newvisize','$newssma','$newredhtml','$newqesh','$newqesb','$newaado','$newaadot','$newaddot','$newaddo','$newoveract')");
        foreach $usertmp (@usertmp) {
                $usertmp =~ tr/A-Z/a-z/;
                $sth = $dbh->prepare("select aux2 from tmpdb where (customer='$tdomain') AND (aux1='$usertmp')");
                $sth->execute();
                ($tempaux1)=$sth->fetchrow_array();
                $sth->finish();
                if (defined($tempaux1) && $tempaux1 eq "1") {
                        $aux1 = "1";
                } else {
                        $aux1 = "0";
                }
                $dbh->do("INSERT INTO userlist VALUES('$tdomain','$usertmp','$aux1')");
        }
        foreach $whitetmp (@whitetmp) {
                $whitetmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO domain VALUES('$tdomain','$whitetmp','0')");
        }
        foreach $blacktmp (@blacktmp) {
                $blacktmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO domain VALUES('$tdomain','$blacktmp','1')");
        }
                foreach $exdomtmp (@exdomtmp) {
                $exdomtmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO domain VALUES('$tdomain','$exdomtmp','2')");
        }
 
        foreach $extentmp (@extentmp) {
                $extentmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO extensions VALUES('$tdomain','$extentmp')");
        }
        foreach $subjecttmp (@subjecttmp) {
                $subjecttmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO subject VALUES('$tdomain','$subjecttmp')");
        }
        $dbh->disconnect;
        $flag="Configuration Updated Sucessfully";
}
 
sub refreshdata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
        $sth = $dbh->prepare("select * from configuration where customer='$tdomain'");
        $sth->execute();
        ($customer,$filter,$action,$thresh,$discard,$qage,$evirus,$attach,$enavirus,$over,$ssm,$visize,$ssma,$redhtml,$qesh,$qesb,$aado,$aadot,$addot,$addo,$overact)=$sth->fetchrow_array();
        $sth = $dbh->prepare("select user from userlist where customer='$tdomain' order by user");
        $sth->execute();
        while (($tempuser)=$sth->fetchrow_array()) {
                $usercontent .="$tempuser\r\n";
        }
        $sth = $dbh->prepare("select * from domain where customer='$tdomain' order by domain");
        $sth->execute();
        while (($customer,$tempdomain,$adflag)=$sth->fetchrow_array()) {
                if ($adflag eq "0") {
                        $contentw .="$tempdomain\r\n";
                }
                if ($adflag eq "1") {
                        $contentb .="$tempdomain\r\n";
                }
                if ($adflag eq "2") {
                        $contentc .="$tempdomain\r\n";
                }
        }
        $sth = $dbh->prepare("select extension from extensions where customer='$tdomain' order by extension");
        $sth->execute();
        while (($tempext)=$sth->fetchrow_array()) {
                $extcontent .="$tempext\r\n";
        }
        $sth = $dbh->prepare("select subject from subject where customer='$tdomain' order by subject");
        $sth->execute();
        while (($tempext)=$sth->fetchrow_array()) {
                $contents .="$tempext\r\n";
        }
        $sth->finish();
        $dbh->disconnect;
        chop($usercontent);
        chop($usercontent);
        chop($contentw);
        chop($contentw);
        chop($contentb);
        chop($contentb);
        chop($contentc);
        chop($contentc);
        chop($extcontent);
        chop($extcontent);
        chop($contents);
        chop($contents);
}
 
sub correctact {
	#flagfix remove when done
        if ($qage eq '1') {
                $q="1 Days";
        } elsif ($qage eq '2') {
                $q="2 Days";
        } elsif ($qage eq '3') {
                $q="3 Days";
        } elsif ($qage eq '4') {
                $q="4 Days";
        } elsif ($qage eq '5') {
                $q="5 Days";
        } else {
                $q="";
        }
        if ($action eq '1') {
                $a="Attach Spam Report";
        } elsif ($action eq '2') {
                $a="Quarantine Message";
        } elsif ($action eq '3') {
                $a="Quarantine & Bounce Message";
        } elsif ($action eq '4') {
                $a="Discard Message";
        } elsif ($action eq '5') {
                $a="Bounce Message";
        } elsif ($action eq '6') {
                $a="Quarantine & Auto Discard Message";
        } else {
                $a="";
        }
        if ($filter eq '1') {
                $f1="checked";
		$f2="";
        } elsif ($filter eq '2') {
                $f1="";
		$f2="checked";
        } else {
                $f1="checked";
		$f2="";
        }
        if ($evirus eq '1') {
                $eva1="Checked";
		$eva2="";
		$eva3="";
        } elsif ($evirus eq '2') {
		$eva1="";
                $eva2="Checked";
		$eva3="";
        } elsif ($evirus eq '3') {
		$eva1="";
		$eva2="";
                $eva3="Checked";
        } else {
                $eva1="Checked";
		$eva2="";
		$eva3="";
        }
        if ($attach eq '1') {
                $att1="checked";
		$att2="";
        } elsif ($attach eq '2') {
                $att1="";
		$att2="checked";
        } else {
                $att1="checked";
		$att2="";
        }
        if ($enavirus eq '1') {
                $enavi1="Checked";
		$enavi2="";
        } elsif ($enavirus eq '2') {
                $enavi2="Checked";
		$enavi1="";
        } else {
		$enavi1="Checked";
                $enavi2="";
        }
        if ($over eq '1') {
                $tover1="checked";
		$tover2="";
        } elsif ($over eq '2') {
                $tover1="";
		$tover2="checked";
        } else {
		$tover1="checked";
                $tover2="";
        }
        if ($overact eq '1') {
                $toveract1="Checked";
		$toveract2="";
		
        } elsif ($overact eq '2') {
		$toveract1="";
                $toveract="Checked";
        } else {
		$toveract1="Checked";
                $toveract2="";
        }
        if ($aado eq '1') {
                $taado1="Checked";
		$taado2="";
        } elsif ($aado eq '2') {
                $taado1="";
		$taado2="Checked";
        } else {
                $taado1="Checked";
		$taado2="";
        }
        if ($addo eq '1') {
                $taddo1="Checked";
		$taddo2="";
        } elsif ($addo eq '2') {
		$taddo1="";
                $taddo2="Checked";
        } else {
                $taddo1="Checked";
		$taddo2="";
        }
        if ($ssm eq '1') {
                $tssm1="Checked";
		$tssm2="";
        } elsif ($ssm eq '2') {
                $tssm1="";
		$tssm2="Checked";
        } else {
                $tssm1="Checked";
		$tssm2="";
        }
        if ($ssma eq '1') {
                $tssma1="Checked";
		$tssma2="";
        } elsif ($ssma eq '2') {
                $tssma1="";
		$tssma2="Checked";
        } else {
                $tssma1="Checked";
		$tssma2="";
        }
        if ($redhtml eq '1') {
                $tredhtml1="Checked";
		$tredhtml2="";
        } elsif ($redhtml eq '2') {
                $tredhtml1="";
		$tredhtml2="Checked";
        } else {
		$tredhtml1="Checked";
                $tredhtml2="";
        }
        if ($qesh eq '1') {
                $tqesh1="Checked";
		$tqesh2="";
        } elsif ($qesh eq '2') {
                $tqesh1="";
		$tqesh2="Checked";
        } else {
		$tqesh1="Checked";
                $tqesh2="";
        }
        if ($qesb eq '1') {
                $tqesb1="Checked";
		$tqesb2="";
        } elsif ($qesb eq '2') {
		$tqesb1="";
                $tqesb2="Checked";
        } else {
		$tqesb1="Checked";
                $tqesb2="";
        }
}
#####Login Subroutine#####
sub login {
	if ($loginchk eq "1") {
        	checkvars();
        	checkpass();
	}
	if ($pass eq "1") {
        	display2();
	}
	if ($pass eq "2") {
        	display3();
	}
	if ($pass eq "0") {
        	display1();
	}
	exit;
}

sub checkvars {
        if ($userlogin eq "" || $passlogin eq "" || $domainlogin eq "") {
                print "Content-type: text/html\n\n";
		print "$userlogin $passlogin $domainlogin\n";
                print '<meta http-equiv="Refresh" content="0;URL=./bleach.cgi?update=200">';
                exit;
        }
}
 
sub checkpass {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
        $sth = $dbh->prepare("select * from customer where customer = '$domainlogin' ");
        $sth->execute();
        ($tdomain,$tusername,$tpassword,$tvalidator,$taux1,$taux2)=$sth->fetchrow_array();
                if (($userlogin eq $tusername) && ($passlogin eq $tpassword) && ($domainlogin eq $tdomain)) {
                        $pass = "1";
                        $temp = "1";
                } else {
                        $flag="Login Failed!";
                }
        $sth->finish();
        $dbh->disconnect;
        if ($temp eq "0") {
		$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
		$sth = $dbh->prepare("select authtype,authserver,authport from authentication where customer = '$domainlogin' ");
		$sth->execute();
		($authtype,$authserver,$authport)=$sth->fetchrow_array();
		if (defined($authtype) && $authtype eq "1") {
			chomp($authserver);
			my $pop3 = Net::POP3->new($authserver,Debug=> 1);
			die "Could not log onto specified server" unless $pop3;
			my $authenticate = $pop3->login($userlogin,$passlogin);
			$pop3->quit();
			if ($authenticate ne "") {
				$pass = "2";	
				$tcook = "$userlogin:$passlogin:$domainlogin";
			} else {
				$flag ="Login Failed!";
			}
		}
        }
}
 
sub display2 {
        $c = new CGI::Cookie(-name=>'access',-value=>"$domainlogin:$tvalidator",-expires=>'+3600');
        print "Set-Cookie: $c\n";
        print "Content-type: text/html\n\n";
        print '<meta http-equiv="Refresh" content="0;URL=./bleach.cgi?update=500">';
}
 
sub display3 {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("INSERT INTO tmpaccess VALUES('$tcook')");
        $dbh->disconnect;
        $c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
        print "Set-Cookie: $c\n";
        print "Content-type: text/html\n\n";
        print '<meta http-equiv="Refresh" content="0;URL=./bleach.cgi?update=600">';
}
 
sub display1 {
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<table border="0" width="100%">
<tr>
<td>
</td>
</tr>
<center>
<form method=POST action="./bleach.cgi">
<INPUT TYPE="HIDDEN" NAME="loginchk" VALUE="1">
<INPUT TYPE="HIDDEN" NAME="update" VALUE="200">
<table border="2" bcolor="#000000">
<tr>
<td align=left>Username:</td><td align=left><input size=30 type=text name=userlogin maxlength=30 value="$userlogin"></td>
</tr>
<tr>
<td align=left>Password:</td><td align=left><input size=30 type=password name=passlogin maxlength=30 value="$passlogin"></td>
</tr>
<tr>
<td align=center colspan=2 ><select name="domainlogin"></option>
<option selected value="$domainlogin">Select Domain</option>
HTML
$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
$sth = $dbh->prepare("select customer from customer order by customer");
$sth->execute();
while (($customer)=$sth->fetchrow_array()) {
        print "<option value=$customer>$customer<\/option>\n";
}
$sth->finish();
$dbh->disconnect;
print<<HTML;
</select></td>
</tr>
</center>
</table>
<br>
<input type=image src="../gifs/login.gif" value="Login">
<br>
<br>
$flag
</center>
</form>
</td>
</tr>
</table>
</body>
</html>
HTML
}
#####Logout Subroutine#####
sub logout {
displaylogout();
exit;
}
 
sub displaylogout {
        $c = new CGI::Cookie(-name=>'access',-value=>"$userval",-expires=>'+0');
        print "Set-Cookie: $c\n";
        print "Content-type: text/html\n\n";
        print '<html>';
        print '<script language="javascript">';
        print 'parent.titlebar.location.href="../title.html"';
        print '</script>';
        print '<body bgcolor="#CCCCCC" text="#000000">';
        print '<center>';
        print '<br>';
        print '<br>';
        print 'You have successfully logged out!';
        print '</center>';
        print '</body>';
        print '</html>';
 
}
#####Quarantine Subroutine#####
sub sysquarantine {
if ($update eq "402") {
        deletealldata();
}
if ($update eq "404") {
        deletedata();
}
if ($update eq "406") {
        resendata();
}
if ($update eq "408") {
        forwarddata();
}
if ($update eq "401") {
        searchdisplay();
}
 
if ($update eq "410") {
        forwardemail();
}
 
if ($update eq "412") {
        viewdata();
}
 
if ($update eq "400") {
        quarantinelist();
}
exit;
}
 
sub quarantinelist {
if ($ncount eq "" && $pcount eq "") {
        $pcount = 0;
        $ncount = 49;
        $ncounttmp1 = $ncount + 50;
        $ncounttmp2 = $pcount + 50;
        $pcounttmp1 = 49;
        $pcounttmp2 = 0;
} else {
        $pcounttmp1 = $ncount - 50;
        $pcounttmp2 = $pcount - 50;
        $ncounttmp1 = $ncount + 50;
        $ncounttmp2 = $pcount + 50;
        if ($pcounttmp1 < 50 || $pcounttmp2 < 0) {
                $pcounttmp1 = 49;
                $pcounttmp2 = 0;
        }
}
 
print "Set-Cookie: $c\n";
print "Content-type: text/html\n";
print "Pragma: no-cache\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<table border="0" width="100%">
<tr>
<td>
<center>
<table width="100%" border="2" bcolor="#000000">
<tr>
<td align=center colspan=6><h2><b>Email Quarantine</b></h2></td>
</tr>
<tr>
<td bgcolor='#999999'><font size='2' color='#000000'><center>Actions</center></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'>Date/Time</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?update=400&sort=4&search=$search&ncount=$ncount&pcount=$pcount'>Score</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?update=400&sort=1&search=$search&ncount=$ncount&pcount=$pcount'>Recipient</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?update=400&sort=2&search=$search&ncount=$ncount&pcount=$pcount'>Sender</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?update=400&sort=3&search=$search&ncount=$ncount&pcount=$pcount'>Subject</a></font></td>
</tr>
HTML
$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
if ($sort eq "1") {
        if ($search ne "") {
                $sth = $dbh->prepare("select count(*) from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%'))");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%')) order by recipient limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
        if ($search eq "") {
                $sth = $dbh->prepare("select count(*) from quarantine where customer = '$tdomain'");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where customer = '$tdomain' order by recipient limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
} elsif ($sort eq "2") {
        if ($search ne "") {
                $sth = $dbh->prepare("select count(*) from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%'))");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%')) order by sender limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
        if ($search eq "") {
                $sth = $dbh->prepare("select count(*) from quarantine where customer = '$tdomain'");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where customer = '$tdomain' order by sender limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
} elsif ($sort eq "3") {
        if ($search ne "") {
                $sth = $dbh->prepare("select count(*) from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%'))");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%')) order by subject limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
        if ($search eq "") {
                $sth = $dbh->prepare("select count(*) from quarantine where customer = '$tdomain'");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where customer = '$tdomain' order by subject limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
} elsif ($sort eq "4") {
        if ($search ne "") {
                $sth = $dbh->prepare("select count(*) from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%'))");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%')) order by score limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
        if ($search eq "") {
                $sth = $dbh->prepare("select count(*) from quarantine where customer = '$tdomain'");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where customer = '$tdomain' order by score limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
} else {
        if ($search ne "") {
                $sth = $dbh->prepare("select count(*) from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%'))");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where (customer = '$tdomain') AND ((recipient like '%$search%') OR (sender like '%$search%') OR (subject like '%$search%')) order by predate limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
        if ($search eq "") {
                $sth = $dbh->prepare("select count(*) from quarantine where customer = '$tdomain'");
                $sth->execute();
                ($dbtotal) = $sth->fetchrow_array();
                $sth = $dbh->prepare("select * from quarantine where customer = '$tdomain' order by predate limit $pcount,50");
                $sth->execute();
                while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        display();
                }
        }
}
$sth->finish();
$dbh->disconnect;
if ($ncount > $dbtotal) {
        $ncounttmp1 = $ncount;
        $ncounttmp2 = $pcount;
}
$plastcount = int($dbtotal/50)*50;
$nlastcount = int($dbtotal/50)*50 + 50;
$pcnt = $pcount + 1;
$ncnt = $ncount + 1;
print<<HTML;
<tr>
<td align=left colspan=2><b>Records $pcnt to $ncnt</b></td>
<td align=left colspan=3><b>SB = Suspicious Body &nbsp;&nbsp;&nbsp; SH = Supsicious Header<br>
V = Virus &nbsp;&nbsp;&nbsp; SM = Subject Match<br>
SD = System Denied Domain &nbsp;&nbsp;&nbsp; UD = User Denied Domain</b></td>
<td align=right colspan=1><b>Total Records $dbtotal</b></td>
</tr>
</table>
</center>
</table>
<table>
<tr>
HTML
if ($pcount > 0) {
print<<HTML;
<td><a href='./bleach.cgi?update=400&ncount=49&pcount=0&sort=$sort&search=$search'><img alt="First" src=../gifs/first.gif border=0></a></td>
<td><a href='./bleach.cgi?update=400&ncount=$pcounttmp1&pcount=$pcounttmp2&sort=$sort&search=$search'><img alt="Previous" src=../gifs/previous.gif border=0></a></td>
HTML
}
print<<HTML;
<td><a href='./bleach.cgi?update=401'><img alt="Search" src=../gifs/search.gif border=0></a></td>
<td><a href='./bleach.cgi?predate=$predate&update=402&search=$search'><img alt="Delete All" src=../gifs/delall.gif border=0></a></td>
<td><a href='./bleach.cgi?update=400'><img alt="Quarantine" src=../gifs/reports.gif border=0></a></td>
HTML
if ($ncount < $dbtotal) {
print<<HTML;
<td><a href='./bleach.cgi?update=400&ncount=$ncounttmp1&pcount=$ncounttmp2&sort=$sort&search=$search'><img alt="Next" src=../gifs/next.gif border=0></a></td>
<td><a href='./bleach.cgi?update=400&ncount=$nlastcount&pcount=$plastcount&sort=$sort&search=$search'><img alt="Last" src=../gifs/last.gif border=0></a></td>
HTML
}
print<<HTML;
</tr>
</table>
</center>
</body>
</html>
HTML
}
 
sub setcookie {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $sth = $dbh->prepare("select * from customer where customer='$cook1'");
        $sth->execute();
        ($tdomain,$tusername,$tpassword,$tvalidator,$taux1,$taux2)=$sth->fetchrow_array();
        $sth->finish();
        $dbh->disconnect;
        $tcook = "$tdomain:$tvalidator";
        if ($cook ne $tcook) {
                print "Content-type: text/html\n\n";
                print '<html>';
                print '<body bgcolor="#CCCCCC" text="#000000">';
                print '<center>';
                print '<br>';
                print '<br>';
                print 'You must be logged in and have sufficient permissions to view this page!';
                print '</center>';
                print '</body>';
                print '</html>';
                exit;
        }
        $c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
}
 
sub deletedata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$tdomain'");
        $dbh->do("INSERT INTO tmpdb VALUES ('$tdomain','$predate','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 B '$tdomain'");
        $update="400";
}
 
sub resendata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$tdomain'");
        $dbh->do("INSERT INTO tmpdb VALUES('$tdomain','$predate','$recipient','$sender','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 C '$tdomain'");
        $update="400";
}
 
sub deletealldata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$tdomain'");
        $dbh->do("INSERT INTO tmpdb VALUES('$tdomain','$search','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 G '$tdomain'");
        $search = "";
        $update ="400";
}
 
sub forwarddata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$tdomain'");
        $dbh->do("INSERT INTO tmpdb VALUES('$tdomain','$predate','$recipient','$sender','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 H '$tdomain'");
        $update="400";
}
 
sub display {
        ($da1,$da2,$da3,$da4,$da5,$da6) = split(/-/,$predate);
        $date = "$da3/$da4/$da2";
        $da5 =~ tr/./:/;
        $time = "$da5";
        print "<tr>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'>\n";
        print "<table><tr>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=412&subject=$subject&recipient=$recipient&sender=$sender&date=$date&time=$time&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>View</a></font></td>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=404&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>Delete</a></font></td></tr>\n";
        print "<tr><td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=406&subject=$subject&recipient=$recipient&sender=$sender&date=$date&time=$time&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>Resend</a></font></td>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=410&subject=$subject&recipient=$recipient&sender=$sender&date=$date&time=$time&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>Forward</a></font></td>\n";
        print "</tr></table>\n";
        print "</td>\n";
        print "<td><font size='2'>$date<br>$time</font></td>\n";
        print "<td><font size='2'>$aux2</font></td>\n";
        print "<td><font size='2'>$recipient</font></td>\n";
        print "<td><font size='2'>$sender</font></td>\n";
        print "<td><font size='2'>$subject</font></td>\n";
        print "</tr>\n";
}
 
sub searchdisplay {
        setcookie();
        print "Set-Cookie: $c\n";
        print "Content-type: text/html\n\n";
        print "<html>\n";
        print "<body bgcolor=\"#CCCCCC\" text=\"#000000\">\n";
        print "<form method=POST action=\"./bleach.cgi\">\n";
	print "<INPUT TYPE=\"HIDDEN\" NAME=\"update\" VALUE=\"400\">\n";
        print "<center>\n";
        print "<tr>\n";
        print "<td>\n";
        print "<center>\n";
        print "<table border=2 bcolor=\"#000000\">\n";
        print "<tr>\n";
        print "<td align=center colspan=2><h2><b>Search Quarantine</b></h2></td>\n";
        print "</tr>\n";
        print "<td align=center colspan=2>\&nbsp\;</td>\n";
        print "<tr>\n";
        print "</tr>\n";
        print "<tr>\n";
        print "<td align=left>Search:</td><td align=left><input size=40 type=text name=search maxlength=50 value=\"\"></td>\n";
        print "</tr>\n";
        print "</table>\n";
        print "<br>\n";
        print "<table>\n";
        print "<tr>\n";
        print "<td><input type=image src=\"../gifs/search.gif\" value=\"Search Quarantine\"></td>\n";
        print "</tr>\n";
        print "</table>\n";
        print "</form>\n";
        print "</html>\n";
        exit;
}
 
sub viewdata {
getviewdata();
$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<tr>
<td>
<center>
<table border="2" bcolor="#000000">
<tr>
<td align=center colspan=5><h2><b>View Quarantined Email</b></h2></td>
</tr>
<tr>
<td align=left>Date: $date</td><td align=left>Time: $time</td>
</tr>
<tr>
<td align=left>Recipient:</td><td align=left>$recipient</td>
</tr>
<tr>
<td align=left>Subject:</td><td align=left>$subject</td>
</tr>
<tr>
<td align=left>Sender:</td><td align=left>$sender</td>
</tr>
<tr>
<td colspan=2>
<center>
<textarea name="white" rows="20" cols="100">$content</textarea>
</center>
</td>
</tr>
</center>
</table>
<br>
<table>
<tr>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=404&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Delete" src=../gifs/delete.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=406&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Resend" src=../gifs/resend.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=410&subject=$subject&recipient=$recipient&sender=$sender&date=$date&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Forward" src=../gifs/forward.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?update=400&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Quarantine" src=../gifs/reports.gif border=0></a></font></td>
</tr>
</table>
</center>
</body>
</html>
HTML
}
 
sub getviewdata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer='$tdomain'");
        $dbh->do("INSERT INTO tmpdb VALUES('$tdomain','$predate','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 I $tdomain");
        open (TEXT,"/tmpfs/ENTIRE_MESSAGE.$tdomain");
        while (<TEXT>) {
                $content .=$_;
        }
        close (TEXT);
        system ("/bin/rm -r -f /tmpfs/ENTIRE_MESSAGE.'$tdomain'");
}
 
sub forwardemail {
$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<form method=POST action="./bleach.cgi">
<center>
<tr>
<td>
<center>
<table border="2" bcolor="#000000">
<tr>
<td align=center colspan=4><h2><b>Forward Quarantined Email</b></h2></td>
</tr>
<tr>
<td bgcolor='#999999'><font size='2' color='#000000'>Date/Time</font></td>
<td bgcolor='#999999'><font size='2' color='#000000'>Original Recipient</font></td>
<td bgcolor='#999999'><font size='2' color='#000000'>Sender</font></td>
<td bgcolor='#999999'><font size='2' color='#000000'>Subject</font></td>
</tr>
<tr>
<td><font size='2'>$date<br>$time</font></td>
<td><font size='2'>$recipient</font></td>
<td><font size='2'>$sender</font></td>
<td><font size='2'>$subject</font></td>
</tr>
<tr>
<td align=center colspan=4>&nbsp;</td>
</tr>
<tr>
<td align=center colspan=2>Forward Address:</td><td align=center colspan=2><input size=40 type=text name=recipient maxlength=50 value="$recipient"></td>
<INPUT TYPE="HIDDEN" NAME="predate" VALUE="$predate">
<INPUT TYPE="HIDDEN" NAME="update" VALUE="408">
<INPUT TYPE="HIDDEN" NAME="sender" VALUE="$sender">
<INPUT TYPE="HIDDEN" NAME="sort" VALUE="$sort">
<INPUT TYPE="HIDDEN" NAME="search" VALUE="$search">
<INPUT TYPE="HIDDEN" NAME="ncount" VALUE="$ncount">
<INPUT TYPE="HIDDEN" NAME="pcount" VALUE="$pcount">
</tr>
</table>
<br>
<table>
<tr>
<td><input type=image src="../gifs/forward.gif" value="Forward Email"><td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=404&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Delete" src=../gifs/delete.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=406&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Resend" src=../gifs/resend.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?update=400&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Quarantine" src=../gifs/reports.gif border=0></a></font></td>
</tr>
</table>
</form>
</html>
HTML
}
#####Status Subroutine#####
sub status {
$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
$sth = $dbh->prepare("select emails,quarantine,discards,virus from counters");
$sth->execute();
($emails,$quarantine,$discards,$virus)=$sth->fetchrow_array();
$sth->finish();
$sth = $dbh->prepare("select * from customer where customer='$cook1'");
$sth->execute();
($tdomain,$tusername,$tpassword,$tvalidator,$taux1,$taux2)=$sth->fetchrow_array();
$sth->finish();
$sth = $dbh->prepare("select emails,quarantine,discards,virus from counters where customer='$tdomain'");
$sth->execute();
($demails,$dquarantine,$ddiscards,$dvirus)=$sth->fetchrow_array();
$sth->finish();
$dbh->disconnect;
$total = $quarantine+$discards;
$dtotal = $dquarantine+$ddiscards;
if ($emails eq "0") {
        $pemails = 0;
        $pvirus = 0;
        $pquarantine = 0;
        $pdiscards = 0;
        $ptotal = 0;
} else {
        $pemails = int(($emails/$emails)*100);
        $pvirus = int(($virus/$emails)*100);
        $pquarantine = int(($quarantine/$emails)*100);
        $pdiscards = int(($discards/$emails)*100);
        $ptotal = int(($total/$emails)*100);
}
if ($demails eq "0") {
        $pdemails = 0;
        $pdvirus = 0;
        $pdquarantine = 0;
        $pddiscards = 0;
        $pdtotal = 0;
} else {
        $pdemails = int(($demails/$demails)*100);
        $pdvirus = int(($dvirus/$demails)*100);
        $pdquarantine = int(($dquarantine/$demails)*100);
        $pddiscards = int(($ddiscards/$demails)*100);
        $pdtotal = int(($dtotal/$demails)*100);
}
$graphpass = "$pemails:$pvirus:$pquarantine:$pdiscards:$pdemails:$pdvirus:$pdquarantine:$pddiscards";
system ("/usr/local/bleach/wrapper 1 J '$graphpass'");
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<html>
<script language="javascript">
parent.titlebar.location.href="../atitle.html"
</script>
<head><title>Bleach</title></head>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<br>
<table width="400" border="2" bcolor="#000000">
<tr>
<td align=center colspan=6><b>Bleach Status</b></td>
</tr>
<tr>
<td align=center colspan=6>Version 1.0</td>
</tr>
<tr>
<td align=center><b>Module</b></td><td colspan=2 align=center><b>Status</b></td><td align=center><b>Module</b></td><td colspan=2 align=center><b>Status</b></td>
</tr>
<tr>
<td align=left>Filter Module</td><td colspan=2 align=center><img border="0" src="../gifs/a2.gif"></td><td align=left>Database Module</td><td colspan=2 align=center><img border="0" src="../gifs/a3.gif"></td>
</tr>
<tr>
<td align=center><b>Server</b></td><td align=center colspan=2><b>Totals</b></td><td align=center><b>$tdomain</b></td><td align=center colspan=2><b>Totals</b></td>
</tr>
<tr>
<td align=left>Emails Processed</td><td align=center>$emails</td><td align=center>$pemails%</td><td><align=left>Emails Processed</td><td align=center>$demails</td><td align=center>$pdemails%</td>
</tr>
<tr>
<td align=left>Emails with Viruses</td><td align=center>$virus</td><td align=center>$pvirus%</td><td><align=left>Emails with Viruses</td><td align=center>$dvirus</td><td align=center>$pdvirus%</td>
</tr>
<tr>
<td align=left>Spam Emails Quarantined</td><td align=center>$quarantine</td><td align=center>$pquarantine%</td><td><align=left>Spam Emails Quarantined</td><td align=center>$dquarantine</td><td align=center>$pdquarantine%</td>
</tr>
<tr>
<td align=left>Spam Emails Auto-Discarded</td><td align=center>$discards</td><td align=center>$pdiscards%</td><td><align=left>Spam Emails Auto-Discarded</td><td align=center>$ddiscards</td><td align=center>$pddiscards%</td>
</tr>
<tr>
<td align=center>Spam Emails Total</td><td align=center>$total</td><td align=center>$ptotal%</td><td><align=left>Spam Emails Total</td><td align=center>$dtotal</td><td align=center>$pdtotal%</td>
</tr>
<td colspan=3 align=center><img border="0" src="../gifs/server.png"></td><td colspan=3 align=center><img border="0" src="../gifs/domain.png"></td>
</tr>
</table>
</center>
</body>
</html>
HTML
exit;
}
#Userquarantine Subroutine
sub userquarantine {
displaycount();
if ($update eq "600") {
       userquarantine2();
}
 
if ($update eq "611") {
        configuration();
}
 
if ($update eq "612") {
        updateconfiguration();
        configuration();
}
 
if ($update eq "615") {
        viewmessage();
}
 
if ($update eq "620") {
        releasemessage();
        userquarantine2();
}
 
if ($update eq "625") {
        deletemessage();
        userquarantine2();
}
 
if ($update eq "630") {
        deleteallmessages();
        userquarantine2();
}
 
if ($update eq "635") {
        userlogout();
}
 
exit;
}

sub debugger {
        $DEBUG = 1;
        if($DEBUG) {
                $| = 1;
                open(STDERR,"<&STDOUT");
        }
}
 
sub userquarantine2 {
print "Set-Cookie: $c\n";
print "Content-type: text/html\n";
print "Pragma: no-cache\n\n";
print<<HTML;
<html>
<script language="javascript">
parent.titlebar.location.href="../utitle.html"
</script>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<table border="0" width="100%">
<tr>
<td>
<center>
<table width="100%" border="2" bcolor="#000000">
<tr>
<td align=center colspan=6><h2><b>Email Quarantine for $email</b></h2></td>
</tr>
<tr>
<td bgcolor='#999999'><font size='2' color='#000000'><center>Actions</center></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'>Date/Time</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?sort=4&update=600&ncount=$ncount&pcount=$pcount'>Score</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?sort=1&update=600&ncount=$ncount&pcount=$pcount'>Recipient</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?sort=2&update=600&ncount=$ncount&pcount=$pcount'>Sender</a></font></td>
<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?sort=3&update=600&ncount=$ncount&pcount=$pcount'>Subject</a></font></td>
</tr>
HTML
$dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
if ($sort eq "1") {
        $sth = $dbh->prepare("select count(*) from quarantine where customer = '$domain' and recipient = '$email'");
        $sth->execute();
        ($dbtotal) = $sth->fetchrow_array();
        $sth = $dbh->prepare("select * from quarantine where customer = '$domain' and recipient = '$email' order by recipient limit $pcount,50");
        $sth->execute();
        while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                userdisplay();
        }
} elsif ($sort eq "2") {
        $sth = $dbh->prepare("select count(*) from quarantine where customer = '$domain' and recipient = '$email'");
        $sth->execute();
        ($dbtotal) = $sth->fetchrow_array();
        $sth = $dbh->prepare("select * from quarantine where customer = '$domain' and recipient = '$email' order by sender limit $pcount,50");
        $sth->execute();
        while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        userdisplay();
                }
} elsif ($sort eq "3") {
        $sth = $dbh->prepare("select count(*) from quarantine where customer = '$domain' and recipient = '$email'");
        $sth->execute();
        ($dbtotal) = $sth->fetchrow_array();
        $sth = $dbh->prepare("select * from quarantine where customer = '$domain' and recipient = '$email' order by subject
limit $pcount,50");
        $sth->execute();
        while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        userdisplay();
                }
} elsif ($sort eq "4") {
        $sth = $dbh->prepare("select count(*) from quarantine where customer = '$domain' and recipient = '$email'");
        $sth->execute();
        ($dbtotal) = $sth->fetchrow_array();
        $sth = $dbh->prepare("select * from quarantine where customer = '$domain' and recipient = '$email' order by score limit $pcount,50");
        $sth->execute();
        while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        userdisplay();
                }
} else {
        $sth = $dbh->prepare("select count(*) from quarantine where customer = '$domain' and recipient = '$email'");
        $sth->execute();
        ($dbtotal) = $sth->fetchrow_array();
        $sth = $dbh->prepare("select * from quarantine where customer = '$domain' and recipient = '$email' order by predate
limit $pcount,50");
        $sth->execute();
        while (($aux1,$predate,$recipient,$sender,$subject,$aux2)=$sth->fetchrow_array()) {
                        userdisplay();
                }
}
$sth->finish();
$dbh->disconnect;
if ($ncount > $dbtotal) {
        $ncounttmp1 = $ncount;
        $ncounttmp2 = $pcount;
}
$plastcount = int($dbtotal/50)*50;
$nlastcount = int($dbtotal/50)*50 + 50;
$pcnt = $pcount + 1;
$ncnt = $ncount + 1;
print<<HTML;
<tr>
<td align=left colspan=2><b>Records $pcnt to $ncnt</b></td>
<td align=left colspan=3><b>SB = Suspicious Body &nbsp;&nbsp;&nbsp; SH = Supsicious Header<br>
V = Virus &nbsp;&nbsp;&nbsp; SM = Subject Match<br>
SD = System Denied Domain &nbsp;&nbsp;&nbsp; UD = User Denied Domain</b></td>
<td align=right colspan=1><b>Total Records $dbtotal</b></td>
</tr>
</table>
</center>
</table>
<table>
<tr>
HTML
if ($pcount > 0) {
print<<HTML;
<td><a href='./bleach.cgi?update=600&ncount=49&pcount=0&sort=$sort&search=$search'><img alt="First" src=../gifs/first.gif border=0></a></td>
<td><a href='./bleach.cgi?update=600&ncount=$pcounttmp1&pcount=$pcounttmp2&sort=$sort&search=$search'><img alt="Previous" src=../gifs/previous.gif border=0></a></td>
HTML
}
print<<HTML;
<td><a href='./bleach.cgi?predate=$predate&update=630&search=$email'><img alt="Delete All" src=../gifs/delall.gif border=0></a></td>
<td><a href='./bleach.cgi?update=600'><img alt="Refresh" src=../gifs/refresh.gif border=0></a></td>
HTML
if ($ncount < $dbtotal) {
print<<HTML;
<td><a href='./bleach.cgi?update=600&ncount=$ncounttmp1&pcount=$ncounttmp2&sort=$sort&search=$search'><img alt="Next" src=../gifs/next.gif border=0></a></td>
<td><a href='./bleach.cgi?update=600&ncount=$nlastcount&pcount=$plastcount&sort=$sort&search=$search'><img alt="Last" src=../gifs/last.gif border=0></a></td>
HTML
}
print<<HTML;
</tr>
</table>
</center>
</body>
</html>
HTML
}
 
sub configuration {
userrefreshdata();
correctacct();
$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<table border="0" width="100%">
<tr>
<td>
<center>
<form method=POST action="./bleach.cgi">
<INPUT TYPE="HIDDEN" NAME="update" VALUE="612">
<table border=2 bcolor="#000000">
<tr>
<td align=center colspan=4><h2><b>Configuration for $email</b></h2></td>
</tr>
<tr>
<td align=left colspan=2>Bleach Custom Filter Settings:</td>
<td align=left colspan=2><select name="newaux1"></option>
<option selected value="$aux1">$b</option>
<option value="">-----</option>
<option value="0">Disable</option>
<option value="1">Enable</option>
</select></td>
</tr>
<tr>
<td align=left colspan=2>Bleach Filter Level:</td>
<td align=left colspan=2><select name="newfilter"></option>
<option selected value="$filter">$f</option>
<option value="">-----</option>
<option value="1">Very Low</option>
<option value="2">Low</option>
<option value="3">Medium</option>
<option value="4">High</option>
<option value="5">Very High</option>
<option value="6">Aggressive</option>
</select></td>
</tr>
<tr>
<td align=left colspan=2>Bleach Action Level:</td>
<td align=left colspan=2><select name="newaction"></option>
<option selected value="$action">$a</option>
<option value="">-----</option>
<option value="1">Attach Spam Report</option>
<option value="2">Quarantine Message</option>
<option value="4">Discard Message</option>
<option value="6">Quarantine & Auto Discard Message</option>
</select></td></tr>
<tr>
<td align=left>Always Allowed Domains:</td><td align=left><textarea name="white" rows="8" cols="40">$contentw</textarea></td>
<td align=left>Always Denied Domains:</td><td align=left><textarea name="black" rows="8" cols="40">$contentb</textarea></td></tr>
<tr><td align=center colspan=4>
<input type=image src="../gifs/update.gif" value="Update Configuration">
</td>
</tr>
</table>
</form>
<center>
<p>$flag</p>
</center>
</body>
</html>
HTML
}
 
sub viewmessage {
usergetviewdata();
$c = new CGI::Cookie(-name=>'access',-value=>"$tcook",-expires=>'+3600');
print "Set-Cookie: $c\n";
print "Content-type: text/html\n\n";
print<<HTML;
<html>
<body bgcolor="#CCCCCC" text="#000000">
<center>
<tr>
<td>
<center>
<table border="2" bcolor="#000000">
<tr>
<td align=center colspan=5><h2><b>View Quarantined Email for $email</b></h2></td>
</tr>
<tr>
<td align=left>Date: $date</td><td align=left>Time: $time</td>
</tr>
<tr>
<td align=left>Recipient:</td><td align=left>$recipient</td>
</tr>
<tr>
<td align=left>Subject:</td><td align=left>$subject</td>
</tr>
<tr>
<td align=left>Sender:</td><td align=left>$sender</td>
</tr>
<tr>
<td colspan=2>
<center>
<textarea name="white" rows="20" cols="100">$content</textarea>
</center>
</td>
</tr>
</center>
</table>
<br>
<table>
<tr>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=625&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Delete" src=../gifs/delete.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?predate=$predate&update=620&recipient=$recipient&sender=$sender&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'><img alt="Release" src=../gifs/release.gif border=0></a></font></td>
<td><font size='3' color='#000000'><a href='./bleach.cgi?sort=$sort&search=$search&update=600&ncount=$ncount&pcount=$pcount'><img alt="Quarantine" src=../gifs/reports.gif border=0></a></font></td>
</tr>
</table>
</center>
</body>
</html>
HTML
}
 
sub usergetviewdata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer='$username2'");
        $dbh->do("INSERT INTO tmpdb VALUES('$username2','$predate','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 I $username2");
        open (TEXT,"/tmpfs/ENTIRE_MESSAGE.$username2");
        while (<TEXT>) {
                $content .=$_;
        }
        close (TEXT);
        system ("/bin/rm -r -f /tmpfs/ENTIRE_MESSAGE.$username2");
}
 
 
sub userdisplay {
        ($da1,$da2,$da3,$da4,$da5,$da6) = split(/-/,$predate);
        $date = "$da3/$da4/$da2";
        $da5 =~ tr/./:/;
        $time = "$da5";
        print "<tr>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'>\n";
        print "<table><tr>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=615&subject=$subject&recipient=$recipient&sender=$sender&date=$date&time=$time&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>View</a></font></td>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=620&subject=$subject&recipient=$recipient&sender=$sender&date=$date&time=$time&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>Release</a></font></td>\n";
        print "<td bgcolor='#999999'><font size='2' color='#000000'><a href='./bleach.cgi?predate=$predate&update=625&sort=$sort&search=$search&ncount=$ncount&pcount=$pcount'>Delete</a></font></td>\n";
        print "</tr></table>\n";
        print "</td>\n";
        print "<td><font size='2'>$date \/ $time</font></td>\n";
        print "<td><font size='2'>$aux2</font></td>\n";
        print "<td><font size='2'>$recipient</font></td>\n";
        print "<td><font size='2'>$sender</font></td>\n";
        print "<td><font size='2'>$subject</font></td>\n";
        print "</tr>\n";
}
 
sub releasemessage {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$username2'");
        $dbh->do("INSERT INTO tmpdb VALUES('$username2','$predate','$recipient','$sender','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 H '$username2'");
}
 
sub deletemessage {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$username2'");
        $dbh->do("INSERT INTO tmpdb VALUES ('$username2','$predate','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 B '$username2'");
}
 
sub displaycount {
        if ($ncount eq "" && $pcount eq "") {
                $pcount = 0;
                $ncount = 49;
                $ncounttmp1 = $ncount + 50;
                $ncounttmp2 = $pcount + 50;
                $pcounttmp1 = 49;
                $pcounttmp2 = 0;
        } else {
                $pcounttmp1 = $ncount - 50;
                $pcounttmp2 = $pcount - 50;
                $ncounttmp1 = $ncount + 50;
                $ncounttmp2 = $pcount + 50;
                if ($pcounttmp1 < 49 || $pcounttmp2 < 0) {
                        $pcounttmp1 = 49;
                        $pcounttmp2 = 0;
                }
        }
}
 
sub deleteallmessages {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpdb where customer = '$domain'");
        $dbh->do("INSERT INTO tmpdb VALUES('$domain','$email','0','0','0')");
        $dbh->disconnect;
        system ("/usr/local/bleach/wrapper 1 K '$domain'");
        $search = "";
}
 
sub userlogout {
        if ($cook ne $tcook) {
                print "Content-type: text/html\n\n";
                print '<html>';
                print '<body bgcolor="#CCCCCC" text="#000000">';
                print '<center>';
                print '<br>';
                print '<br>';
                print 'You have not logged in yet!';
                print '</center>';
                print '</body>';
                print '</html>';
                exit;
        }
        $c = new CGI::Cookie(-name=>'useraccess',-value=>"$userval",-expires=>'+0');
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM tmpaccess where customer = '$tcook'");
        $dbh->disconnect;
        print "Set-Cookie: $c\n";
        print "Content-type: text/html\n\n";
        print '<html>';
        print '<script language="javascript">';
        print 'parent.titlebar.location.href="../title.html"';
        print '</script>';
        print '<body bgcolor="#CCCCCC" text="#000000">';
        print '<center>';
        print '<br>';
        print '<br>';
        print 'You have successfully logged out!';
        print '</center>';
        print '</body>';
        print '</html>';
}
 
sub updateconfiguration {
        @whitetmp = split(/\r\n/,$white);
        @blacktmp = split(/\r\n/,$black);
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Failure";
        $dbh->do("DELETE FROM userdomain where customer='$email'");
        $dbh->do("DELETE FROM userprefs where customer='$email'");
        $dbh->do("UPDATE userlist set aux1='$newaux1' where user='$email'");
        if ($newfilter eq '1') {
                $newthresh = "8";
                $newdiscard = "16";
        } elsif ($newfilter eq '2') {
                $newthresh = "6";
                $newdiscard = "14";
        } elsif ($newfilter eq '3') {
                $newthresh = "4";
                $newdiscard = "12";
        } elsif ($newfilter eq '4') {
                $newthresh = "3";
                $newdiscard = "11";
        } elsif ($newfilter eq '5') {
                $newthresh = "2";
                $newdiscard = "10";
        } elsif ($newfilter eq '6') {
                $newthresh = "1";
                $newdiscard = "9";
        } else {
                $newthresh = "8";
                $newdiscard = "16";
        }
        $dbh->do("INSERT INTO userprefs VALUES('$email','$newfilter','$newaction','$newthresh','$newdiscard','$newqage','$newevirus','0','0')");
        foreach $whitetmp (@whitetmp) {
                $whitetmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO userdomain VALUES('$email','$whitetmp','0')");
        }
        foreach $blacktmp (@blacktmp) {
                $blacktmp =~ tr/A-Z/a-z/;
                $dbh->do("INSERT INTO userdomain VALUES('$email','$blacktmp','1')");
        }
        $flag="Configuration Updated Sucessfully";
}
 
sub userrefreshdata {
        $dbh = DBI->connect($dsn,$dbu,$dbp) or die "Access Failed";
        $sth = $dbh->prepare("select aux1 from userlist where user='$email'");
        $sth->execute();
        ($aux1)=$sth->fetchrow_array();
        $sth = $dbh->prepare("select * from userprefs where customer='$email'");
        $sth->execute();
        ($customer,$filter,$action,$thresh,$discard,$qage,$evirus,$aux2,$aux3)=$sth->fetchrow_array();
        $sth = $dbh->prepare("select * from userdomain where customer='$email' order by domain");
        $sth->execute();
        while (($customer,$tempdomain,$adflag)=$sth->fetchrow_array()) {
                if ($adflag eq "0") {
                        $contentw .="$tempdomain\r\n";
                }
                if ($adflag eq "1") {
                        $contentb .="$tempdomain\r\n";
                }
        }
        $sth->finish();
        $dbh->disconnect;
        chop($contentw);
        chop($contentw);
        chop($contentb);
        chop($contentb);
}
 
 
sub correctacct {
        if ($action eq '1') {
                $a="Attach Spam Report";
        } elsif ($action eq '2') {
                $a="Quarantine Message";
        } elsif ($action eq '4') {
                $a="Discard Message";
        } elsif ($action eq '6') {
                $a="Quarantine & Auto Discard Message";
        } else {
                $a="";
        }
        if ($filter eq '1') {
                $f="Very Low";
        } elsif ($filter eq '2') {
                $f="Low";
        } elsif ($filter eq '3') {
                $f="Medium";
        } elsif ($filter eq '4') {
                $f="High";
        } elsif ($filter eq '5') {
                $f="Very High";
        } elsif ($filter eq '6') {
                $f="Agressive";
        } else {
                $f="";
        }
        if ($aux1 eq '0') {
                $b="Disable";
        } elsif ($aux1 eq '1') {
                $b="Enable";
        } else {
                $b="";
        }
 
}
#####Core Subroutine##### 
sub core {

}
