<template>
<div>
  <Upload :show-upload-list="true" :on-success="handleSuccess" :on-error="handleError" multiple type="drag" action="http://10.0.0.1:5000/api/upload">
    <div style="padding: 20px 0">
      <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
      <p>点击或将文件拖拽到这里上传</p>
    </div>
  </Upload>
<Button type="primary" size="small" :loading="loading1" @click="submit1()">清洗数据</Button>
<!-- <Button type="primary" size="small" :loading="loading2" @click="submit2()">计算地位</Button>
<Button type="primary" size="small" :loading="loading3" @click="submit3()">返回文件</Button> -->
</div>
</template>
<script>
export default {
  data () {
    return {
      fileName: '',
      loading1: false,
      fileData: []
    }
  },
  methods: {
    handleSuccess (response, file, fileList) {
      this.fileName = file.name
      this.$Notice.open({
        title: '上传文件成功',
        desc: ''
      })
    },
    handleError () {
      this.$Notice.open({
        title: '无法上传文件',
        desc: ''
      })
    },
    submit1 () {
      this.loading1 = true
      console.log(this.fileName)
      if (this.fileName === '') {
        this.$Modal.error({
          title: '地位文件计算生成',
          content: `请先选择上传文件`
        })
        return
      } else {
        this.$http.get('/item/' + this.fileName).then(response => {
          this.fileData = response.data
          if (this.fileData.boolean) {
            this.$Modal.success({
              title: '地位文件计算生成',
              content: `生成地位文件${this.fileData.fileName}<br>
                        请联系管理员配置使用`
            })
            this.loading1 = false
            return
          } else {
            setTimeout(() => {
              this.loading1 = false
            }, 30000)
          }
        })
      }
    }
  }
}
</script>
