<template>
  <div>
    <Row class="upload">
      <Upload :action="uploadUrl" :format="accpetExt" :on-format-error="handleFormatError" :before-upload="handleUpload" :on-success="handleSuccess">
        <Button icon="ios-cloud-upload-outline">上传数据</Button>
      </Upload>
    </Row>
    <Row class="run">
      <Button @click="handleRun" type="primary" :loading="loading" icon="ios-power">
        <span v-if="!loading">运行算法</span>
        <span v-else>运行中</span>
      </Button>
    </Row>
    <Row>
      <a v-if="downloadLink != ''" :href="downloadLink" download="result">下载结果</a>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      uploadUrl: '/api/file-upload',
      downloadLink: '',
      filename: '',
      loading: false,
      accpetExt: ['zip']
    }
  },
  methods: {
    handleUpload: function (file) {
      console.log(file)
      this.filename = this.getDateString() + file.name
    },
    handleSuccess: function (res, file, fileList) {
      this.filename = res
    },
    handleFormatError: function (file, fileList) {
      let filename = file.name
      let filenameSplit = filename.split('.')
      let ext = filenameSplit[filenameSplit.length - 1]
      this.$Notice.error({
        title: '不支持的文件格式 .' + ext,
        desc: '目前支持的文件格式为.zip'
      })
    },
    handleRun: function () {
      if (this.filename === '') {
        this.$Notice.error({
          title: '无法运行',
          desc: '请先上传数据集'
        })
        return
      }
      this.loading = true
      // this.filename = this.getDateString()
      let url = `/api/run?filename=${this.filename}`
      let _this = this
      this.$http.get(url).then(function (res) {
        console.log(res)
        if (res.status === 200 && res.data === 'ok') {
          _this.downloadLink = `/api/file-download?filename=${_this.filename}`
          _this.$Notice.success({
            title: '运行成功',
            desc: '点击下方"下载结果"链接可以下载运行结果表格'
          })
        } else {
          _this.$Notice.error({
            title: '运行出错',
            desc: res.status + ' 运行算法出错，请重试'
          })
        }
        _this.loading = false
      })
    },
    handleDownload: function () {
    },
    getDateString: function () {
      let date = new Date()
      let seperator1 = '-'
      let seperator2 = ':'
      let year = date.getFullYear()
      let month = date.getMonth() + 1
      let strDate = date.getDate()
      let hour = date.getHours()
      let minute = date.getMinutes()
      let second = date.getSeconds()
      if (month >= 1 && month <= 9) {
        month = '0' + month
      }
      if (strDate >= 0 && strDate <= 9) {
        strDate = '0' + strDate
      }
      let currentdate = year + seperator1 + month + seperator1 + strDate + ' ' + hour + seperator2 + minute + seperator2 + second + '_'
      return currentdate
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.upload {
  padding: 10px 20% 10px 20%;
  border-bottom: 1px solid #eee;
  margin-bottom: 15px;
}

.run {
  padding: 0 0 15px 0;
}
</style>
