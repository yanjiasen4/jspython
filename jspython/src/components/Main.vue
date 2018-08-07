<template>
  <div>
    <Row class="upload">
      <Upload action="/api/file-upload" :before-upload="handleUpload">
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
      filename: '',
      downloadLink: '',
      loading: false
    }
  },
  methods: {
    handleUpload: function (file) {
      this.filename = file
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
