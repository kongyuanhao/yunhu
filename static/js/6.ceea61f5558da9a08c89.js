webpackJsonp([6],{"A7+X":function(t,a,n){"use strict";function e(t){n("yLj1")}Object.defineProperty(a,"__esModule",{value:!0});var i=n("X0Oa"),o=n("qXfr"),l=n("5lJd"),s=n("sfEt"),c=n("UHn/"),d=n("InD7"),r=n("xwk4"),p=n("vwcn"),u=n("TpY+"),m={mixins:[r.a,u.a],data:function(){return{groupColor:"#50b97b",name:null,tel:null,identity:null,zhima_score:null,wechat:null,address:null,idcard_pic:"",idcard_backpic:"",idcard_people_pic:"",type:0}},components:{XInput:i.a,Group:o.a,XButton:l.a,Box:s.a,Flexbox:c.a,FlexboxItem:d.a,UploadImg:p.a},computed:{},methods:{changeImg:function(t,a){"undefined"!==a&&(this[a]=t,this.$vux.toast.show({text:"上传成功",time:500}))},submit:function(){var t=this;this.formMixin_submit("/update_base_info/").then(function(){var a=t;t.$vux.toast.show({text:"提交成功",time:500,onHide:function(){a.routerLink("ApplySupplementInfo",{},{checkway:a.$route.query.checkway})}})}).catch(function(t){console.log("code:"+t.code+" \n msg:"+t.msg)})},checkInfo:function(){var t=this;this.$axios.post({url:"/check_base_info/",data:{customer_id:parseInt(localStorage.getItem("yunhu!customer_id"))}}).then(function(a){t.name=a.name,t.tel=a.tel,t.identity=a.identity,t.zhima_score=a.zhima_score,t.wechat=a.wechat,t.address=a.address,t.idcard_pic=a.idcard_pic,t.idcard_backpic=a.idcard_backpic,t.idcard_people_pic=a.idcard_people_pic})}},created:function(){this.checkInfo()},mounted:function(){}},A=function(){var t=this,a=t.$createElement,n=t._self._c||a;return n("div",{staticClass:"demonUI ApplyForLoan"},[n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 姓名","title-color":t.groupColor}},[n("x-input",{ref:"name",attrs:{name:"name",placeholder:"请输入您的真实姓名",required:!0},on:{"on-enter":function(a){t.nextFocus("tel")}},model:{value:t.name,callback:function(a){t.name=a},expression:"name"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 手机号码","title-color":t.groupColor}},[n("x-input",{ref:"tel",attrs:{name:"tel",placeholder:"请输入您的手机号码",required:!0,type:"tel"},on:{"on-enter":function(a){t.nextFocus("identity")}},model:{value:t.tel,callback:function(a){t.tel=a},expression:"tel"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 身份证号码","title-color":t.groupColor}},[n("x-input",{ref:"identity",attrs:{name:"identity",placeholder:"请输入您的身份证号码",required:!0},on:{"on-enter":function(a){t.nextFocus("zhima_score")}},model:{value:t.identity,callback:function(a){t.identity=a},expression:"identity"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 芝麻信用分","title-color":t.groupColor}},[n("x-input",{ref:"zhima_score",attrs:{name:"zhima_score",placeholder:"请输入您的芝麻信用分",required:!0,type:"number"},on:{"on-enter":function(a){t.nextFocus("wechat")}},model:{value:t.zhima_score,callback:function(a){t.zhima_score=a},expression:"zhima_score"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 微信号","title-color":t.groupColor}},[n("x-input",{ref:"wechat",attrs:{name:"wechat",placeholder:"请输入您的微信号",required:!0},on:{"on-enter":function(a){t.nextFocus("address")}},model:{value:t.wechat,callback:function(a){t.wechat=a},expression:"wechat"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> 详细地址","title-color":t.groupColor}},[n("x-input",{ref:"address",attrs:{name:"address",placeholder:"请输入您的详细地址",required:!0},model:{value:t.address,callback:function(a){t.address=a},expression:"address"}})],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> <i class='iconfont icon-credentials_icon'> 请上传清晰可见的身份证正面照","title-color":t.groupColor}},[n("x-input",{ref:"idcard_pic",staticStyle:{display:"none"},attrs:{name:"idcard_pic",required:!0,placeholder:"请上传清晰可见的身份证正面照"},model:{value:t.idcard_pic,callback:function(a){t.idcard_pic=a},expression:"idcard_pic"}}),t._v(" "),n("div",{staticClass:"uploadImg"},[n("div",{staticClass:"item"},[n("div",{staticClass:"content add"},[n("label",{attrs:{for:"img-upload-idcard_pic"}},[n("upload-img",{attrs:{"model-name":"idcard_pic"},on:{changeImg:t.changeImg}}),t._v(" "),n("i",{staticClass:"iconfont icon-zhaoxiang"}),n("br"),t._v(" "),n("span",[t._v("请选择图片")])],1)])]),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"},[n("img",{attrs:{src:t.idcard_pic,alt:""}})])]),t._v(" "),n("div",{staticClass:"item"}),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"})])])],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> <i class='iconfont icon-credentials_icon'> 请上传清晰可见的身份证反面照","title-color":t.groupColor}},[n("x-input",{ref:"idcard_backpic",staticStyle:{display:"none"},attrs:{name:"idcard_backpic",required:!0,placeholder:"请上传清晰可见的身份证反面照"},model:{value:t.idcard_backpic,callback:function(a){t.idcard_backpic=a},expression:"idcard_backpic"}}),t._v(" "),n("div",{staticClass:"uploadImg"},[n("div",{staticClass:"item"},[n("div",{staticClass:"content add"},[n("label",{attrs:{for:"img-upload-idcard_backpic"}},[n("upload-img",{attrs:{"model-name":"idcard_backpic"},on:{changeImg:t.changeImg}}),t._v(" "),n("i",{staticClass:"iconfont icon-zhaoxiang"}),n("br"),t._v(" "),n("span",[t._v("请选择图片")])],1)])]),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"},[n("img",{attrs:{src:t.idcard_backpic,alt:""}})])]),t._v(" "),n("div",{staticClass:"item"}),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"})])])],1),t._v(" "),n("group",{staticClass:"dm-input",attrs:{title:"<span style='color:red'>*</span> <i class='iconfont icon-credentials_icon'> 请上传清晰可见的手持身份证照","title-color":t.groupColor}},[n("x-input",{ref:"idcard_people_pic",staticStyle:{display:"none"},attrs:{name:"idcard_people_pic",required:!0,placeholder:"请上传清晰可见的手持身份证照"},model:{value:t.idcard_people_pic,callback:function(a){t.idcard_people_pic=a},expression:"idcard_people_pic"}}),t._v(" "),n("div",{staticClass:"uploadImg"},[n("div",{staticClass:"item"},[n("div",{staticClass:"content add"},[n("label",{attrs:{for:"img-upload-idcard_people_pic"}},[n("upload-img",{attrs:{"model-name":"idcard_people_pic"},on:{changeImg:t.changeImg}}),t._v(" "),n("i",{staticClass:"iconfont icon-zhaoxiang"}),n("br"),t._v(" "),n("span",[t._v("请选择图片")])],1)])]),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"},[n("img",{attrs:{src:t.idcard_people_pic,alt:""}})])]),t._v(" "),n("div",{staticClass:"item"}),t._v(" "),n("div",{staticClass:"item"},[n("div",{staticClass:"content"})])])],1),t._v(" "),n("box",{staticStyle:{padding:"20px"}},[n("x-button",{attrs:{type:"confirm",disabled:t.submitLoadding,"show-loading":t.submitLoadding,gradients:["#50b97b","#19D5FD"]},nativeOn:{click:function(a){t.submit(a)}}},[t._v(" 下一步\n        ")])],1)],1)},g=[],h={render:A,staticRenderFns:g},v=h,C=n("X4nt"),b=e,f=C(m,v,!1,b,"data-v-16a258da",null);a.default=f.exports},Z2rg:function(t,a,n){a=t.exports=n("I71c")(!0),a.push([t.i,"\n.ApplyForLoan[data-v-16a258da] {\n  /*图片上传*/\n}\n.ApplyForLoan .dm-input[data-v-16a258da] {\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n}\n.ApplyForLoan .uploadImg[data-v-16a258da] {\n  width: 100%;\n  font-size: 0;\n  -webkit-text-size-adjust: none;\n  vertical-align: middle;\n}\n.ApplyForLoan .uploadImg .item[data-v-16a258da] {\n  display: inline-block;\n  width: 25vw;\n  height: 25vw;\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n  padding: 10px;\n  color: #969696;\n  position: relative;\n}\n.ApplyForLoan .uploadImg .item .content[data-v-16a258da] {\n  position: absolute;\n  left: 5px;\n  right: 5px;\n  top: 5px;\n  bottom: 5px;\n}\n.ApplyForLoan .uploadImg .item .content.add[data-v-16a258da] {\n  background-color: #ccc;\n}\n.ApplyForLoan .uploadImg .item .content label[data-v-16a258da] {\n  display: inline-block;\n  width: 100%;\n  height: 100%;\n  font-size: 12px;\n  overflow: hidden;\n  text-align: center;\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-orient: vertical;\n  -webkit-box-direction: normal;\n      -ms-flex-flow: nowrap column;\n          flex-flow: nowrap column;\n  -webkit-box-pack: center;\n      -ms-flex-pack: center;\n          justify-content: center;\n}\n.ApplyForLoan .uploadImg .item .content label p[data-v-16a258da] {\n  pointer-events: none;\n}\n.ApplyForLoan .uploadImg .item .content label span[data-v-16a258da] {\n  font-size: 12px;\n}\n.ApplyForLoan .uploadImg .item .content label i.iconfont[data-v-16a258da] {\n  font-size: 25px;\n}\n.ApplyForLoan .uploadImg .item .content img[data-v-16a258da] {\n  width: 100%;\n  height: 100%;\n  -o-object-fit: cover;\n     object-fit: cover;\n}\n","",{version:3,sources:["D:/demongao/yunhu/src/pages/ApplyBaseInfo.vue"],names:[],mappings:";AACA;EACE,QAAQ;CACT;AACD;EACE,+BAA+B;UACvB,uBAAuB;CAChC;AACD;EACE,YAAY;EACZ,aAAa;EACb,+BAA+B;EAC/B,uBAAuB;CACxB;AACD;EACE,sBAAsB;EACtB,YAAY;EACZ,aAAa;EACb,+BAA+B;UACvB,uBAAuB;EAC/B,cAAc;EACd,eAAe;EACf,mBAAmB;CACpB;AACD;EACE,mBAAmB;EACnB,UAAU;EACV,WAAW;EACX,SAAS;EACT,YAAY;CACb;AACD;EACE,uBAAuB;CACxB;AACD;EACE,sBAAsB;EACtB,YAAY;EACZ,aAAa;EACb,gBAAgB;EAChB,iBAAiB;EACjB,mBAAmB;EACnB,qBAAqB;EACrB,qBAAqB;EACrB,cAAc;EACd,6BAA6B;EAC7B,8BAA8B;MAC1B,6BAA6B;UACzB,yBAAyB;EACjC,yBAAyB;MACrB,sBAAsB;UAClB,wBAAwB;CACjC;AACD;EACE,qBAAqB;CACtB;AACD;EACE,gBAAgB;CACjB;AACD;EACE,gBAAgB;CACjB;AACD;EACE,YAAY;EACZ,aAAa;EACb,qBAAqB;KAClB,kBAAkB;CACtB",file:"ApplyBaseInfo.vue",sourcesContent:["\n.ApplyForLoan[data-v-16a258da] {\n  /*图片上传*/\n}\n.ApplyForLoan .dm-input[data-v-16a258da] {\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n}\n.ApplyForLoan .uploadImg[data-v-16a258da] {\n  width: 100%;\n  font-size: 0;\n  -webkit-text-size-adjust: none;\n  vertical-align: middle;\n}\n.ApplyForLoan .uploadImg .item[data-v-16a258da] {\n  display: inline-block;\n  width: 25vw;\n  height: 25vw;\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n  padding: 10px;\n  color: #969696;\n  position: relative;\n}\n.ApplyForLoan .uploadImg .item .content[data-v-16a258da] {\n  position: absolute;\n  left: 5px;\n  right: 5px;\n  top: 5px;\n  bottom: 5px;\n}\n.ApplyForLoan .uploadImg .item .content.add[data-v-16a258da] {\n  background-color: #ccc;\n}\n.ApplyForLoan .uploadImg .item .content label[data-v-16a258da] {\n  display: inline-block;\n  width: 100%;\n  height: 100%;\n  font-size: 12px;\n  overflow: hidden;\n  text-align: center;\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-orient: vertical;\n  -webkit-box-direction: normal;\n      -ms-flex-flow: nowrap column;\n          flex-flow: nowrap column;\n  -webkit-box-pack: center;\n      -ms-flex-pack: center;\n          justify-content: center;\n}\n.ApplyForLoan .uploadImg .item .content label p[data-v-16a258da] {\n  pointer-events: none;\n}\n.ApplyForLoan .uploadImg .item .content label span[data-v-16a258da] {\n  font-size: 12px;\n}\n.ApplyForLoan .uploadImg .item .content label i.iconfont[data-v-16a258da] {\n  font-size: 25px;\n}\n.ApplyForLoan .uploadImg .item .content img[data-v-16a258da] {\n  width: 100%;\n  height: 100%;\n  -o-object-fit: cover;\n     object-fit: cover;\n}\n"],sourceRoot:""}])},axSH:function(t,a,n){var e=n("kzBw");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);n("8bSs")("403926d2",e,!0)},kzBw:function(t,a,n){a=t.exports=n("I71c")(!0),a.push([t.i,"","",{version:3,sources:[],names:[],mappings:"",file:"uploadImg.vue",sourceRoot:""}])},vwcn:function(t,a,n){"use strict";function e(t){n("axSH")}var i={name:"image-html5-upload",props:{modelName:{type:String,default:"undefined"},imgNumLimit:{type:Number,default:1}},components:{},computed:{},methods:{uploadImg:function(t){this.$vux.loading.show({text:"图片加载中..."});var a=t.target,n=a.files[0],e=this,i=new FileReader;i.onload=function(t){var a=new Image;a.src=t.target.result,a.onload=function(){var t=this.naturalWidth,a=this.naturalHeight;this.naturalWidth>this.naturalHeight&&this.naturalWidth>400?(t=400,a=t*this.naturalHeight/this.naturalWidth):this.naturalHeight>this.naturalWidth&&this.naturalHeight>600&&(a=600,t=a*this.naturalWidth/this.naturalHeight);var i=document.createElement("canvas"),o=i.getContext("2d");i.width=t,i.height=a,o.drawImage(this,0,0,t,a);var l=i.toDataURL("image/jpeg",.6);n.size/1024e3>1?e.imgScale(l,2):(e.$vux.loading.hide(),e.$emit("changeImg",l,e.modelName))}},i.readAsDataURL(n)},imgScale:function(t,a){var n=new Image,e=this,i=document.createElement("canvas"),o=i.getContext("2d");n.src=t,n.onload=function(){var t=n.naturalWidth/a,l=n.naturalHeight/a;i.width=t,i.height=l,o.drawImage(this,0,0,t,l),e.$vux.loading.hide(),e.$emit("changeImg",i.toDataURL("image/jpeg"),e.modelName)}},rotateImg:function(t,a,n){if(null!==t){var e=t.height,i=t.width,o=2;null===o&&(o=0),"right"===a?++o>3&&(o=0):--o<0&&(o=3);var l=90*o*Math.PI/180,s=n.getContext("2d");switch(o){case 0:n.width=i,n.height=e,s.drawImage(t,0,0);break;case 1:n.width=e,n.height=i,s.rotate(l),s.drawImage(t,0,-e);break;case 2:n.width=i,n.height=e,s.rotate(l),s.drawImage(t,-i,-e);break;case 3:n.width=e,n.height=i,s.rotate(l),s.drawImage(t,-i,0)}}}},mounted:function(){}},o=function(){var t=this,a=t.$createElement;return(t._self._c||a)("input",{staticStyle:{display:"none"},attrs:{type:"file",id:"img-upload-"+t.modelName,multiple:"",accept:"image/*"},on:{change:function(a){t.uploadImg(a)}}})},l=[],s={render:o,staticRenderFns:l},c=s,d=n("X4nt"),r=e,p=d(i,c,!1,r,"data-v-85fb2948",null);a.a=p.exports},yLj1:function(t,a,n){var e=n("Z2rg");"string"==typeof e&&(e=[[t.i,e,""]]),e.locals&&(t.exports=e.locals);n("8bSs")("2bbb290f",e,!0)}});
//# sourceMappingURL=6.ceea61f5558da9a08c89.js.map