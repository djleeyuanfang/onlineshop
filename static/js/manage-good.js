$('#good-table').bootstrapTable({
    url: "/manager/goods/query/",
    method: "GET",
    striped: true,                      //是否显示行间隔色
    cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    toolbar: "#search-good-table-toolbox",

    sortable: true,                     //是否启用排序
    sortOrder: "asc",                   //排序方式
    // 分页
    sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
    pagination: true,                   //是否显示分页（*）
    pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
    pageSize: 15,                        //每页的记录行数（*）
    pageList: [15, 25, 50, 100],         //可供选择的每页的行数（*）
    search: false,                      //是否显示表格搜索
    strictSearch: true,
    showColumns: true,                  //是否显示所有的列（选择显示的列）
    showRefresh: true,                  //是否显示刷新按钮
    minimumCountColumns: 2,             //最少允许的列数
    clickToSelect: true,                //是否启用点击选中行
    //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
    uniqueId: "good_id",                     //每一行的唯一标识，一般为主键列
    showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
    cardView: false,                    //是否显示详细视图
    detailView: false,                  //是否显示父子表
    queryParams: function (params) {
        let p = $("#search-good-form").serializeObject();
        p["page_size"] = params.limit;
        p["page_num"] = (params.offset / params.limit) + 1;
        return p;
    },
    responseHandler: function(res) {
        console.log(res);
        //data["Customer_name"] = list[0].customer.name;
        return {
            "total": res.total, //总页数
            "rows": res.rows    //数据
        };
    },
    columns: [ //{checkbox: true},
        {
            field: 'good_id',
            title: '商品编号',
        },
        {
            field: 'first_img',
            title: '封面图',
            sortable: false,
            formatter: function (value, row, index) {
                return "<a href='/good/" + row.good_id +"/' target='_blank'><img src='/" + value +"' width='150'></a>";
            }
        },
        {
            field: 'title',
            title: '标题',
            sortable: false,
        },
        {
            field: 'price',
            title: '价格',
            sortable: false,
        },
        {
            field: 'sizes',
            title: '尺码',
            sortable: false,
            formatter: function (value, row, index) {
                let html = "";
                for (let i = 0; i < value.length; i++){
                    html += "<div>尺码:" + value[i].size + " 库存:" + value[i].amount + "</div>";
                }
                return html;
            }
        },
        {
            field: 'collections',
            title: '分类标签',
            sortable: false,
            formatter: function (value, row, index) {
                let html = "";
                let label_style = ["primary", "warning", "danger", "default", "success"];

                for (let i = 0; i < value.length; i++){
                    html += "<span class='label label-"+ label_style[i%5] +"'>" + value[i] +"</span>";
                }
                return html;
            }
        },
        {
            field: 'is_sell',
            title: '在售状态',
            sortable: false,
            formatter: function (value, row, index) {
                if (value === true) {
                    return "在售";
                }
                else{
                    return "下架";
                }
            }
        },
        {
            field: 'week_sell_amount',
            title: '周销量',
            sortable: false
        },
        {
            field: 'month_sell_amount',
            title: '月销量',
            sortable: false
        },
        {
            field: 'total_sell_amount',
            title: '总销量',
            sortable: false
        },
    ]
});