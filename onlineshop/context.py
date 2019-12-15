from order.models import Collection


'''
模板 全局量
'''


def collection(req):
    # collections = []
    # for i, c in enumerate(Collection.objects.all()):
    #     style = ""
    #     if i % 5 == 0:
    #         style = "danger"
    #     elif i % 5 == 1:
    #         style = "warning"
    #     elif i % 5 == 2:
    #         style = "success"
    #     elif i % 5 == 3:
    #         style = "default"
    #     elif i % 5 == 4:
    #         style = "primary"
    #     collections.append({
    #         "style": style,
    #         "collection": c,
    #         "is_select": good.collections.filter(label=c.label).exists()
    #     })

    return {"collections": Collection.objects.filter(is_show=True).order_by("index")}