from DataBase.models import DProject
from DataBase.models import DUser
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time


class Statistics(object):
    @staticmethod
    def export_statistics(identity):
        # Takes pid or uid.
        try:
            d = Statistics.get_project_dict(identity)
        except AttributeError:
            d = Statistics.get_user_dict(identity)
        pp = PdfPages('report.pdf')
        if 'pid' in d:
            overall_sum, monthly_sum = Statistics.get_donation_sum(d)
            x_iter = range(len(monthly_sum[0]))
            fig = plt.figure()
            plt.grid(axis="y")
            for x, y in zip(x_iter, monthly_sum[1]):
                plt.text(x, y, round(y, 2), ha='center', va='bottom')
            plt.title("Monthly Collection")
            plt.xlabel('Total: ' + str(round(overall_sum, 2)) + ' GBP')
            plt.xticks(x_iter, monthly_sum[0])
            plt.ylabel('/GBP')
            plt.bar(x_iter, monthly_sum[1])
            pp.savefig(fig)

            completeness = Statistics.get_completeness(d)
            x_iter = range(len(completeness[0]))
            fig = plt.figure()
            plt.grid(True)
            for x, y in zip(x_iter, completeness[1]):
                plt.text(x, y, round(y, 2), ha='left', va='top')
            plt.title("Collection Completeness")
            plt.xticks(x_iter, completeness[0])
            plt.ylim(-0.1, 1.1)
            plt.plot(x_iter, completeness[1])
            pp.savefig(fig)

            region_dist = Statistics.get_region_distribution(d)
            fig = plt.figure()
            plt.title("Country/Region Distribution")
            plt.pie(region_dist[1], labels=region_dist[0], autopct='%.2f%%')
            pp.savefig(fig)
        else:
            overall_sum, monthly_sum = Statistics.get_donation_sum(d)
            x_iter = range(len(monthly_sum[0]))
            fig = plt.figure()
            plt.grid(axis="y")
            for x, y in zip(x_iter, monthly_sum[1]):
                plt.text(x, y, round(y, 2), ha='center', va='bottom')
            plt.title("Monthly Donation")
            plt.xlabel('Total: ' + str(round(overall_sum, 2)) + ' GBP')
            plt.xticks(x_iter, monthly_sum[0])
            plt.ylabel('/GBP')
            plt.bar(x_iter, monthly_sum[1])
            pp.savefig(fig)
        pp.close()
        return 0

    @staticmethod
    def get_completeness(project_dict):
        # Get monthly completeness of a project.
        # Returns completeness: [year-month_list, completeness_list].
        overall_sum, monthly_sum = Statistics.get_donation_sum(project_dict)
        target = project_dict['total_num']
        current_sum = 0
        completeness = []
        for i in range(len(monthly_sum[1])):
            current_sum += monthly_sum[1][i]
            completeness.append(current_sum / project_dict['price'] / target)
        completeness = [monthly_sum[0], completeness]
        return completeness

    @staticmethod
    def get_donation_sum(d):
        # Get overall and monthly sum of donation of a project/received by a charity/made by a donor.
        # For project: from start_time to this month. For user: from first donation to this month.
        # Takes project_dict or user_dict.
        # Returns overall_sum: int, monthly_sum: [year-month_list, sum_list].
        overall_sum = 0
        monthly_sum_dict = {}
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                for timestamp, num in sub_dict.items():
                    overall_sum += num * d['price']
                    dt = datetime.fromtimestamp(int(timestamp))
                    ym = dt.strftime('%Y%m')
                    if ym in monthly_sum_dict.keys():
                        monthly_sum_dict[ym] = monthly_sum_dict[ym] + num * d['price']
                    else:
                        monthly_sum_dict[ym] = num * d['price']
        else:
            for pid, sub_dict in d['donate_history'].items():
                project_dict = Statistics.get_project_dict(pid)
                if d['type'] == 1:
                    for uid, sub_sub_dict in sub_dict.items():
                        for timestamp, num in sub_sub_dict.items():
                            overall_sum += num * project_dict['price']
                            dt = datetime.fromtimestamp(int(timestamp))
                            ym = dt.strftime('%Y%m')
                            if ym in monthly_sum_dict.keys():
                                monthly_sum_dict[ym] = monthly_sum_dict[ym] + num * project_dict['price']
                            else:
                                monthly_sum_dict[ym] = num * project_dict['price']
                elif d['type'] == 2:
                    for timestamp, num in sub_dict.items():
                        overall_sum += num * project_dict['price']
                        dt = datetime.fromtimestamp(int(timestamp))
                        ym = dt.strftime('%Y%m')
                        if ym in monthly_sum_dict.keys():
                            monthly_sum_dict[ym] = monthly_sum_dict[ym] + num * project_dict['price']
                        else:
                            monthly_sum_dict[ym] = num * project_dict['price']
        monthly_sum = sorted(monthly_sum_dict.items(), key=lambda x: x[0])
        if 'pid' in d:
            dt = datetime.fromtimestamp(d['start_time'])
            start_ym = dt.strftime('%Y%m')
        else:
            start_ym = monthly_sum[0][0]
        dt = datetime.fromtimestamp(time.time())
        end_ym = dt.strftime('%Y%m')
        ym_list = []
        sum_list = []
        for ym in range(int(start_ym), int(end_ym) + 1):
            if 1 <= int(str(ym)[-2:]) <= 12:
                ym_list.append(ym)
                sum_list.append(monthly_sum_dict[str(ym)] if str(ym) in monthly_sum_dict else 0)
        monthly_sum = [ym_list, sum_list]
        return overall_sum, monthly_sum

    @staticmethod
    def get_project_dict(pid):
        dproject = DProject()
        project = dproject.get_project({"pid": pid})
        return project.to_dict()

    @staticmethod
    def get_region_distribution(project_dict):
        # Returns region_dist: [region_list, ratio_list].
        region_dist_dict = {}
        for uid, sub_dict in project_dict['donate_history'].items():
            user_dict = Statistics.get_user_dict(uid)
            region = user_dict['region']
            user_sum = 0
            for timestamp, num in sub_dict.items():
                user_sum += num * project_dict['price']
            user_ratio = user_sum / project_dict['price'] / project_dict['current_num']
            if region in region_dist_dict.keys():
                region_dist_dict[region] = region_dist_dict[region] + user_ratio
            else:
                region_dist_dict[region] = user_ratio
        region_dist = sorted(region_dist_dict.items(), key=lambda x: x[1], reverse=True)
        region_list, ratio_list = zip(*region_dist)
        region_dist = [region_list, ratio_list]
        return region_dist

    @staticmethod
    def get_user_dict(uid):
        duser = DUser()
        user = duser.get_user({"uid": uid})
        return user.to_dict()
