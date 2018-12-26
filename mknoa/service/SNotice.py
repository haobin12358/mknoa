from mknoa.common.base_service import SBase
from mknoa.models.notice import Notice
from sqlalchemy import or_, and_, extract

class SNotice(SBase):

    def s_update_notice(self, notice_id, notice):
        self.session.query(Notice).filter_by(notice_id=notice_id).update(notice)
        self.session.commit()
        return True

    def get_notice_list_by_page(self, page_size, page_num):
        return self.session.query(Notice.notice_id, Notice.notice_title, Notice.notice_message, Notice.notice_updatetime)\
            .filter_by(notice_status=141).offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_notice_list_count(self):
        return self.session.query(Notice.notice_id, Notice.notice_title, Notice.notice_message,
                                  Notice.notice_updatetime) \
            .filter_by(notice_status=141).all()

    def get_notice_message_by_noticeid(self, notice_id):
        return self.session.query(Notice.notice_title, Notice.notice_message).filter_by(notice_id=notice_id).first()