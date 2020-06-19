<?php
try{
$client = @new SoapClient(null,array('location' => 'http://localhost/servicios.php','uri' => 'urn:webservices'));
$respuesta1=$client->multiplica(4,5);
$respuesta2=$client->suma(4,5);
$csv = fopen("http://localhost/documentos.csv","r");
$dato = mime_content_type($csv);
$dato2 = base64_encode($dato);
$respuesta3=$client->recibido($dato2);

echo $respuesta1.' '.$respuesta2.' '.$respuesta3;
} catch (Exception $e) {
echo 'Error --> '. $e->getMessage();
}
?>