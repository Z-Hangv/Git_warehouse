<?php 

/* 
开发文档，本程序ROBOTAPI.PHP可以接受外部指令，实现远程控制机器人
*/

$cmd = $_POST['cmd'];

if ( $cmd == "") {
	echo "post error";
	die;
}

$cmd = $cmd.'<end>';

$host="localhost";
$port=7705;
$socket=socket_create(AF_INET,SOCK_STREAM,SOL_TCP)or die("cannot create socket\n");
$conn=socket_connect($socket,$host,$port) or die("cannot connect robot com server, host: ".$host." port: ".$port."\n");
if($conn)
{
	socket_write($socket, $cmd) or die("cannot send data\n");
	$res = socket_read($socket, 1024);
	echo $res;
	socket_close($socket);
	// echo $cmd;
}
else{
	echo "failed";
}
?>
