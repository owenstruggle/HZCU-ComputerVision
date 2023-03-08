<template>
  <div>
    <el-row style="margin-top: 20px;">
      <el-col :span="12" :offset="4">
        <el-form :model="formData" ref="formData" label-width="110px" class="demo-formData">
          <el-form-item label="选择文件">
            <el-upload class="file-uploader" multiple :auto-upload="false" :on-change="onUploadChange" action=""
                       :show-file-list="false" accept=".jpeg,.png,.jpg">
              <el-button type="primary">选择文件</el-button>
            </el-upload>
          </el-form-item>

          <el-form-item v-if="isUpload" label="原始图片">
            <el-image :src="dialogImageUrl"></el-image>
          </el-form-item>

          <el-form-item v-if="isUpload" label="操作">
            <template>
              <el-button type="primary" @click="handleGrayscaleReversal">灰度反转</el-button>
              <el-button type="primary" @click="handleHistogram">直方图</el-button>
              <el-button type="primary" @click="handleHistogramEqualization">直方图均衡化</el-button>
              <el-button type="primary" @click="inputSegmentedLinearTransformation = true">分段线性变换</el-button>
              <el-button type="primary" @click="inputLogarithmicTransformation = true">对数变换</el-button>
              <el-button type="primary" @click="inputGammaTransformation = true">伽马变换</el-button>
            </template>
          </el-form-item>
          <el-form-item v-if="isHandle" label="处理结果">
            <el-image :src="handleDialogImageUrl" style="width: 100%"></el-image>
          </el-form-item>

        </el-form>
      </el-col>
    </el-row>

    <div>
      <el-dialog title="参数" :visible.sync="inputSegmentedLinearTransformation" width="300px">
        <el-form :model="params">
          <el-form-item label="r1" label-width="30px">
            <el-input v-model="params.r1" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="s1" label-width="30px">
            <el-input v-model="params.s1" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="r2" label-width="30px">
            <el-input v-model="params.r2" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="s2" label-width="30px">
            <el-input v-model="params.s2" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="inputSegmentedLinearTransformation = false">取 消</el-button>
          <el-button type="primary" @click="handleSegmentedLinearTransformation">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="参数" :visible.sync="inputLogarithmicTransformation" width="300px">
        <el-form :model="params">
          <el-form-item label="c" label-width="30px">
            <el-input v-model="params.c" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="inputLogarithmicTransformation = false">取 消</el-button>
          <el-button type="primary" @click="handleLogarithmicTransformation">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="参数" :visible.sync="inputGammaTransformation" width="300px">
        <el-form :model="params">
          <el-form-item label="c" label-width="30px">
            <el-input v-model="params.c" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="v" label-width="30px">
            <el-input v-model="params.v" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="inputGammaTransformation = false">取 消</el-button>
          <el-button type="primary" @click="handleGammaTransformation">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import {
  gammaTransformation,
  grayscaleReversal,
  histogram,
  histogramEqualization,
  logarithmicTransformation,
  segmentedLinearTransformation
} from "@/api/getData";

export default {
  name: 'App',
  data() {
    return {
      formData: {},
      fileInfoList: {},
      params: {
        r1: 0,
        r2: 0,
        s1: 0,
        s2: 0,
        c: 0,
        v: 0
      },
      dialogImageUrl: "",
      handleDialogImageUrl: "",
      isUpload: false,
      isHandle: false,
      inputSegmentedLinearTransformation: false,
      inputLogarithmicTransformation: false,
      inputGammaTransformation: false
    }
  },
  methods: {
    async onUploadChange(file) {
      // console.log("file", file)
      this.isHandle = false
      this.isUpload = true
      this.dialogImageUrl = URL.createObjectURL(file.raw)

      this.fileInfoList = ({
        file_name: file.name,
        raw: file.raw
      })
    },
    async handleGrayscaleReversal() {
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await grayscaleReversal({base64: base64})
      this.base64toFile(res.base64)
    },
    async handleHistogram() {
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await histogram({base64: base64})
      this.base64toFile(res.base64)
    },
    async handleHistogramEqualization() {
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await histogramEqualization({base64: base64,})
      this.base64toFile(res.base64)
    },
    async handleSegmentedLinearTransformation() {
      this.inputSegmentedLinearTransformation = false
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await segmentedLinearTransformation({
        base64: base64,
        r1: this.params.r1,
        r2: this.params.r2,
        s1: this.params.s1,
        s2: this.params.s2
      })
      this.base64toFile(res.base64)
    },
    async handleLogarithmicTransformation() {
      this.inputLogarithmicTransformation = false
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await logarithmicTransformation({base64: base64, c: this.params.c})
      this.base64toFile(res.base64)
    },
    async handleGammaTransformation() {
      this.inputGammaTransformation = false
      this.isHandle = false
      const base64 = await this.getBase64(this.fileInfoList.raw)
      const res = await gammaTransformation({base64: base64, c: this.params.c, v: this.params.v})
      this.base64toFile(res.base64)
    },
    async getBase64(file) {
      const res = await new Promise(function (resolve, reject) {
        const reader = new FileReader()
        let imgResult = ''
        reader.readAsDataURL(file)
        reader.onload = function () {
          imgResult = reader.result
        }
        reader.onerror = function (error) {
          reject(error)
        }
        reader.onloadend = function () {
          resolve(imgResult)
        }
      })
      const params = res.split(',')
      // console.log('params', params[1])
      if (params.length > 0) {
        return params[1]
      }
      return null
    },
    base64toFile(arr) {
      const bstr = atob(arr);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      let file = new File([u8arr], this.fileInfoList.file_name);
      console.log(file)
      this.handleDialogImageUrl = window.webkitURL.createObjectURL(file)
      this.isHandle = true
    },
  }
}
</script>

<style>
</style>
