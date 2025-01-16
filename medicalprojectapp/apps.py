from django.apps import AppConfig


class MedicalprojectappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicalprojectapp'

    # def ready(self):
    #     try:
    #         from django.contrib.auth.models import Group
    #         groups = ["Doctors", "Users", "Receptionists"]
    #         for group in groups:
    #             Group.objects.get_or_create(name=group)
    #     except (ProgrammingError, OperationalError):
    #         # Ignore errors during migration or app initialization
    #         pass
    def ready(self):
        import medicalprojectapp.signals