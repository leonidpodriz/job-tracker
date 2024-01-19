from job_tracker.permissions import GeneralObjectPermission


class ApplicationObjectPermission(GeneralObjectPermission):
    protected_fields = ("status", "notes")
