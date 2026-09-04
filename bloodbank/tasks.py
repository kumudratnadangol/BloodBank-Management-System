
import threading
from .services import ReportService


def run_expire_units_task():
    """
    Runs the expiry-check logic in a background thread so the API request
    returns immediately without waiting for the DB update to finish.
    This satisfies the assignment's requirement for an async/background
    processing component that updates a database table on client request.
    """
    def _job():
        updated_count = ReportService.expire_old_units()
        print(f"[Background Task] Expired units updated: {updated_count}")

    thread = threading.Thread(target=_job)
    thread.start()