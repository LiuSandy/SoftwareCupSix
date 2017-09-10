webpackJsonp([0],{480:function(t,e,a){function r(t){a(501)}var n=a(165)(a(489),a(509),r,"data-v-98256d0c",null);t.exports=n.exports},489:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){var t=this;return{loading:!1,total:91,allData:[],tableData:[],columns:[{title:"day_id",key:"day_id",sortable:!0},{title:"cnt",key:"cnt",sortable:!0},{title:"round",key:"round",sortable:!0},{title:"in_degree",key:"in_degree",sortable:!0},{title:"out_degree",key:"out_degree",sortable:!0},{title:"page_rank",key:"page_rank",sortable:!0},{title:"操作",key:"action",aligen:"center",width:150,render:function(e,a){return e("div",[e("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){t.show(a.index)}}},"查看")])}}],data:[],result:[]}},mounted:function(){var t=this.$route.fullPath,e=String(t).split("/"),a=e[e.length-1];this.drawLine(a)},methods:{drawLine:function(t){var e=this;this.$http.get("/detail",{params:{type:t}}).then(function(t){e.result=t.data;var a=t.data;e.$echarts.init(document.getElementById("myChart")).setOption({tooltip:{trigger:"axis",axisPointer:{type:"shadow",label:{show:!0}}},toolbox:{show:!0,x:"center",y:"top",feature:{mark:{show:!0},dataView:{show:!0,readOnly:!1},magicType:{show:!0,type:["line","bar"]},restore:{show:!0},saveAsImage:{show:!0}}},calculable:!0,legend:{data:["Growth","销售量","销售额"],itemGap:5},grid:{top:"12%",left:"1%",right:"10%",containLabel:!0},xAxis:[{type:"category",data:a.day_id}],yAxis:[{type:"value",name:"销售额"},{type:"value",name:"销售量"}],dataZoom:[{show:!0,start:81,end:100},{type:"inside",start:81,end:100},{show:!0,yAxisIndex:0,filterMode:"empty",width:30,height:"80%",showDataShadow:!1,left:"93%"}],series:[{name:"销售量",type:"bar",yAxisIndex:1,data:a.cnt},{name:"销售额",type:"bar",data:a.round}]}),e.$echarts.init(document.getElementById("secondChart")).setOption({title:{text:"销售关系图"},tooltip:{trigger:"axis"},legend:{data:["销售量(cnt)","销售额(round)"]},grid:{left:"3%",right:"4%",bottom:"3%",containLabel:!0},toolbox:{feature:{saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:a.day_id},yAxis:[{type:"value",name:"销售量(cnt)"},{type:"value",name:"销售额(round)"}],dataZoom:[{startValue:81},{type:"inside"}],series:[{name:"销售量(cnt)",type:"line",stack:"总量",data:a.cnt},{name:"销售额(round)",type:"line",stack:"总量",yAxisIndex:1,data:a.round}]});var r=[];a.day_id.map(function(t){var e={day_id:t,cnt:a.cnt[Number(t-1)],round:a.round[Number(t-1)],in_degree:a.in_degree[Number(t-1)],out_degree:a.out_degree[Number(t-1)],page_rank:a.page_rank[Number(t-1)]};r.push(e)});for(var n=window._.chunk(r,10),o=0;o<n.length;o++)e.allData.push(n[o]);e.data=e.allData[0]})},changePage:function(t){this.allData.length>=t&&(this.data=this.allData[t-1]),console.log("当前页码"+t)},exportData:function(t){console.log(t),1===t?this.$refs.table.exportCsv({filename:"原始数据"}):2===t&&this.$refs.table.exportCsv({filename:"排序和过滤后的数据",original:!1})},show:function(t){this.$Modal.info({title:"详细信息",content:"day_id:"+this.data[t].day_id+"<br>cnt："+this.data[t].cnt+"<br>round："+this.data[t].round+"<br>in_degree："+this.data[t].in_degree+"<br>out_degree："+this.data[t].out_degree+"<br>page_rank："+this.data[t].page_rank})}}}},495:function(t,e,a){e=t.exports=a(469)(!0),e.push([t.i,"#select-type[data-v-98256d0c]{margin:10px 0}","",{version:3,sources:["C:/Users/Administrator/Desktop/FlaskApp/src/components/sale/Show.vue"],names:[],mappings:"AACA,8BACE,aAAe,CAChB",file:"Show.vue",sourcesContent:["\n#select-type[data-v-98256d0c] {\n  margin: 10px 0;\n}\n"],sourceRoot:""}])},501:function(t,e,a){var r=a(495);"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);a(470)("6b773cf3",r,!0)},509:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("Card",[a("div",[a("Row",[a("Col",{attrs:{span:"4",offset:"1"}},[a("Card",{staticStyle:{background:"#F05050"},attrs:{bordered:!1}},[a("h3",[a("Icon",{attrs:{type:"ribbon-b"}}),t._v("销售量")],1),t._v(" "),a("h4",[t._v(t._s(t.result.cntSum))])])],1),t._v(" "),a("Col",{attrs:{span:"4",offset:"2"}},[a("Card",{staticStyle:{background:"#7266ba"},attrs:{bordered:!1}},[a("h3",[a("Icon",{attrs:{type:"social-yen"}}),t._v("销售额")],1),t._v(" "),a("h4",[t._v(t._s(t.result.roundSum))])])],1),t._v(" "),a("Col",{attrs:{span:"4",offset:"2"}},[a("Card",{staticStyle:{background:"#23b7e5"},attrs:{bordered:!1}},[a("h3",[a("Icon",{attrs:{type:"ios-pricetag"}}),t._v("平均销售量")],1),t._v(" "),a("h4",[t._v(t._s(t.result.cntAvg))])])],1),t._v(" "),a("Col",{attrs:{span:"4",offset:"2"}},[a("Card",{staticStyle:{background:"#27C24C"},attrs:{bordered:!1}},[a("h3",[a("Icon",{attrs:{type:"pie-graph"}}),t._v("平均销售额")],1),t._v(" "),a("h4",[t._v(t._s(t.result.roundAvg))])])],1)],1)],1)]),t._v(" "),a("br"),t._v(" "),a("Card",[a("div",{style:{height:"300px"},attrs:{id:"myChart"}})]),t._v(" "),a("br"),t._v(" "),a("Card",[a("div",{style:{height:"300px"},attrs:{id:"secondChart"}})]),t._v(" "),a("br"),t._v(" "),a("Card",[a("Table",{ref:"table",attrs:{columns:t.columns,data:t.data,stripe:"",loading:t.loading}}),t._v(" "),a("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[a("Button",{attrs:{type:"primary",size:"large"},on:{click:function(e){t.exportData(1)}}},[a("Icon",{attrs:{type:"ios-download-outline"}}),t._v(" 导出原始数据")],1),t._v(" "),a("Button",{attrs:{type:"primary",size:"large"},on:{click:function(e){t.exportData(2)}}},[a("Icon",{attrs:{type:"ios-download-outline"}}),t._v(" 导出排序和过滤后的数据")],1),t._v(" "),a("div",{staticStyle:{float:"right"}},[a("Page",{attrs:{total:t.total,current:1},on:{"on-change":t.changePage}})],1)],1)],1),t._v(" "),a("Back-top")],1)},staticRenderFns:[]}}});
//# sourceMappingURL=0.aba89c1f21660cd4a45f.js.map