<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col text-left">
                <h2>Listado carreras</h2>

                <div class = "col-md-12">
                    <b-table striped hover :items="carreras" :fields="campos">
                    </b-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data(){
        return{
            campos: [
                {key: 'Nombre', label: 'Nombre carrera'},
                {key: 'Codigo', label: 'Codigo carrera'},
                {key: 'Nem', label: 'Nem'},
                {key: 'Ranking', label: 'Ranking'},
                {key: 'Lenguaje', label: 'Lenguaje'},
                {key: 'Matematicas', label: 'Matematicas'},
                {key: 'Historia', label: 'Historia'},
                {key: 'Ciencias', label: 'Ciencias'},
                {key: 'PuntajePromedio', label: 'Puntaje promedio'},
                {key: 'PuntajeMinimo', label: 'Puntaje minimo'},
                {key: 'Vacantes', label: 'Vacantes'},
                {key: 'PrimerMatriculado', label: 'Primer matriculado'},
                {key: 'UltimoMatriculado', label: 'Ultimo matriculado'}
            ],
            carreras: []
        }
    },
    methods: {
        getpuntajes(){
            const path ='http://127.0.0.1:8000/api/v0.01/postulante/'
            axios.get(path).then((responce) => {
                this.carreras = responce.data
            })
            .catch((error) => {
                console.log(error)
            })
        }
    },
    created(){
        this.getpuntajes()
    }
}
</script>

<style lang = "css" scoped>
</style>