///////////////////////////////////////////////////////////////////////////////LIBRERIAS///////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <cstdlib>
#include <opencv4/opencv2/opencv_modules.hpp>
#include <opencv4/opencv2/photo.hpp>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/core/core.hpp>
#include <opencv4/opencv2/core.hpp>
#include <mpi.h>
#include <string>
#include <vector>
#include <ctime>
#include <cmath>
#include <pthread.h>

using namespace cv;
using namespace std;

///////////////////////////////////////////////////////////////////////////////V. GLOBALES///////////////////////////////////////////////////////////////////////////////

Mat trozoImagen, resultadoParcial;

///////////////////////////////////////////////////////////////////////////////FUNCIONES///////////////////////////////////////////////////////////////////////////////

/**
 * Funcion de los autores.
*/
void integrantes();

/**
 * Funcion que guarda la imagen procesada
 * @param image Ingreso de imagen en formato mat
 * @param operation Ingreso del numero de opcion
*/
void guardarImagenResultado(Mat image, string operation);

/**
 * Función utilizada para generar copias de una imagen o parte de estas si se desea
 * @param ientrante Imagen original
 * @param idestino Imagen a donde se guardara lo copiado
 * @param primx primera coordenada X de de la copia
 * @param primy primera coordenada Y de de la copia
 * @param ultix ultima coordenada X de de la copia
 * @param ultiy ultima coordenada X de de la copia
*/
void copiarTrozoImagen(Mat ientrante, Mat idestino, int primx, int primy, int ultix, int ultiy);

/**
 * Función para establecer comunicacion de evnio entre los procesadores
 * @param imagenParaEnvio La imagen que se envia
 * @param idestino Se ingresa el rank del receptor
*/
void enviarImagen(Mat imagenParaEnvio, int idestino);

/**
 * Función para establecer comunicacion de recepcion entre los procesadores
 * @param imgToRecv Donde se guarda la imagen
 * @param ientrante Se ingresa el rank del emisor
*/
void recibirImagen(Mat &imgToRecv,int ientrante);



///////////////////////////////////////////////////////////////////////////////PROGRAMA PRINCIPAL///////////////////////////////////////////////////////////////////////////////
/**
 * Funcion del programa principal
 * @param argc Cantidad de argumentos
 * @param argv Vector de argumentos
 * @return resultado de la operacion
*/
int main(int argc, char** argv ){

    if(argc > 2)///Detecta los argumentos de ingreso, son necesarios 3 argumentos, si se ingresan mas se ignoran los sobrantes
    {
        //Definicion de variables, rank sera el numero de procesador, procesadores el numero total de estos e imagen 

        int rank, procesadores;
        Mat imagen;
        //Se inicia el MPI
        MPI_Init(&argc, &argv);
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &procesadores);
        string opcion(argv[1]);

        ///////////////////////EL MAESTRO DISTRIBUYE EL TRABAJO
        if(rank == 0)
        {
            imagen = imread(argv[2],IMREAD_COLOR); //Guarda en la variable tipo mat "imagen", la lectura de la informacion de la imagen ingresada.
            int dimensionParticion = imagen.cols / procesadores; //Divide la imagen a procesar en partes iguales, en base al numero de procesadores que trabajaran.
            int bordeSuperior = dimensionParticion; //Limite superior inicial para trabajar la imagen.
            int bordeInferior = 0; //Limite inferior inicial para trabajar la imagen.
            trozoImagen.create(imagen.rows,dimensionParticion, CV_8UC4);//Se crea una trozo de imagen inicial, destinado esclusivamente para el maestro (su parte del trabajo); 8u = imagen de 8 bits,C4 = 4 canales
            copiarTrozoImagen(imagen,trozoImagen,0,0,dimensionParticion,imagen.rows);//Se copia del trozo de imagen destinado al maestro.

            for(int proce = 1; proce < procesadores; proce++)//Bucle destinado a repartir el trabajo entre los procesadores participantes restantes
            {
                bordeInferior = (dimensionParticion * proce); // En base al numero del procesador se designan los bordes o margenes del trabajo en la imagen
                bordeSuperior = (dimensionParticion * (proce + 1)); 
                if(proce+1 == procesadores)
                {
                    bordeSuperior = imagen.cols;
                }
                int diferencia = bordeSuperior - bordeInferior;
                Mat imagenParaEnvio(Size(diferencia, imagen.rows), CV_8UC4); /// Se realiza el la creacion de la plantilla para la imagen a enviar
                copiarTrozoImagen(imagen, imagenParaEnvio, bordeInferior, 0, bordeSuperior, imagen.rows);// Se copia el contenido de la imagen original a la plantilla que corresponde al procesador de turno
                enviarImagen(imagenParaEnvio, proce);// Se envia la imagen para su procesamiento al procesador correspondiente
            }
        }
        else
        {
            recibirImagen(trozoImagen,0);// Recepcion del trabajo o los trozos de la imagen a procesar por parte de los esclavos >:c
            
        }

        ///////////////////////SE CREA EL ESPACIO DE TRABAJO 

        if(opcion == "1" || opcion == "2")
        {
            resultadoParcial = trozoImagen.clone();
        }
        else if(opcion == "3"){
            int columnasAgregadas = trozoImagen.cols * 2.0;
            int filasAgregadas = trozoImagen.rows * 2.0;
            resultadoParcial.create(filasAgregadas, columnasAgregadas, CV_8UC4);
        }
        
        ///////////////////////PROCESAMIENTO DE LAS IMAGENES O TROZOS DE ESTAS EN BASE A LA OPCION INGRESADA
        if(opcion=="1")
        {
            GaussianBlur(trozoImagen, resultadoParcial, Size(7,7), 0,0,1); //Funcion maravillosa que realiza el difuminado de la imagen o el trozo de esta por el metodo de gauss.
        }
        if(opcion=="2")
        {
            for(int x=0; x<trozoImagen.cols; x++) // Bucle de doble for que se encarga de obtener el escalado de grises para la imagen, en base al promedio de los colores de los canales.
            {
                for(int y=0; y<trozoImagen.rows; y++)
                {
                    float valores_promedio = 0;
                    valores_promedio = (trozoImagen.at<Vec4b>(y,x)[0] + trozoImagen.at<Vec4b>(y,x)[1] + trozoImagen.at<Vec4b>(y,x)[2])/3;
                    resultadoParcial.at<Vec4b>(y,x)[0] = valores_promedio;//Se iguala al promedio, que equivale a la tonalidad en grises
                    resultadoParcial.at<Vec4b>(y,x)[1] = valores_promedio;//Se iguala al promedio, que equivale a la tonalidad en grises
                    resultadoParcial.at<Vec4b>(y,x)[2] = valores_promedio;//Se iguala al promedio, que equivale a la tonalidad en grises
                }
            }
        }
        if(opcion=="3")
        {
            resize(trozoImagen,resultadoParcial,cv::Size(0,0),2,2, INTER_NEAREST);// Re-escalado de la imagen o trozo al doble del tamaño original
        }

        ///////////////////////PROCESAMIENTO DE LAS IMAGENES O TROZOS DE ESTAS PARA SU UNION
        if(opcion == "1" || opcion == "2" || opcion == "3")
        {
            if(rank == 0)// Si se trata del maestro, realiza las operaciones de union de los trozos de la imagen ya procesados
            {
                Mat imagenFinal(imagen.rows, imagen.cols, CV_8UC4);
                imagenFinal = resultadoParcial.clone();//Debido a que siempre sera el maestro el primero en aportar con una parte del proceso, se iguala la imagen final al trabajo realizado pore este.

                for(int p = 1; p < procesadores; p++)//Luego de lo anterior, recolecta el trabajo de los esclavos, uno a uno, y los va juntando en la imagen final.
                {
                    Mat imagenTemporal(resultadoParcial.rows, resultadoParcial.cols, CV_8UC4);//Crea la imagen temporal donde se guarda lo recibido por parte de los esclavos.
                    recibirImagen(imagenTemporal, p);
                    hconcat(imagenFinal, imagenTemporal, imagenFinal);//Operacion clave, la encargada de juntar todas las imagenes recibidas para formar la imagen resultante o final.
                }
                guardarImagenResultado(imagenFinal, opcion);//Guarda la imagen procesada y completa. 
            }
            else
            {
                enviarImagen(resultadoParcial, 0);// Si nos e trata del maestro, envia la imagen trabajada al maestro para su union.
            }
        }
        else
        {
            if(rank == 0)
                cout<<"\nLa opcion ingresada no existe, utilice los numeros 1,2 o 3.\n";
            return EXIT_FAILURE;
        }

        if(rank == 0)
            cout<<"\nFinalizacion exitosa.\n";
        MPI_Finalize();
    }
    else
    {
        cout<<"\nArgumentos mal ingresados, ej) ./dist/programa [Num.opcion] [path imagen]\n";
        return EXIT_FAILURE;
    }
    integrantes();
    return EXIT_SUCCESS;
}

///////////////////////////////////////////////////////////////////////////////FUNCIONES (CUERPO)///////////////////////////////////////////////////////////////////////////////

void guardarImagenResultado(Mat image, string operation){
    time_t rawtime;
    struct tm * timeinfo;
    char buffer[80];
    time (&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer,sizeof(buffer),"%Y%m%d%I%M%S",timeinfo); 
    std::string str(buffer);
    imwrite("operacion_"+operation+"_"+str+".png",image);
}

void copiarTrozoImagen(Mat ientrante, Mat idestino, int primx, int primy, int ultix, int ultiy)
{
    for(int x = 0; x<ultix-primx; x++){
        for(int y = 0; y<ultiy-primy; y++){
            idestino.at<Vec4b>(y,x)[0] = ientrante.at<Vec3b>(y,x+primx)[0];
            idestino.at<Vec4b>(y,x)[1] = ientrante.at<Vec3b>(y,x+primx)[1];
            idestino.at<Vec4b>(y,x)[2] = ientrante.at<Vec3b>(y,x+primx)[2];
            idestino.at<Vec4b>(y,x)[3] = 255;
        }
    }
}

void enviarImagen(Mat imagenParaEnvio, int idestino){
    int sizes[3];

    sizes[2] = imagenParaEnvio.elemSize();
    Size s = imagenParaEnvio.size();
    sizes[0] = s.height;
    sizes[1] = s.width;
    MPI_Send( sizes, 3, MPI_INT,idestino,0,MPI_COMM_WORLD);
    MPI_Send( imagenParaEnvio.data, sizes[0]*sizes[1]*4, MPI_CHAR,idestino,1, MPI_COMM_WORLD);
}

void recibirImagen(Mat &imagenParaRecibir,int ientrante){
    MPI_Status estado;
    int sizes[3];
    MPI_Recv( sizes,3, MPI_INT,ientrante,0, MPI_COMM_WORLD, &estado);
    imagenParaRecibir.create(sizes[0], sizes[1], CV_8UC4);
    MPI_Recv( imagenParaRecibir.data, sizes[0] * sizes[1] * 4, MPI_CHAR, ientrante, 1, MPI_COMM_WORLD, &estado);
}

void integrantes()
{
    cout<<"Integrantes:\n";
    cout<<"            - Ignacio Valdes.\n";
    cout<<"            - Camila Carrasco.\n";
    cout<<"            - Gonzalo Salinas.\n";
}