<template>
  <div>
    <Table :columns="columns" :data="data" ref="table"></Table>
    <div style="margin: 10px;overflow: hidden">
      <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
      <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
      <div style="float: right;">
        <Page :total="Number(total)" :current="1" @on-change="changePage"></Page>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        allData: [],    // 全部分页数据
        tableData: [],  // 表格数据
        columns: [
          {
            title: 'sale_nbr',
            key: 'sale_nbr'
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
            title: 'avg(in_degree/out_degree)',
            key: 'avg',
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
                  on: {
                    click: () => {
                      this.$router.push({name: 'degreeShow', params: {id: `${this.data[params.index].sale_nbr}`}})
                    }
                  }
                }, '详情')
              ])
            }
          }
        ],
        data: [],
        total: ''
      }
    },
    mounted () {
      this.statis('cnt')
    },
    methods: {
      fuck (name) {
        this.statis(name)
      },
      statis (type) {
        this.$http.get('/target', {params: { 'type': type }}).then(response => {
          let data = response.data
          console.log(data.sale_nbr.length)
          this.total = data.sale_nbr.length
          let tempData = []
          for (let i = 0; i < data.sale_nbr.length; i++) {
            let item = {
              sale_nbr: data.sale_nbr[i],
              in_degree: data.in_degree[i],
              out_degree: data.out_degree[i],
              avg: Number(data.in_degree[i] / data.out_degree[i]),
              page_rank: data.page_rank[i]
            }
            tempData.push(item)
            tempData.push(item)
            if (tempData.length === 10) {
              this.allData.push(tempData)
              tempData = []
            }
          }
          // let group = window._.chunk(tempData, 10)
          // for (let i = 0; i < 10; i++) {
          //   this.allData.push(group)
          // }
          this.data = this.allData[0]
        })
      },
      changePage (event) {
        if (this.allData.length >= event) {
          this.data = this.allData[event - 1]
        }
        console.log('当前页码' + event)
        // 这里直接更改了模拟的数据，真实使用场景应该从服务端获取数据
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
          title: '代理人信息',
          content: `sale_nbr：${this.data[index].sale_nbr}<br>cnt：${this.data[index].cnt}<br>round：${this.data[index].round}<br>in_degree：${this.data[index].in_degree}<br>out_degree：${this.data[index].out_degree}<br>page_rank：${this.data[index].page_rank}`
        })
      }
    }
  }
</script>