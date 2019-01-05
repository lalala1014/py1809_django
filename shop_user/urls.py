from django.conf.urls import url
from . import views


app_name = "buy"
urlpatterns = [
    url(r'^login/$', views.login,name="login"), # 登录界面
    url(r'^regist/$',views.regist,name="regist"), # 注册界面
    url(r'^index/$',views.index,name="index"), # 登陆成功的首页
    url(r'formlist/$',views.formlist),   # 订单列表
    url(r'^update_user/$',views.update_user,name="update_user"), # 修改个人资料界面
    url(r'^cart/$',views.Cart), # 购物车界面
    url(r'^shangyi/$',views.shangyi),   # 上衣界面
    url(r'^xiazhuang/$',views.xiazhuang),   # 下装界面
    url(r'^shoes/$', views.shoes),  # 鞋界面
    url(r'^bags/$', views.bags),  # 包界面
    url(r'^Accessories/$',views.Accessories),   # 配饰界面
    url(r'^code/$', views.create_code_img),  # 创建验证码
    url(r'^exit/$',views.exit),   # 退出登录
]