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
        <Button type="primary" @click="submit(formItem)">提交</Button>
        <Button type="ghost" style="margin-left: 8px">取消</Button>
      </Form-item>
    </Form>
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
    
  </div>
</template>
<script>
export default {
  data () {
    return {
      cascader: [{
        value: 'first',
        label: '1-31',
        children: []
      }, {
        value: 'second',
        label: '32-61',
        children: []
      }, {
        value: 'third',
        label: '62-91',
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
          title: 'sale_nbr',
          key: 'sale_nbr'
        },
        {
          title: 'buy_nbr',
          key: 'buy_nbr'
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
              }, '查看')
            ])
          }
        }
      ],
      data1: [],
      allData: [],
      total: ''
    }
  },

  mounted () {
    let n = 1
    this.cascader.forEach((item) => {
      let i = 1
      let max = 31
      if (n === 1) {
        i = 1
        max = 31
      }
      if (n === 2) {
        i = 32
        max = 61
      }
      if (n === 3) {
        i = 62
        max = 91
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
    submit: function (event) {
      let saleNbr = event.input
      let dayId = event.select[1]
      console.log(saleNbr)
      console.log(dayId)
      this.$http.get('/search/' + saleNbr + '/' + dayId).then(response => {
        let data = response.data
        if (data.day_id.length === 0) {
          this.$Modal.error({
            content: '没有与之相关的交易记录'
          })
        }
        this.total = data.day_id.length
        this.allData = []
        let tempData = []
        for (let i = 0; i < data.day_id.length; i++) {
          let item = {
            day_id: data.day_id[i],
            sale_nbr: data.sale_nbr[i],
            buy_nbr: data.buy_nbr[i],
            cnt: data.cnt[i],
            round: data.round[i]
          }
          tempData.push(item)
        }
        let group = window._.chunk(tempData, 10)
        for (let i = 0; i < group.length; i++) {
          this.allData.push(group[i])
        }
        this.data1 = this.allData[0]
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
      console.log('当前页码' + event)
      // 这里直接更改了模拟的数据，真实使用场景应该从服务端获取数据
    },
    show (index) {
      this.$Modal.info({
        title: '销售信息',
        content: `day_id：${this.data1[index].day_id}<br>sale_nbr：${this.data1[index].sale_nbr}<br>buy_nbr：${this.data1[index].buy_nbr}<br>cnt：${this.data1[index].cnt}<br>round：${this.data1[index].round}`
      })
    }
  }
}
</script>

<style scoped>
.body{
  min-height: 500px;
}
</style>
