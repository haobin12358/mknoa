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
            .filter_by(approval_id=approval_id).filter_by(approvallevel_status=101).all()