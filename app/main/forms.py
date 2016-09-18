# -*-coding: utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, FileField, \
                    TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms.widgets import TextArea

photos = UploadSet('photos', IMAGES)

from ..models import User, Role


class EditProfileForm(Form):
    name = StringField(u'姓名或昵称', validators=[Length(0, 64)])
    location = StringField(u'城市', validators=[Length(0,64)])
    website = StringField(u'网站', validators=[Length(0,64), Optional(),
                         URL(message= u'请输入有效的地址，比如：http://withlihui.com')], render_kw={"placeholder": "<i class = glyphicon glyphicon-user form-control-feedback></i>"})
    about_me = TextAreaField(u'关于我', validators=[Length(0,64)], render_kw={"placeholder": u"我是......"})
    submit = SubmitField(u'提交')


class TESTForm(Form):
    url = StringField("Enter URL",
                   validators=[URL(), Required()],
                   )
    submit = SubmitField('Search')

    def validate_url(self, field):
        if "http://" not in field.data:
            raise ValidationError(u'请输入有效的地址，比如：http://withlihui.com')

class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(message= u'邮件不能为空'), Length(1, 64),
                                           Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    username = StringField(u'用户名', validators=[Required(message= u'用户名不能为空'), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                      u'用户名只能有字母，'
                                                      u'数字，点和下划线组成。')])
    confirmed = BooleanField(u'确认状态')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'姓名或昵称', validators=[Length(0, 64)])
    location = StringField(u'城市', validators=[Length(0, 64)])
    website = StringField(u'网站', validators=[Length(0, 64),
                                             URL(message= u'请输入有效的地址，比如：http://withlihui.com')])
    about_me = TextAreaField(u'关于我', validators=[Length(0, 64)])
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经注册，请直接登录。')

    def validate_username(self, field):
        if field.data != self.user.username and \
        User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册，换一个吧。')


class TagForm(Form):
    title = StringField(u'标题', validators=[Required()])
    sub_title = StringField(u'副标题')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')], default='1')
    photos = FileField(u'选择图片')
    submit = SubmitField(u'提交')


class WallForm(Form):
    title = StringField(u'标题')
    about = StringField(u'介绍')
    theme = RadioField(
        u'选择一个主题',
        choices=[('1', u'黑底白字'), ('2', u'白底黑字'), ('3', u'紫底白字')]
    )
    photo = FileField(u'图片', validators=[
        FileRequired(),
        FileAllowed(photos, u'只能上传图片！')
    ])
    submit = SubmitField(u'提交')


class NormalForm(Form):
    title = StringField(u'标题')
    about = TextAreaField(u'介绍')
    photo = FileField(u'图片', validators=[
        FileRequired(),
        FileAllowed(photos, u'只能上传图片！')
    ])
    submit = SubmitField(u'提交')
