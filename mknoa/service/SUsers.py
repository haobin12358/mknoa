from mknoa.common.base_service import SBase
from mknoa.models.user import Users, Tags, UserTags
from mknoa.models.power import PowerTag
from sqlalchemy import or_, and_, extract

class SUsers(SBase):

    def get_password_by_name(self, user_name):
        return self.session.query(Users.user_password).filter_by(user_name=user_name).first()

    def get_userid_by_name(self, user_name):
        return self.session.query(Users.user_id).filter_by(user_name=user_name).first()

    def get_user_message(self, user_id):
        return self.session.query(Users.user_name, Users.user_createtime, Users.user_email, Users.user_telphone,
                                  Users.user_truename, Users.user_icon, Users.user_location, Users.user_contract,
                                  Users.user_message, Users.user_qq, Users.user_status, Users.user_wechat)\
            .filter_by(user_id=user_id).first()

    def get_usertagid_by_user(self, user_id):
        return self.session.query(UserTags.tag_id).filter_by(user_id=user_id).filter_by(usertag_status=31).all()

    def get_tagname_by_tagid(self, tag_id):
        return self.session.query(Tags.tag_name, Tags.tag_level, Tags.tag_id, Tags.tag_status)\
            .filter_by(tag_id=tag_id).first()

    def get_username_by_userid(self, user_id):
        return self.session.query(Users.user_name).filter_by(user_id=user_id).first()

    def get_taglevel_by_tagid(self, tag_id):
        return self.session.query(Tags.tag_level).filter_by(tag_id=tag_id).first()

    def get_all_taglevel(self):
        return self.session.query(Tags.tag_level).all()

    def s_update_tag(self, tag_id, tag):
        self.session.query(Tags).filter_by(tag_id=tag_id).update(tag)
        return True

    def s_update_tagpower(self, powertag_id, powertag):
        self.session.query(PowerTag).filter_by(powertag_id=powertag_id).update(powertag)
        return True

    def get_userid_by_tagid(self, tag_id):
        return self.session.query(Tags.user_id).filter_by(tag_id=tag_id).first()

    def get_tagpowerid_by_powerid(self, power_id):
        return self.session.query(PowerTag.powertag_id).filter_by(power_id=power_id).all()

    # get_taglist_by_userid 和 get_taglist_count 成组出现
    def get_taglist_by_userid(self, page_num, page_size, user_id):
        taglist = self.session.query(Tags.tag_id, Tags.tag_name, Tags.tag_level).filter_by(tag_status=21)
        if user_id == "1":
            taglist = taglist.filter_by(user_id=user_id)
        return taglist.offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_taglist_count(self, user_id):
        taglist = self.session.query(Tags.tag_id, Tags.tag_name, Tags.tag_level).filter_by(tag_status=21)
        if user_id == "1":
            taglist = taglist.filter_by(user_id=user_id)
        return taglist.all()

    # get_userlist_page 和 get_userlist 成组出现
    def get_userlist_page(self, page_num, page_size):
        return self.session.query(Users.user_id, Users.user_name, Users.user_telphone)\
            .filter(Users.user_status!=12).offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_userlist(self):
        return self.session.query(Users.user_id, Users.user_name, Users.user_telphone) \
            .filter(Users.user_status != 12).all()