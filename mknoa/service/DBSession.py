from mknoa.common.base_service import db_session

def get_session():
    try:
        session = db_session()
        status = True
    except Exception as e:
        print(e)
        session = None
        status = False
    finally:
        return session, status
