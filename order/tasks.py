import xlwt


def to_report(orders, report):
    row_header = ["订单号", "订单状态", "商品信息", "金额", "收货信息", "物流单号", "物流公司", "客户邮箱", "订单创建时间", "订单付款时间", "订单发货时间",]

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    for i, item in enumerate(row_header):
        worksheet.write(1, i, label=item)

    count = 0
    for i, order in enumerate(orders):
        count += 1
        item_lst = []
        for item in order.orderitem_set.all():
            item_lst.append("{} {} ￥{} x {}".format(item.good.title, item.size, item.good.price, item.amount))

        worksheet.write(i + 2, 0, label=order.id)
        worksheet.write(i + 2, 1, label=order.get_status_display())
        worksheet.write(i + 2, 2, label="#".join(item_lst))  # 订单项目
        worksheet.write(i + 2, 3, label=order.cash)
        worksheet.write(i + 2, 4, label=order.address.replace("/", " "))
        worksheet.write(i + 2, 5, label=order.express_number)
        worksheet.write(i + 2, 6, label=order.express_cmp)
        worksheet.write(i + 2, 7, label=order.user.mail)
        worksheet.write(i + 2, 8, label=order.create_time)
        worksheet.write(i + 2, 9, label=order.pay_time)
        worksheet.write(i + 2, 10, label=order.ship_time)

    # workbook.data
    workbook.save(report.get_local_path)
    report.is_finish = True
    report.count = count
    report.save()
