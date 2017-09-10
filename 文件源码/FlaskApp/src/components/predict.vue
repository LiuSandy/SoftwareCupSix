<template>
  <div class="body">
    <Form :model="formItem" :label-width="80">
      <Form-item label="代理人代码">
        <Input v-model="formItem.input" placeholder="请输入"></Input>
      </Form-item>
      <Form-item label="day_id">
        <!-- formItem.select -->
        <Cascader :data="cascader" v-model="formItem.select" placeholder="请选择"></Cascader>
      </Form-item>
      <Form-item>
        <Button type="primary" :loading="loading" @click="submit()">提交</Button>
        <Button type="ghost" style="margin-left: 8px">取消</Button>
      </Form-item>
    </Form>
    <br>
    <Card id="show" v-if="showEchart">
      <div id="myChart" :style="{ height: '300px'}"></div>
    </Card>
    <br>
    <Table :columns="columns1" :data="data1" ref="table"></Table>
    <div style="margin: 10px;overflow: hidden">
      <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
      <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
      <div style="float: right;">
        <Page :total="Number(total)" :current="1" @on-change="changePage"></Page>
      </div>
    </div>
    <br>
    <BackTop></BackTop>
  </div>
</template>
<script>
export default {
  data () {
    return {
      loading: false,
      cascader: [{
        value: 'first',
        label: '1-30',
        children: []
      }],
      formItem: {
        input: '',
        select: []
      },
      columns1: [
        {
          title: 'day_id',
          key: 'day_id'
        },
        {
          title: 'cnt',
          key: 'cnt'
        },
        {
          title: 'round',
          key: 'round'
        },
        {
          title: 'in_degree',
          key: 'in_degree'
        },
        {
          title: 'out_degree',
          key: 'out_degree'
        },
        {
          title: 'page_rank',
          key: 'page_rank'
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
          align: 'center',
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
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'saleShow', params: {id: `${this.saleNbr}`}})
                  }
                }
              }, '详情')
            ])
          }
        }
      ],
      data1: [],
      allData: [],
      total: '',
      saleNbr: '',
      dayId: '',
      showEchart: false
    }
  },

  mounted () {
    let n = 1
    this.cascader.forEach((item) => {
      let i = 1
      let max = 31
      if (n === 1) {
        i = 1
        max = 30
      }
      for (i; i <= max; i++) {
        let save = {
          value: i,
          label: i
        }
        item.children.push(save)
      }
      n++
    })
  },
  methods: {
    submit () {
      let saleNbr = this.formItem.input
      if (saleNbr === '') {
        this.$Message.error('请输入代理人代码')
        this.showEchart = false
        this.loading = false
        return
      }
      this.saleNbr = saleNbr
      let dayId = this.formItem.select[1]
      if (dayId === undefined && saleNbr !== '') {
        dayId = 'all'
        this.showEchart = true
      }
      this.loading = true
      this.$http.get('/prdt/' + saleNbr + '/' + dayId).then(response => {
        let data = response.data
        this.total = data.length
        let tempData = []
        for (let i = 0; i < data.length; i++) {
          let item = {
            day_id: data[i].day_id,
            cnt: data[i].cnt.split(',')[0].substring(1),
            round: data[i].round.split(',')[0].substring(1),
            in_degree: data[i].in_degree.split(',')[0].substring(1),
            out_degree: data[i].out_degree.split(',')[0].substring(1),
            page_rank: data[i].page_rank.split(',')[0].substring(1)
          }
          tempData.push(item)
        }
        let group = window._.chunk(tempData, 10)
        for (let i = 0; i < group.length; i++) {
          this.allData.push(group[i])
        }
        this.data1 = this.allData[0]
        let dayList = []
        let cntList = []
        let roundList = []
        let indegreeList = []
        let outdegreeList = []
        let pagerankList = []
        for (let i = 0; i < data.length; i++) {
          dayList.push(i + 1)
          cntList.push(data[i].cnt.split(',')[0].substring(1))
          roundList.push(data[i].round.split(',')[0].substring(1))
          indegreeList.push(data[i].in_degree.split(',')[0].substring(1))
          outdegreeList.push(data[i].out_degree.split(',')[0].substring(1))
          pagerankList.push(data[i].page_rank.split(',')[0].substring(1))
        }
        this.$nextTick(() => {
          let myChart = this.$echarts.init(document.getElementById('myChart'))
          myChart.setOption({
            title: {
              text: ''
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['cnt', 'round', 'in_degree', 'out_degree', 'page_rank']
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            toolbox: {
              feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
              }
            },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              data: dayList
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: 'cnt',
                type: 'line',
                stack: '总量',
                data: cntList
              },
              {
                name: 'round',
                type: 'line',
                stack: '总量',
                data: roundList
              },
              {
                name: 'in_degree',
                type: 'line',
                stack: '总量',
                data: indegreeList
              },
              {
                name: 'out_degree',
                type: 'line',
                stack: '总量',
                data: outdegreeList
              },
              {
                name: 'page_rank',
                type: 'line',
                stack: '总量',
                data: pagerankList
              }
            ]
          })
        })
        this.loading = false
      }, () => {
        this.loading = false
      })
    },
    exportData (type) {
      console.log(type)
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
    },
    changePage (event) {
      if (this.allData.length >= event) {
        this.data1 = this.allData[event - 1]
      }
    },
    show (index) {
      this.$Modal.info({
        title: '销售信息',
        content: `day_id：${this.data1[index].day_id}<br>
                  cnt：${this.data1[index].cnt}<br>
                  round：${this.data1[index].round}<br>
                  in_degree：${this.data1[index].in_degree}<br>
                  out_degree：${this.data1[index].out_degree}<br>
                  page_rank：${this.data1[index].page_rank}`
      })
    }
  }
}
</script>

<style scoped>
.body{
  min-height: 500px;
}
#select-type {
  margin: 10px 0;
}
</style>
