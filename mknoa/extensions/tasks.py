# -*- coding: utf-8 -*-
import uuid
from datetime import date, timedelta, datetime

from flask import current_app
from flask_celery import Celery
from sqlalchemy import cast, Date

from mknoa import create_app
from mknoa.common.error_response import NotFound
from mknoa.config.enums import ApplyStatus
from mknoa.control.CApproval import CApproval
from mknoa.extensions.register_ext import db
from mknoa.models import Approvals, ApprovalSov

celery = Celery()


@celery.task()
def auto_agree_task(approvalsov_id):
    approvalsov = ApprovalSov.query.filter_by_(approvalsov_id=approvalsov_id).first()
    if approvalsov.approvalsov_suggestion == 132:
        return
    else:
        capp = CApproval()
        if capp.get_approvalsov_now_by_subid(approvalsov.approvalsub_id):
            capp.deal(approvalsov.approvalsub_id, '平台', 132, '通过')



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # fetch_share_deal()
        # auto_evaluate()
        auto_agree_task()