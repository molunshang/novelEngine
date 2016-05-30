from flask_wtf import Form;
from wtforms import (StringField, IntegerField, BooleanField)
from wtforms.validators import DataRequired


class siteConfigForm(Form):
    SiteName = StringField("siteName", validators=[DataRequired()]);
    SiteHost = StringField("siteHost", validators=[DataRequired()]);
    SiteEncoding = StringField("siteEncoding", validators=[DataRequired()]);
    ListRegex = StringField("listRegex", validators=[DataRequired()]);
    ListTimeRegex = StringField("listTimeRegex", validators=[DataRequired()]);
    DetailRegex = StringField("detailRegex");
    DetailListRegex = StringField("detailListRegex", validators=[DataRequired()]);
    DetailItemRegex = StringField("detailItemRegex", validators=[DataRequired()]);
    ItemSort = BooleanField("itemSort");
    DetailMatch = StringField("detailMatch", validators=[DataRequired()]);
    MatchType = IntegerField("matchType", validators=[DataRequired()]);
    TitleRegex = StringField("titleRegex", validators=[DataRequired()]);
    AuthorRegex = StringField("authorRegex", validators=[DataRequired()]);
    IconRegex = StringField("iconRegex", validators=[DataRequired()]);
    LastTime = StringField("lastTime", validators=[DataRequired()]);
