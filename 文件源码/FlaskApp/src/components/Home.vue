<template>
  <div>
    <Card>
      <div>
       <Row>
         <Col :md="6" :xs="22">
         <Card :bordered="false" style="background:#F05050">
          <h3><Icon type="ribbon-b"></Icon>销售量</h3>
          <h4>{{result.cnt}}</h4>
         </Card>
         </Col>
         <Col :md="6" :xs="22">
         <Card :bordered="false" style="background:#7266ba">
          <h3><Icon type="social-yen"></Icon>销售额</h3>
          <h4>{{result.round}}</h4>
         </Card>
         </Col>
         <Col :md="6" :xs="22">
         <Card :bordered="false" style="background:#23b7e5">
            <h3><Icon type="ios-pricetag"></Icon>平均销售量</h3>
            <h4>{{Number(result.cnt)/91}}</h4>
         </Card>
         </Col>
         <Col :md="6" :xs="22">
          <Card :bordered="false" style="background:#27C24C;">
            <h3><Icon type="pie-graph"></Icon>平均销售额</h3>
            <h4>{{Number(result.round)/91}}</h4>
          </Card>
        </Col>
       </Row>
      </div>
    </Card>
    <Row>
      <Col span="12" id="select-type">
      <Dropdown @on-click="fuck" style="margin-left: 20px">
        <Button type="primary">选择属性<Icon type="arrow-down-b"></Icon></Button>
        <Dropdown-menu slot="list">
          <Dropdown-item name="cnt">销售量</Dropdown-item>
          <Dropdown-item name="round">销售额</Dropdown-item>
          <Dropdown-item name="outDegree">出度</Dropdown-item>
          <Dropdown-item name="inDegree">入度</Dropdown-item>
          <Dropdown-item name="pageRank">PageRank</Dropdown-item>
        </Dropdown-menu>
      </Dropdown>
      </Col>
    </Row>
    <Row>
      <Col span="24" id="select-type">
      <Card>
        <div id="myChart" :style="{height: '300px'}"></div>
      </Card>
      </Col>
    </Row>

    <Table :columns="columns1" :data="data1" ref=table></Table>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
    <Back-top></Back-top>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        value1: [],
        data: [{
          value: 'first',
          label: '1-31',
          children: [
            {
              value: 'gugong',
              label: '故宫'
            },
            {
              value: 'tiantan',
              label: '天坛'
            },
            {
              value: 'wangfujing',
              label: '王府井'
            }
          ]
        }, {
          value: 'second',
          label: '32-61',
          children: [
            {
              value: 'nanjing',
              label: '南京'
            },
            {
              value: 'suzhou',
              label: '苏州'
            }
          ]
        }, {
          value: 'third',
          label: '62-91',
          children: [
            {
              value: 'nanjing1',
              label: '南京'
            },
            {
              value: 'suzhou2',
              label: '苏州'
            }
          ]
        }],
        columns1: [
          {
            title: 'sale_nbr',
            key: 'sale_nbr'
          },
          {
            title: 'cnt',
            key: 'cnt',
            sortable: true
          },
          {
            title: 'round',
            key: 'round',
            sortable: true
          },
          {
            title: 'in_degree',
            key: 'in_degree',
            sortable: true
          },
          {
            title: 'out_degree',
            key: 'out_degree',
            sortable: true
          },
          {
            title: 'PageRank',
            key: 'PageRank',
            sortable: true
          },
          {
            title: '操作',
            key: 'edit',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.show(params.index)
                    }
                  }
                }, '查看'),
                h('Button', {
                  props: {
                    type: 'info',
                    size: 'small',
                    icon: 'stats-bars'
                  },
                  on: {
                    click: () => {
                      this.$router.push({name: 'saleShow', params: {id: `${this.data1[params.index].sale_nbr}`}})
                    }
                  }
                }, '详情')
              ])
            }
          }
        ],
        data1: [],
        result: []
      }
    },
    mounted () {
      this.drawLine('cnt')
      this.drawLines('cnt')
    },
    methods: {
      fuck (name) {
        this.drawLine(name)
        this.drawLines(name)
      },
      drawLine (type) {
        this.$http.get('/degree', {params: { 'type': type }}).then(response => {
          this.result = response.data
          this.data1 = []
          for (let i in this.result.sale_nbr) {
            let item = {
              sale_nbr: i,
              cnt: this.result.sale_nbr[i]['cnt'],
              round: this.result.sale_nbr[i]['round'],
              in_degree: this.result.sale_nbr[i]['in_degree'],
              out_degree: this.result.sale_nbr[i]['out_degree'],
              PageRank: this.result.sale_nbr[i]['page_rank']
            }
            this.data1.push(item)
          }
        })
      },
      drawLines (type) {
        this.$http.get('/sum', {params: { 'type': type }}).then(response => {
          let data = response.data
          // 基于准备好的dom，初始化echarts实例
          let myChart = this.$echarts.init(document.getElementById('myChart'))
          // 绘制图表
          myChart.setOption({
            title: { text: '机票市场走势图' },
            tooltip: { trigger: 'axis' },
            xAxis: {
              data: data.map(function (item) {
                return item[0]
              })
            },
            yAxis: {
              splitLine: {
                show: false
              }
            },
            toolbox: {
              left: 'center',
              feature: {
                dataZoom: {
                  yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
              }
            },
            dataZoom: [{
              startValue: '81'
            }, {
              type: 'inside'
            }],
            series: {
              name: type,
              type: 'line',
              data: data.map(function (item) {
                return item[1]
              })
            }
          })
        })
      },
      show (index) {
        this.$Modal.info({
          title: '代理人信息',
          content: `sale_nbr：${this.data1[index].sale_nbr}<br>cnt：${this.data1[index].cnt}<br>round：${this.data1[index].round}<br>in_degree：${this.data1[index].in_degree}<br>out_degree：${this.data1[index].out_degree}<br>page_rank：${this.data1[index].PageRank}`
        })
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: '原始数据'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: '排序和过滤后的数据',
            original: false
          })
        }
      }
    }
  }
</script>
<style scoped>
  #select-type {
    margin: 10px 0;
  }
  .ivu-card {
    border: none;
    border-radius:0;
  }
.ivu-card-body h3,.ivu-card-body h4 {
    color: #FFF
  }
</style>

