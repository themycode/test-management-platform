<template>
  <editor
    v-model="formatData"
    :lang="mode"
    :theme="theme"
    :options="options"
    :width="width"
    :height="height"
    @init="editorInit"
    @blur.native.capture="onEditorBlur"
    @paste.native="onPaste"
  />
</template>

<script>
export default {
  components: { editor: require("vue2-ace-editor") },
  data() {
    return {
      formatData: "",
      options: {
        highlightActiveLine: true, // 高亮当前行
        readOnly: this.readOnly, //编辑器只读--不能编辑内容//默认为false
        showPrintMargin: false, //去除编辑器里的竖线--打印边距
        enableLiveAutocompletion: true // 启用实时自动补全
      }
    };
  },
  props: {
    data: {
      type: String
    },
    readOnly: {
      type: Boolean,
      default() {
        return false;
      }
    },
    mode: {
      type: String,
      default() {
        return "text";
      }
    },
    modes: {
      type: Array,
      default() {
        return ["text", "json", "xml", "html"];
      }
    },
    theme: {
      type: String,
      default() {
        return "chrome";
      }
    },
    themes: {
      type: Array,
      default() {
        return ["chrome"];
      }
    },
    width: {
      type: String,
      default() {
        return "100%";
      }
    },
    height: {
      type: String,
      default() {
        return "100%";
      }
    }
  },
  mounted() {
    this.format();
  },
  watch: {
    formatData() {
      console.log(this.formatData);
      this.$emit("update:data", this.formatData);
    },
    mode() {
      this.format();
    }
  },
  methods: {
    editorInit: function(editor) {
      require("brace/ext/language_tools"); // 语言模式扩展的必要组件(language extension prerequsite...)
      require("brace/ext/searchbox"); // 支持Ctrl+F搜索、Ctrl+H替换

      this.modes.forEach(mode => {
        require("brace/mode/" + mode); //language
      });
      this.themes.forEach(theme => {
        require("brace/theme/" + theme); //language
      });
      require("brace/theme/chrome");
      require("brace/snippets/javascript"); //snippet //代码块
      //   if (this.readOnly) {
      //     editor.setReadOnly(true);
      //   }
    },
    format() {
      if (this.mode === "json") {
        try {
          this.formatData = JSON.stringify(JSON.parse(this.data), null, 2);
        } catch (e) {
          if (this.data) {
            this.formatData = this.data;
          }
        }
      } else {
        if (this.data) {
          this.formatData = this.data;
        }
      }
    },
    onEditorBlur() {
      this.format();
    },
    onPaste() {
      this.format();
    }
  }
};
</script>

<style scoped></style>
