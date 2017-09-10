<template>
  <div>
    <Button type="primary" icon="arrow-return-left" @click="back">返回销售关系</Button>
    <br>
    <Card>
      <div>
        <Row>
          <Col :md="6" :xs="22">
          <Card :bordered="false" style="background:#F05050">
            <h3><Icon type="ribbon-b"></Icon>销售量</h3>
            <h4>{{result.cntSum}}</h4>
          </Card>
          </Col>
          <Col :md="6" :xs="22">
         <Card :bordered="false" style="background:#7266ba">
          <h3><Icon type="social-yen"></Icon>销售额</h3>
          <h4>{{result.roundSum}}</h4>
         </Card>
         </Col>
         <Col :md="6" :xs="22">
         <Card :bordered="false" style="background:#23b7e5">
            <h3><Icon type="ios-pricetag"></Icon>平均销售量</h3>
            <h4>{{result.cntAvg}}</h4>
         </Card>
         </Col>
         <Col :md="6" :xs="22">
          <Card :bordered="false" style="background:#27C24C">
            <h3><Icon type="pie-graph"></Icon>平均销售额</h3>
            <h4>{{result.roundAvg}}</h4>
          </Card>
        </Col>
        </Row>
      </div>
    </Card>
    <br>
    <Card>
    <div id="myChart" :style="{ height: '300px'}"></div>
    </Card>
    <br>
    <!-- 折线图 -->
    <Card>
    <div id="secondChart" :style="{height: '300px'}"></div>
    </Card>
    <br>
    <!-- 表格显示 -->
    <Card>
      <Table :columns="columns" :data="data" stripe ref="table" :loading="loading"></Table>
      <div style="margin: 10px;overflow: hidden">
        <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
        <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
        <div style="float: right;">
          <Page :total="total" :current="1" @on-change="changePage"></Page>
        </div>
      </div>
    </Card>
    <Back-top></Back-top>
  </div>
</template>
<script>
    export default {
      data () {
        return {
          loading: false,
          total: 91,
          allData: [],    // 全部分页数据
          tableData: [],  // 表格数据
          columns: [
            {
              title: 'day_id',
              key: 'day_id',
              sortable: true
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
              title: 'page_rank',
              key: 'page_rank',
              sortable: true
            },
            {
              title: '操作',
              key: 'action',
              aligen: 'center',
              width: 150,
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
                  }, '查看')
                ])
              }
            }
          ],
          data: [],
          result: []
        }
      },
      mounted () {
        let cans = this.$route.fullPath
        let spstr = String(cans).split('/')
        let type = spstr[spstr.length - 1]
        this.drawLine(type)
      },
      methods: {
        back () {
          this.$router.push({name: 'degreeShow', params: {id: this.$route.params.id}})
        },
        drawLine (type) {
          this.$http.get('/detail', {params: { 'type': type }}).then(response => {
            this.result = response.data
            let data = response.data
            let myChart = this.$echarts.init(document.getElementById('myChart'))
            // 基于准备好的dom，初始化echarts实例
            myChart.setOption({
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'shadow',
                  label: {
                    show: true
                  }
                }
              },
              toolbox: {
                show: true,
                x: 'right',
                y: 'top',
                feature: {
                  mark: {show: true},
                  dataView: {show: true, readOnly: false},
                  magicType: {show: true, type: ['line', 'bar']},
                  restore: {show: true},
                  saveAsImage: {show: true}
                }
              },
              calculable: true,
              legend: {
                data: ['Growth', '销售量', '销售额'],
                itemGap: 5
              },
              grid: {
                top: '12%',
                left: '1%',
                right: '10%',
                containLabel: true
              },
              xAxis: [
                {
                  type: 'category',
                  data: data.day_id
                }
              ],
              yAxis: [
                {
                  type: 'value',
                  name: '销售额'
                },
                {
                  type: 'value',
                  name: '销售量'
                }
              ],
              dataZoom: [
                {
                  show: true,
                  start: 81,
                  end: 100
                },
                {
                  type: 'inside',
                  start: 81,
                  end: 100
                },
                {
                  show: true,
                  yAxisIndex: 0,
                  filterMode: 'empty',
                  width: 30,
                  height: '80%',
                  showDataShadow: false,
                  left: '93%'
                }
              ],
              series: [
                {
                  name: '销售量',
                  type: 'bar',
                  yAxisIndex: 1,
                  data: data.cnt
                },
                {
                  name: '销售额',
                  type: 'bar',
                  data: data.round
                }
              ]
            })
            let secondChart = this.$echarts.init(document.getElementById('secondChart'))
            secondChart.setOption({
              title: {
                text: '销售关系图'
              },
              tooltip: {
                trigger: 'axis'
              },
              legend: {
                data: ['销售量(cnt)', '销售额(round)']
              },
              grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
              },
              toolbox: {
                feature: {
                  saveAsImage: {}
                }
              },
              xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.day_id
              },
              yAxis: [
                {
                  type: 'value',
                  name: '销售量(cnt)'
                },
                {
                  type: 'value',
                  name: '销售额(round)'
                }
              ],
              dataZoom: [{
                startValue: 81
              }, {
                type: 'inside'
              }],
              series: [
                {
                  name: '销售量(cnt)',
                  type: 'line',
                  stack: '总量',
                  data: data.cnt
                },
                {
                  name: '销售额(round)',
                  type: 'line',
                  stack: '总量',
                  yAxisIndex: 1,
                  data: data.round
                }
              ]
            })
            let tempData = []
            data.day_id.map(i => {
              let item = {
                day_id: i,
                cnt: data.cnt[Number(i - 1)],
                round: data.round[Number(i - 1)],
                in_degree: data.in_degree[Number(i - 1)],
                out_degree: data.out_degree[Number(i - 1)],
                page_rank: data.page_rank[Number(i - 1)]
              }
              tempData.push(item)
            })
            let group = window._.chunk(tempData, 10)
            for (let i = 0; i < group.length; i++) {
              this.allData.push(group[i])
            }
            this.data = this.allData[0]
          })
        },
        changePage (event) {
          if (this.allData.length >= event) {
            this.data = this.allData[event - 1]
          }
          console.log('当前页码' + event)
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
        show (index) {
          this.$Modal.info({
            title: '详细信息',
            content: `day_id:${this.data[index].day_id}<br>cnt：${this.data[index].cnt}<br>round：${this.data[index].round}<br>in_degree：${this.data[index].in_degree}<br>out_degree：${this.data[index].out_degree}<br>page_rank：${this.data[index].page_rank}`
          })
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
