<?php
$url = "http://localhost:8000/?wsdl";
//$client = @new SoapClient('http://localhost:8000/?wsdl');
try{
    $clienteSOAP = new SoapClient($url,array(
        ‘location’=>$endpoint,
        ‘trace’=>true,
        ‘exceptions’=>false));
//$respuesta1=$client->multiplica(4,5);
$respuesta2=$client->sumar(null,4,5);
/*$csv = fopen("http://localhost/documentos.csv","r");
$dato = mime_content_type($csv);
$dato2 = base64_encode($dato);
$respuesta3=$client->recibido($dato2);

echo $respuesta1.' '.$respuesta2.' '.$respuesta3;
*/
} catch (Exception $e) {
echo 'Error --> '. $e->getMessage();
}
?>