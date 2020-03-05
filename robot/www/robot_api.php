<?php 

/* 
开发文档，本程序ROBOTAPI.PHP可以接受外部指令，实现远程控制机器人
指令接入是由URL传递的， 格式是： "http://192.168.0.104/robot_api.php?module=hello&sparam=null&loop=1"
IP地址： 127.0.0.1是机器人主机的IP地址。
*/

$module = $_GET['module'];
$loop = $_GET['loop'];
$param = $_GET['sparam'];
$priority = $_GET['priority'];

// echo $param;

if ($module == "") {
	echo "URL error, should be : robot_api.php?module=hello&sparam=null&loop=1&priority=5";
	die;
}

if ($loop == "") $loop = 1;
if ($param == "") $param = "null";

$host="localhost";
$port=7701;
$socket=socket_create(AF_INET,SOCK_STREAM,SOL_TCP)or die("cannot create socket\n");
$conn=socket_connect($socket,$host,$port) or die("cannot connect robot script server, host: ".$host." port: ".$port."\n");
if($conn)
{
	$script1 = "{'action':'runmodule', 'module': '".$module."', 'param': '".$param."', 'priority': '".$priority."', 'loop':'".$loop."'}<end>";
	socket_write($socket, $script1) or die("cannot send data\n");
	socket_close($socket);
	echo "succeed: ".$script1;
}
else{
	echo "failed";
}
?>
