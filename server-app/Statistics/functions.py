from DataBase.models import DProject
from DataBase.models import DUser


class Statistics(object):
    @staticmethod
    def get_donation_sum(user_dict):
        # Get overall sum of donation received by charity or made by donor.
        donation_sum = 0
        for pid, sub_dict in user_dict['donate_history'].items():
            project_dict = Statistics.get_project_dict(pid)
            if user_dict['type'] == 1:
                for uid, sub_sub_dict in sub_dict.items():
                    for timestamp, num in sub_sub_dict.items():
                        donation_sum = donation_sum + num * project_dict['price']
            elif user_dict['type'] == 2:
                for timestamp, num in sub_dict.items():
                    donation_sum = donation_sum + num * project_dict['price']
        return donation_sum

    @staticmethod
    def get_project_dict(pid):
        dproject = DProject()
        project = dproject.get_project({"pid": pid})
        return project.to_dict()

    @staticmethod
    def get_user_dict(uid):
        duser = DUser()
        user = duser.get_user({"uid": uid})
        return user.to_dict()
