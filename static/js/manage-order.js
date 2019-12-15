$('#order-table').bootstrapTable({
    url: "/manager/order/query/",
    method: "GET",
    striped: true,                      //是否显示行间隔色
    cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    toolbar: "#search-order-table-toolbox",

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
    uniqueId: "order_id",                     //每一行的唯一标识，一般为主键列
    showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
    cardView: false,                    //是否显示详细视图
    detailView: false,                  //是否显示父子表
    queryParams: function (params) {
        let p = $("#search-order-form").serializeObject();
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
            field: 'order_id',
            title: '订单号',
            formatter: function (value, row, index) {
                return "<a href='/order/" + value +"/' target='_blank'>"+ value +"</a>"
            }
        },
        {
            field: 'status',
            title: '订单状态',
            sortable: false,
        },
        {
            field: 'items',
            title: '订单项目',
            sortable: false,
            formatter: function (value, row, index) {
                let html = "<table>";
                for (let i = 0; i < value.length; i++){
                    let item = value[i];
                    html += "<tr><td><img width='100' src='/" + item.src +"'></td>" +
                        "<td><div>商品ID：" + item.good_id +"</div><div>" + item.title + " " + item.size + " ￥" + item.price + " x " + item.amount +"</div></td>"+
                        "</tr>";
                }
                return html + "</table>"
            }
        },
        {
            field: 'cash',
            title: '金额',
            sortable: false,
        },
        {
            field: 'user',
            title: '买家',
            sortable: false,
        },
        {
            field: 'times',
            title: '时间信息',
            sortable: false,
            formatter: function (value, row, index) {
                return "<div><div>订单创建时间：" + value.create_time + "</div>" +
                "<div>订单付款时间：" + value.pay_time + "</div>" +
                "<div>订单发货时间：" + value.ship_time + "</div></div>"
            }
        }
    ]
});