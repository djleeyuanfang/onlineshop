Date.prototype.format = function(fmt) {
     var o = {
        "M+" : this.getMonth()+1,                 //月份
        "d+" : this.getDate(),                    //日
        "h+" : this.getHours(),                   //小时
        "m+" : this.getMinutes(),                 //分
        "s+" : this.getSeconds(),                 //秒
        "q+" : Math.floor((this.getMonth()+3)/3), //季度
        "S"  : this.getMilliseconds()             //毫秒
    };
    if(/(y+)/.test(fmt)) {
            fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
     for(var k in o) {
        if(new RegExp("("+ k +")").test(fmt)){
             fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
         }
     }
    return fmt;
};
Date.prototype.fromString = function (str) {
    let d = str.split("-");
    this.setFullYear(Number(d[0]));
    this.setMonth(Number(d[1]) - 1);
    this.setDate(Number(d[2]));
};
function toTop() {
    let speed=200;//滑动的速度
    $('body,html').animate({ scrollTop: 0 }, speed);
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
                }
            o[this.name].push(this.value || '');
            } else {
            o[this.name] = this.value || '';
            }
        });
    return o;
};

function deal_res_code(res) {
    if (res.code===1024){
        window.location.href = res.redirect;
    }
}

function article_node(){
    return $("<article class=\"post-152 post type-post status-publish format-standard hentry category-people category-photos\" >\n" +
        "            <div class=\"post-format-content\">\n" +
        "                <div class=\"post-thumbnail\">\n" +
        "                    <img width=\"480\" src=\"/img/default.png\" class=\"attachment-thumbnail wp-post-image\" alt=\"\">\n" +
        "                </div>\n" +
        "                <div class=\"content-wrap\">\n" +
        "                    <h1 class=\"entry-title\">\n" +
        "                        <a href=\"#\" class=\"featured-image\" rel=\"bookmark\">Example</a>\n" +
        "                    </h1>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </article>")
}

function article_detail_node() {
    return $("<article class=\"post-152 post type-post status-publish format-standard hentry category-people category-photos\">\n" +
        "                    <div class=\"post-format-content\">\n" +
        "                        <div class=\"post-thumbnail\">\n" +
        "                            <img width=\"480\" height=\"480\" src=\"/img/default2.png\" class=\"attachment-thumbnail wp-post-image\" alt=\"\">\n" +
        "                        </div>\n" +
        "                        <div class=\"content-wrap\">\n" +
        "                            <h1 class=\"entry-title\">\n" +
        "                                <a href=\"#\" class=\"featured-image\" rel=\"bookmark\" onclick=\"move_front(this)\">向前移动</a>\n" +
        "                                <a href=\"#\" class=\"featured-image\" rel=\"bookmark\" onclick=\"show_img(this)\">显示照片</a>\n" +
        "                                <a href=\"#\" class=\"featured-image\" rel=\"bookmark\" onclick=\"move_back(this)\">向后移动</a>\n" +
        "                            </h1>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                </article>")
}
function article_cloud_image_node() {
    return $("<article class=\"post-152 post type-post status-publish format-standard hentry category-people category-photos\">\n" +
                "                                <div class=\"post-format-content\">\n" +
                "                                    <div class=\"post-thumbnail\">\n" +
                "                                        <img width=\"125\" height=\"100\" src=\"/img/default.png\" class=\"attachment-thumbnail wp-post-image\" alt=\"\">\n" +
                "                                    </div>\n" +
                "                                    <div class=\"content-wrap\">\n" +
                "                                        <h1 class=\"entry-title\">\n" +
                "                                            <a class=\"featured-image\" rel=\"bookmark\" onclick=\"select_image_to_content(this)\">图片名</a>\n" +
                "                                        </h1>\n" +
                "                                    </div>\n" +
                "                                </div>\n" +
                "                            </article>");
}