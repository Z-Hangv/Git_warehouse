<?php
$log = $_GET['log'];
$file_path = "C:/myprojects/xrobot4/xrobot4a/deploy/pi/root/robot/log/".$log;
$myfile = fopen($file_path, "r") or die("Unable to open file!");
$content = fread($myfile,filesize($file_path));
$content = str_replace("\n", "<br>\n", $content);
echo $content;
fclose($myfile);
?>