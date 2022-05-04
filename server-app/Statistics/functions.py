from Common.common import rid2region
from DataBase.models import DProject
from DataBase.models import DUser
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time


class Statistics(object):
    @staticmethod
    def fold_pie(data, threshold=0.04):
        # Takes [[key], [value]].
        f_key = []
        f_value = []
        sum_of_others = 0
        for i in range(len(data[0])):
            if data[1][i] >= threshold:
                f_key.append(data[0][i])
                f_value.append(data[1][i])
            else:
                sum_of_others += data[1][i]
        if sum_of_others:
            f_key.append('Others')
            f_value.append(sum_of_others)
        f_data = [f_key, f_value]
        return f_data

    @staticmethod
    def get_completeness(project_dict):
        # Get monthly completeness of a project.
        # Returns completeness: [year-month_list, completeness_list].
        overall_sum, monthly_sum = Statistics.get_donation_sum(project_dict)
        current_sum = 0
        completeness = []
        for i in range(len(monthly_sum[1])):
            current_sum += monthly_sum[1][i]
            completeness.append(current_sum / project_dict['total_num'] / project_dict['price'])
        completeness = [monthly_sum[0], completeness]
        return completeness

    @staticmethod
    def get_donation_sum(d):
        # Get overall and monthly sum of donation.
        # For project: from start_time to this month. For user: from first donation to this month.
        # Takes project_dict or user_dict.
        # Returns overall_sum: int, monthly_sum: [year-month_list, sum_list].
        overall_sum = 0
        monthly_sum_dict = {}
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                for timestamp, num in sub_dict.items():
                    overall_sum += num * d['price']
                    ym = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m')
                    if ym in monthly_sum_dict.keys():
                        monthly_sum_dict[ym] += num * d['price']
                    else:
                        monthly_sum_dict[ym] = num * d['price']
        else:
            for pid, sub_dict in d['donate_history'].items():
                price = Statistics.get_project_dict(pid)['price']
                if d['type'] == 1:
                    for uid, sub_sub_dict in sub_dict.items():
                        for timestamp, num in sub_sub_dict.items():
                            overall_sum += num * price
                            ym = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m')
                            if ym in monthly_sum_dict.keys():
                                monthly_sum_dict[ym] += num * price
                            else:
                                monthly_sum_dict[ym] = num * price
                else:
                    for timestamp, num in sub_dict.items():
                        overall_sum += num * price
                        ym = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m')
                        if ym in monthly_sum_dict.keys():
                            monthly_sum_dict[ym] += num * price
                        else:
                            monthly_sum_dict[ym] = num * price
        monthly_sum = sorted(monthly_sum_dict.items(), key=lambda x: x[0])
        if 'pid' in d:
            start_ym = datetime.fromtimestamp(d['start_time']).strftime('%Y%m')
        else:
            start_ym = monthly_sum[0][0]
        end_ym = datetime.fromtimestamp(time.time()).strftime('%Y%m')
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
        project = dproject.get_project({'pid': pid})
        return project.to_dict()

    @staticmethod
    def get_project_report(pid):
        d = Statistics.get_project_dict(pid)
        file_name = d['pid'] + '.pdf'
        pp = PdfPages('DOC/report/' + file_name)
        overall_sum, monthly_sum = Statistics.get_donation_sum(d)
        completeness = Statistics.get_completeness(d)
        region_dist = Statistics.fold_pie(Statistics.get_region_distribution(d))

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- Project Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)
        plt.close()

        lines = ['Project:    ' + (d['title'] if len(d['title']) <= 36 else d['title'][:36] + '...'),
                 'Charity:    ' + d['charity'],
                 'Location:    ' + rid2region(d['region']),
                 'Meal Price:    ' + str(round(d['price'], 2)) + ' GBP',
                 'Progress:    ' + str(round(overall_sum, 2)) + ' / '
                 + str(round(d['total_num'] * d['price'], 2)) + ' GBP '
                 + '(' + str(round(completeness[1][-1] * 100, 2)) + '%)',
                 'Period:    ' + datetime.fromtimestamp(d['start_time']).strftime('%Y/%m/%d') + ' - '
                 + datetime.fromtimestamp(d['end_time']).strftime('%Y/%m/%d'),
                 'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')]
        y = 0.05 * len(lines) + 0.45
        fig = plt.figure()
        fig.text(0.95, 0.05, '1', fontsize=10, ha='center', va='center')
        for line in lines:
            fig.text(0.1, y, line, fontsize=14, ha='left', va='center')
            y -= 0.1
        pp.savefig(fig)
        plt.close()

        x_iter = range(len(monthly_sum[0]))
        fig = plt.figure()
        fig.text(0.95, 0.05, '2', fontsize=10, ha='center', va='center')
        plt.grid(axis='y')
        for x, y in zip(x_iter, monthly_sum[1]):
            plt.text(x, y, round(y, 2), ha='center', va='bottom')
        plt.title('Monthly Donation')
        plt.xticks(x_iter, monthly_sum[0], rotation=30)
        plt.ylabel('/GBP')
        plt.bar(x_iter, monthly_sum[1])
        pp.savefig(fig)
        plt.close()

        x_iter = range(len(completeness[0]))
        fig = plt.figure()
        fig.text(0.95, 0.05, '3', fontsize=10, ha='center', va='center')
        plt.grid(True)
        for x, y in zip(x_iter, completeness[1]):
            plt.text(x, y, round(y, 2), ha='left', va='top')
        plt.title('Project Completeness')
        plt.xticks(x_iter, completeness[0], rotation=30)
        plt.ylim(-0.1, 1.1)
        plt.plot(x_iter, completeness[1])
        pp.savefig(fig)
        plt.close()

        fig = plt.figure()
        fig.text(0.95, 0.05, '4', fontsize=10, ha='center', va='center')
        plt.title('Source Location Distribution')
        plt.pie(region_dist[1], labels=region_dist[0], autopct='%.2f%%')
        pp.savefig(fig)
        plt.close()
        pp.close()
        return file_name

    @staticmethod
    def get_region_distribution(d):
        # Get region distribution of donation.
        # Returns region_dist: [region_list, ratio_list].
        region_dist_dict = {}
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                user_dict = Statistics.get_user_dict(uid)
                region = rid2region(user_dict['region'])
                user_num_sum = 0
                for timestamp, num in sub_dict.items():
                    user_num_sum += num
                user_ratio = user_num_sum / d['current_num']
                if region in region_dist_dict.keys():
                    region_dist_dict[region] += user_ratio
                else:
                    region_dist_dict[region] = user_ratio
        else:
            if d['type'] == 1:
                projects_sum = 0
                for pid, sub_dict in d['donate_history'].items():
                    project_dict = Statistics.get_project_dict(pid)
                    projects_sum += project_dict['current_num'] * project_dict['price']
                    for uid, sub_sub_dict in sub_dict.items():
                        user_dict = Statistics.get_user_dict(uid)
                        region = rid2region(user_dict['region'])
                        user_sum = 0
                        for timestamp, num in sub_sub_dict.items():
                            user_sum += num * project_dict['price']
                        if region in region_dist_dict.keys():
                            region_dist_dict[region] += user_sum
                        else:
                            region_dist_dict[region] = user_sum
                for key in region_dist_dict.keys():
                    region_dist_dict[key] = region_dist_dict[key] / projects_sum
            else:
                overall_sum, monthly_sum = Statistics.get_donation_sum(d)
                for pid, sub_dict in d['donate_history'].items():
                    project_dict = Statistics.get_project_dict(pid)
                    region = rid2region(project_dict['region'])
                    project_num_sum = 0
                    for timestamp, num in sub_dict.items():
                        project_num_sum += num
                    project_ratio = project_num_sum * project_dict['price'] / overall_sum
                    if region in region_dist_dict.keys():
                        region_dist_dict[region] += project_ratio
                    else:
                        region_dist_dict[region] = project_ratio
        region_dist = sorted(region_dist_dict.items(), key=lambda x: x[1], reverse=True)
        region_list, ratio_list = zip(*region_dist)
        region_dist = [region_list, ratio_list]
        return region_dist

    @staticmethod
    def get_user_dict(uid):
        duser = DUser()
        user = duser.get_user({'uid': uid})
        return user.to_dict()

    @staticmethod
    def get_user_report(uid):
        d = Statistics.get_user_dict(uid)
        file_name = d['uid'] + '.pdf'
        pp = PdfPages('DOC/report/' + file_name)
        overall_sum, monthly_sum = Statistics.get_donation_sum(d)
        region_dist = Statistics.fold_pie(Statistics.get_region_distribution(d))

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- ' + ('Charity' if d['type'] == 1 else 'Guest') + ' Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)
        plt.close()

        lines = ['User:    ' + d['name'],
                 'Email:    ' + d['mail'],
                 'Location:    ' + rid2region(d['region']),
                 'Currency:    ' + d['currency_type'],
                 'Total Donation:    ' + str(round(overall_sum, 2)) + ' GBP',
                 'Registration Date:    ' + datetime.fromtimestamp(d['regis_time']).strftime('%Y/%m/%d'),
                 'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')]
        y = 0.05 * len(lines) + 0.45
        fig = plt.figure()
        fig.text(0.95, 0.05, '1', fontsize=10, ha='center', va='center')
        for line in lines:
            fig.text(0.1, y, line, fontsize=14, ha='left', va='center')
            y -= 0.1
        pp.savefig(fig)
        plt.close()

        x_iter = range(len(monthly_sum[0]))
        fig = plt.figure()
        fig.text(0.95, 0.05, '2', fontsize=10, ha='center', va='center')
        plt.grid(axis='y')
        for x, y in zip(x_iter, monthly_sum[1]):
            plt.text(x, y, round(y, 2), ha='center', va='bottom')
        plt.title('Monthly Donation')
        plt.xticks(x_iter, monthly_sum[0], rotation=30)
        plt.ylabel('/GBP')
        plt.bar(x_iter, monthly_sum[1])
        pp.savefig(fig)
        plt.close()

        fig = plt.figure()
        fig.text(0.95, 0.05, '3', fontsize=10, ha='center', va='center')
        plt.title('Source Location Distribution' if d['type'] == 1 else 'Target Location Distribution')
        plt.pie(region_dist[1], labels=region_dist[0], autopct='%.2f%%')
        pp.savefig(fig)
        plt.close()

        # Project briefing
        if d['type'] == 1:
            page_number = 4
            for pid in d['project']:
                d = Statistics.get_project_dict(pid)
                overall_sum, monthly_sum = Statistics.get_donation_sum(d)
                completeness = Statistics.get_completeness(d)

                lines = ['Project:    ' + (d['title'] if len(d['title']) <= 36 else d['title'][:36] + '...'),
                         'Meal Price:    ' + str(round(d['price'], 2)) + ' GBP',
                         'Progress:    ' + str(round(overall_sum, 2)) + ' / '
                         + str(round(d['total_num'] * d['price'], 2)) + ' GBP '
                         + '(' + str(round(completeness[1][-1] * 100, 2)) + '%)',
                         'Period:    ' + datetime.fromtimestamp(d['start_time']).strftime('%Y/%m/%d') + ' - '
                         + datetime.fromtimestamp(d['end_time']).strftime('%Y/%m/%d')]
                y = 0.05 * len(lines) + 0.45
                fig = plt.figure()
                fig.text(0.95, 0.05, str(page_number), fontsize=10, ha='center', va='center')
                for line in lines:
                    fig.text(0.1, y, line, fontsize=14, ha='left', va='center')
                    y -= 0.1
                pp.savefig(fig)
                plt.close()

                page_number += 1
        pp.close()
        return file_name
