from suds.client import Client
import base64
import os
wsdl = Client('http://localhost:8000/?wsdl')
print (wsdl.service.metodo(arg1,arg2))

def codificar(textoSinCodificar):
    base64_cadena_bytes = base64.b64encode(textoSinCodificar.encode('ascii'))
    texto_base64 = base64_cadena_bytes.decode('ascii')
    return texto_base64


def generarXlsx(rutss,puntajess):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        writer = pandas.ExcelWriter(dir_path+"/"+"UTEM.xlsx") # pylint: disable=abstract-class-instantiated
        for i in range(0,28):
            df = pandas.DataFrame({
                "Nº": [int(j)+1 for j in range(len(puntajess[i]))],
                "RUT Matriculado": rutss[i],
                "Puntaje": puntajess[i]})
            df = df[["Nº", "RUT Matriculado", "Puntaje"]]
            if (i==0):
                df.to_excel(writer, "Administración Pública", index=False)
            if (i==1):
                df.to_excel(writer, "Bibliotecología y Documentación", index=False)
            if (i==2):
                df.to_excel(writer, "Contador Público y Auditor", index=False)
            if (i==3):
                df.to_excel(writer, "Ing. Comercial", index=False)
            if (i==4):
                df.to_excel(writer, "Ing. en Adm. Agroindustrial", index=False)
            if (i==5):
                df.to_excel(writer, "Ing. en Comercio Inter.", index=False)
            if (i==6):
                df.to_excel(writer, "Ing. en Gestión Turística", index=False)
            if (i==7):
                df.to_excel(writer, "Arquitectura", index=False)
            if (i==8):
                df.to_excel(writer, "Ing. Civil en Obras Civiles", index=False)
            if (i==9):
                df.to_excel(writer, "Ing. en Construcción", index=False)
            if (i==10):
                df.to_excel(writer, "Ing. Civil en Prev. de R.", index=False)
            if (i==11):
                df.to_excel(writer, "Ing.en Biotecnología", index=False)
            if (i==12):
                df.to_excel(writer, "Ing. en Ind. Alimentaria", index=False)
            if (i==13):
                df.to_excel(writer, "Ing. en Química", index=False)
            if (i==14):
                df.to_excel(writer, "Química Ind.", index=False)
            if (i==15):
                df.to_excel(writer, "Diseño en Comunicación Visual", index=False)
            if (i==16):
                df.to_excel(writer, "Diseño Ind.", index=False)
            if (i==17):
                df.to_excel(writer, "Trabajo Social", index=False)
            if (i==18):
                df.to_excel(writer, "Bach. en Ciencias de la Ing.", index=False)
            if (i==19):
                df.to_excel(writer, "Dibujante Proyectista", index=False)
            if (i==20):
                df.to_excel(writer, "Ing. Civil en Comp.", index=False)
            if (i==21):
                df.to_excel(writer, "Ing. Civil Ind.", index=False)
            if (i==22):
                df.to_excel(writer, "Ing. Civil en Ciencia de Datos", index=False)
            if (i==23):
                df.to_excel(writer, "Ing. Civil Electrónica", index=False)
            if (i==24):
                df.to_excel(writer, "Ing. Civil en Mecánica", index=False)
            if (i==25):
                df.to_excel(writer, "Ing. en Geomensura", index=False)
            if (i==26):
                df.to_excel(writer, "Ing. en Informática", index=False)
            if (i==27):
                df.to_excel(writer, "Ing. Ind.", index=False)
        writer.save()