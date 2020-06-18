<?php

class servicios{
    
    public function informacionActualServer($variable){
        
        $fecha = date("F j, Y, g:i:s a");
        
        $datos = $variable->mensaje." ".$fecha;
        
        $objeto_respuesta = new stdClass ();
        $objeto_respuesta->out=$datos;
        
        return $objeto_respuesta;
    }
}
?>
