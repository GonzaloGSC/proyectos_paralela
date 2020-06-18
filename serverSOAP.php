<?php
    
    include_once('clases.php');
    ini_set("soap.wsdl_cache_enabled", "0");
    
    $directorioWSDL = "directorioWSDL/miWSDL.wsdl";
    
    $parametros = array(
        'uri'=>'http://localhost/',
        'soap_version'=>SOAP_1_1
    );
    
$ObjetoServer = new SoapServer($directorioWSDL,$parametros);
$ObjetoServer->setClass("servicios");
$ObjetoServer->handle();
    
?>