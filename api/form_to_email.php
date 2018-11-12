<?php
if(!isset($_POST['submit'])){

//This page should not be accessed directly.
  echo "error, you need to submit the form.";
}
$email = $_POST['email'];
$content = $_POST['txt_comments'];

//Validate first
if(empty($email)){

  echo "Email is mandatory"
  exit;

}

if(IsInjected($email)){

  echo "Bad email value";
  exit;

}

$email_subject = "Complaint";
$email_body = "This is the whiner: $email.\n Here is the quarrel good sir:\n $content";
$to = "alexander_rodriguez20@milton.edu";//haedmonitor email
//Send the email!
mail($to,$email_subject,$email_body);
//done. redirect to thank-you
// header()//not sure How

//Validate against email injection
function IsInjected($str){

  $injections = array('(\n+)',
              '(\r+)',
              '(\t+)',
              '(%0A+)',
              '(%0D+)',
              '(%08+)',
              '(%09+)'
              );
  $inject = join('|', $injections);
  $inject = "/$inject/i";
  if(preg_match($inject,$str))
    {
    return true;
  }
  else
    {
    return false;
  }

}



?>
