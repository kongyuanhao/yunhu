/**
 * Created by klk on 2017/7/4.
 */
function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}
(function (document, window, $) {
    'use strict';
    (function () {
        var $table = $('#table').bootstrapTable({
            url: "/shopdata/shoplist/",
            sidePagination: "server",
            search: true,
            showRefresh: true,
            showToggle: true,
            showColumns: true,
            toolbar: '#exampleToolbar',
            iconSize: 'outline',
            detailView: true,
            pagination: true,
            paginationLoop: true,
            height: getHeight(),
            pageSize: 20,
            filter: true,
            icons: {
                refresh: 'glyphicon-repeat',
                toggle: 'glyphicon-list-alt',
                columns: 'glyphicon-list'
            },
            columns: [{
                field: 'id',
                title: 'Item ID'
            }, {
                field: 'shop_province',
                title: '省份'
            }, {
                field: 'shop_city',
                title: '市'
            }, {
                field: 'shop_zone',
                title: '区域'
            }, {
                field: 'shop_area',
                title: '街道'
            }, {
                field: 'shop_type1',
                title: '分类1'
            }, {
                field: 'shop_type2',
                title: '分类2'
            }, {
                field: 'shop_type3',
                title: '分类3'
            }, {
                field: 'shop_name',
                title: '商铺名称'
            }, {
                field: 'shop_address',
                title: '商铺地址'
            }, {
                field: 'shop_tel',
                title: '商铺电话'
            }, {
                field: 'shop_merchandise',
                title: '商铺介绍'
            }, {
                field: 'shop_img',
                title: '商铺图片'
            }, {
                field: 'shop_linkman',
                title: '联系人'
            }, {
                field: 'spider_time',
                title: '采集时间'
            }, {
                field: 'spider_site',
                title: '采集站点',
                // filter: {
                //     type: "select",
                //     data: []
                // }
            }, {
                field: 'spider_url',
                title: '采集网址'
            }]
        });
        // $table.bootstrapTable("setFilterData", "name", ["item 1", "item 2", "item 3"]);
    })()


})(document, window, jQuery);
