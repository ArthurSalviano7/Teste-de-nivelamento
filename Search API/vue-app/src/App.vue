<template>
  <div>
    <h2>Buscar Operadores</h2>
    <form @submit.prevent="buscarOperadores">
      
      <label for="reg">Registro_ANS:  </label>
      <input type="text" v-model="filtros.reg" id="reg" /><br>

      <label for="cnpj">CNPJ: </label>
      <input type="text" v-model="filtros.cnpj" id="cnpj" /><br>

      <label for="corp_name">Razão Social:  </label>
      <input type="text" v-model="filtros.corp_name" id="corp_name" /><br>

      <label for="fantasy_name">Nome Fantasia:  </label>
      <input type="text" v-model="filtros.fantasy_name" id="fantasy_name" /><br>

      <label for="modality">Modalidade: </label>
      <input type="text" v-model="filtros.modality" id="modality" /><br>
      
      <label for="city">Cidade: </label>
      <input type="text" v-model="filtros.city" id="city" /><br>

      <label for="state">UF:  </label>
      <input type="text" v-model="filtros.state" id="state" /><br>

      <label for="sales_region">Região de comercializacao (nº): </label>
      <input type="text" v-model="filtros.sales_region" id="sales_region" /><br>

      <button type="submit">Buscar</button>
    </form>

    <h3>Resultados:</h3>
    <ul>
      {{ console.log("Operadores:", operadores) }}
      <li v-for="operador in operadores" v-bind:key="operador.Registro_ANS">
        <i>{{ JSON.stringify(operador, null, 2) }}</i>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      filtros: {
        corp_name: "",
        fantasy_name: "",
        city: "",
        modality: "",
      },
      operadores: {},
    };
  },
  methods: {
    async buscarOperadores() {
      try {
        const params = new URLSearchParams(this.filtros).toString();
        const response = await axios.get(`http://127.0.0.1:5000/search?${params}`, {
          responseType: 'json'
        });
        this.operadores = typeof response.data === "string" ? JSON.parse(response.data) : response.data;   
    
        console.log(this.operadores);
        console.log(response) 
      } catch (error) {
        console.error("Erro ao buscar operadores:", error);
      }
    },
  },
};
</script>