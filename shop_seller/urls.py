from django.conf.urls import url
from . import views
from django.views.static import serve

app_name = "shop"
urlpatterns = [
    url(r'^login/$', views.login,name="login"), # 登录界面
    url(r'^manage/$',views.manage,name="manage"), # 后台管理首页
    url(r'^welcome/$',views.welcome,name="welcome"), # 管理首页
    url(r'^update_shop/$',views.update_shop,name="update_shop"), # 修改店铺资料页面
    url(r'^product_list/$',views.product_list),   # 产品列表管理页面
    url(r'^product_add/$',views.product_add),    # 添加产品小弹窗
    url(r'^admin_role/$',views.admin_role),     # 用户列表
    url(r'^edit/$',views.edit), # 修改店铺资料小弹窗
    url(r'^code/$', views.create_code_img),  # 创建验证码
    url(r'^exit/$',views.exit),   # 退出
]