from mknoa.common.base_service import SBase
from mknoa.models.approval import Approvals, ApprovalPower, ApprovalLevel, ApprovalSub, ApprovalSov, ApprovalMould
from sqlalchemy import or_, and_, extract

class SApproval(SBase):

    def s_update_approval_power(self, approvalpower_id, approval_power):
        self.session.query(ApprovalPower).filter_by(approvalpower_id=approvalpower_id).update(approval_power)
        self.session.commit()
        return True

    def s_update_approval_level(self, approvallevel_id, approval_level):
        self.session.query(ApprovalLevel).filter_by(approvallevel_id=approvallevel_id).update(approval_level)
        self.session.commit()
        return True

    def s_update_approval(self, approval_id, approval):
        self.session.query(Approvals).filter_by(approval_id=approval_id).update(approval)
        self.session.commit()
        return True

    def get_approvalpowerid_by_approvalid(self, approval_id):
        return self.session.query(ApprovalPower.approvalpower_id).filter_by(approval_id=approval_id).all()

    def get_approvallevelid_by_approvalid(self, approval_id):
        return self.session.query(ApprovalLevel.approvallevel_id).filter_by(approval_id=approval_id).all()

    def get_approval_list_by_page(self, page_num, page_size):
        return self.session.query(Approvals.approval_id, Approvals.approval_name)\
            .filter_by(approval_status=91).offset(page_size * (page_num - 1)).limit(page_size).all()

    def get_approval_list_count(self):
        return self.session.query(Approvals.approval_id, Approvals.approval_name) \
            .filter_by(approval_status=91).all()

    def get_approval_list_by_none(self):
        return self.session.query(Approvals.approval_id, Approvals.approval_name) \
            .filter_by(approval_status=91).all()

    def get_approval_message_by_approvalid(self, approval_id):
        return self.session.query(Approvals.approval_name, Approvals.mould_id).filter_by(approval_id=approval_id).first()

    def get_approvalpower_by_approvalid(self, approval_id):
        return self.session.query(ApprovalPower.tag_id)\
            .filter_by(approval_id=approval_id).filter_by(approvalpower_status=111).all()

    def get_approvallevel_by_approvalid(self, approval_id):
        return self.session.query(ApprovalLevel.tag_id, ApprovalLevel.approvallevel_index)\
            .filter_by(approval_id=approval_id).filter_by(approvallevel_status=101)\
            .order_by(ApprovalLevel.approvallevel_index.asc()).all()

    def get_approvalsov_by_tagid_status(self, tag_id, approvalsov_suggestion=None):
        approvalsov = self.session.query(ApprovalSov.approvalsub_id).filter(ApprovalSov.tag_id == tag_id)
        if approvalsov_suggestion:
            if approvalsov_suggestion == "全部":
                approvalsov = approvalsov.all()
            elif approvalsov_suggestion == "已审批":
                approvalsov = approvalsov.filter(ApprovalSov.approvalsov_suggestion != 131)
            elif approvalsov_suggestion == "未审批":
                approvalsov = approvalsov.filter(ApprovalSov.approvalsov_suggestion == 131)
            else:
                approvalsov = None
        else:
            approvalsov = approvalsov.all()
        return approvalsov

    def get_approvalsub_by_userid_status(self, user_id, approvalsov_suggestion=None):
        approvalsub = self.session.query(ApprovalSub.approvalsub_id, ApprovalSub.approvalsub_createtime,
                                         ApprovalSub.approvalsub_endtime, ApprovalSub.user_truename,
                                         ApprovalSub.approval_name, ApprovalSub.approvalsub_status)\
            .filter(ApprovalSub.user_id == user_id)
        if approvalsov_suggestion:
            if approvalsov_suggestion == "全部":
                approvalsub = approvalsub.all()
            elif approvalsov_suggestion == "已审批":
                approvalsub = approvalsub.filter(ApprovalSub.approvalsub_status != 121)
            elif approvalsov_suggestion == "未审批":
                approvalsub = approvalsub.filter(ApprovalSub.approvalsub_status == 121)
            else:
                approvalsub = None
        else:
            approvalsub = approvalsub.all()
        return approvalsub

    def get_approvalsub_by_subid(self, approvalsub_id):
        return self.session.query(ApprovalSub.approval_name, ApprovalSub.approvalsub_createtime,
                                  ApprovalSub.approvalsub_endtime, ApprovalSub.user_truename, ApprovalSub.approvalsub_status)\
            .filter_by(approvalsub_id=approvalsub_id).first()

    def get_approvalsub_message_by_subid(self, approvalsub_id):
        return self.session.query(ApprovalSub.approval_name, ApprovalSub.approvalsub_createtime,
                                  ApprovalSub.approvalsub_endtime, ApprovalSub.user_truename, ApprovalSub.user_telphone)\
            .filter_by(approvalsub_id=approvalsub_id).first()

    def get_approval_message(self, approvalsub_id):
        return self.session.query(ApprovalMould.mouldelement_name, ApprovalMould.element_value,
                                  ApprovalMould.element_value_name, ApprovalMould.element_name,
                                  ApprovalMould.mouldelement_index, ApprovalMould.mouldelement_rank)\
            .filter_by(approvalsub_id=approvalsub_id).order_by(ApprovalMould.mouldelement_index.asc()).all()

    def get_approvalsov_message_by_subid(self, approvalsub_id):
        return self.session.query(ApprovalSov.approvalsov_suggestion, ApprovalSov.approvalsov_createtime,
                                  ApprovalSov.tag_id, ApprovalSov.user_truename, ApprovalSov.approvalsov_message)\
            .filter(ApprovalSov.approvalsub_id == approvalsub_id).filter(ApprovalSov.approvalsov_suggestion != 134)\
            .order_by(ApprovalSov.approvalsub_index.asc()).all()

    def get_approvalsov_now_by_subid(self, approvalsub_id):
        return self.session.query(ApprovalSov.approvalsov_id, ApprovalSov.approvalsub_index)\
            .filter_by(approvalsub_id=approvalsub_id)\
            .filter_by(approvalsov_suggestion=131).first()

    def s_update_approvalsov(self, approvalsov_id, approvalsov):
        self.session.query(ApprovalSov).filter_by(approvalsov_id=approvalsov_id).update(approvalsov)
        self.session.commit()
        return True

    def get_approvalsov_now_by_subid_index(self, approvalsub_id, approvalsub_index):
        return self.session.query(ApprovalSov.approvalsov_id, ApprovalSov.approvalsub_index)\
            .filter_by(approvalsub_id= approvalsub_id).filter_by(approvalsub_index=approvalsub_index)\
            .filter_by(approvalsov_suggestion=134).first()

    def s_update_approvalsub(self, approvalsub_id, approvalsub):
        self.session.query(ApprovalSub).filter_by(approvalsub_id=approvalsub_id).update(approvalsub)
        self.session.commit()
        return True

    def get_tagid_by_approvalsub_suggestion(self, approvalsub_id):
        return self.session.query(ApprovalSov.tag_id).filter_by(approvalsub_id=approvalsub_id)\
            .filter_by(approvalsov_suggestion=131).first()