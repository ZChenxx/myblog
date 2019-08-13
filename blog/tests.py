from django.test import TestCase


# Create your tests here.
# 当你使用startproject命令创建新Django项目时，认证框架已经包括在项目的默认设置中。它由django.contrib.auth应用和以下两个中间件（middleware）类组成（这两个中间类位于项目的MIDDLEWARE_CLASSES设置中）：
#
# AuthenticationMiddleware：使用会话管理用户和请求
# SessionMiddleware：跨请求处理当前会话
# 一个中间件是一个带有方法的类，在解析请求或响应时，这些方法在全局中执行。
#
# 该认证框架还包括以下模块：
#
# User：一个有基础字典的用户模型；主要字段有：username，password，email，first_name，last_name和is_active。
# Group：一个用于对用户分类的组模型。
# Permission：执行特定操作的标识。