<template>

  <div id='Chart'>
    <b-alert show variant="info">Info Alert</b-alert>
    <apexchart type="line" height="350" :options="chartOptions" :series="pres"></apexchart>
    <apexchart type="line" height="350" :options="chartOptions" :series="temp"></apexchart>
    <apexchart type="line" height="350" :options="chartOptions" :series="humi"></apexchart>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'Chart',
  components:{
    apexcharts : VueApexCharts,

  },
  created(){
    this.$socket.on("temp",(data)=>{
      this.temp = [{ name: "temp", data}];
     
    });
    this.$socket.on("humi",(data)=>{
   
      this.humi = [{ name: "humi", data}];
    });
    this.$socket.on("pres",(data)=>{
   
      this.pres = [{ name: "pres", data}];
    });
  },
  data: function () {
    return {
          chartOptions: {
        chart: { height: 350,
        width: 300,
              type: 'line',
              zoom: {
                enabled: false
              } },
      },
          series: [],
          temp:[],
          humi:[]
          }
          
          
        }
  }
  

</script>
