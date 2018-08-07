<template>
  <div>
    <Row class="upload">
      <Upload :action="uploadUrl" :before-upload="handleUpload" :on-success="handleSuccess">
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
      loading: false
    }
  },
  methods: {
    handleUpload: function (file) {
      console.log(file)
      this.filename = this.getDateString() + file.name
    },
    handleSuccess: function (res, file, fileList) {
      this.filename = res
      // this.filename = this.getDateString()
    },
    handleRun: function () {
      this.loading = true
      let delay = Math.random(0, 4)
      let _this = this
      setTimeout(function () {
        _this.loading = false
        _this.downloadLink = `/api/file-download?filename=${this.filename}`
      }, delay * 1000)
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
