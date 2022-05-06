from Common.common import rid2region
from DataBase.models import DProject
from DataBase.models import DUser
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time


class Statistics(object):
    @staticmethod
    def fold_data(data, threshold=0.04):
        # Takes: [key_list, value_list]
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
    def get_briefing_page(lines, page_number):
        y = 0.05 * len(lines) + 0.45
        fig = plt.figure()
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        for line in lines:
            fig.text(0.1, y, line, fontsize=14, ha='left', va='center')
            y -= 0.1
        return fig

    @staticmethod
    def get_monthly_sum(d):
        # Get overall and monthly sum of donation.
        # For project: from start_time to this month.
        # For user: from first donation to this month.
        # Takes: project_dict or user_dict
        # Returns: overall_sum, [year-month_list, sum_list]
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
    def get_monthly_sum_page(monthly_sum, page_number):
        x_iter = range(len(monthly_sum[0]))
        fig = plt.figure()
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.grid(axis='y')
        for x, y in zip(x_iter, monthly_sum[1]):
            plt.text(x, y, round(y, 2), ha='center', va='bottom')
        plt.title('Monthly Donation')
        plt.xticks(x_iter, monthly_sum[0], rotation=30)
        plt.ylabel('/GBP')
        plt.bar(x_iter, monthly_sum[1])
        return fig

    @staticmethod
    def get_progress(project_dict):
        # Get monthly progress of a project.
        # Returns: [year-month_list, progress_list]
        overall_sum, monthly_sum = Statistics.get_monthly_sum(project_dict)
        current_sum = 0
        progress = []
        for i in range(len(monthly_sum[1])):
            current_sum += monthly_sum[1][i]
            progress.append(current_sum / project_dict['total_num'] / project_dict['price'])
        progress = [monthly_sum[0], progress]
        return progress

    @staticmethod
    def get_progress_page(progress, page_number):
        x_iter = range(len(progress[0]))
        fig = plt.figure()
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.grid(True)
        for x, y in zip(x_iter, progress[1]):
            plt.text(x, y, round(y, 2), ha='left', va='top')
        plt.title('Project Progress')
        plt.xticks(x_iter, progress[0], rotation=30)
        plt.ylim(-0.1, 1.1)
        plt.plot(x_iter, progress[1])
        return fig

    @staticmethod
    def get_project_dict(pid):
        dproject = DProject()
        project = dproject.get_project({'pid': pid})
        return project.to_dict()

    @staticmethod
    def get_project_report(pid):
        # Save report to local directory.
        # Returns: full filename
        d = Statistics.get_project_dict(pid)
        filename = 'p_' + d['pid'] + '.pdf'
        pp = PdfPages('DOC/' + filename)
        overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
        progress = Statistics.get_progress(d)
        regional_dist = Statistics.fold_data(Statistics.get_regional_dist(d))
        page_number = 1

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- Project Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)

        lines = ['Project:    ' + (d['title'] if len(d['title']) <= 36 else d['title'][:36] + '...'),
                 'Charity:    ' + d['charity'],
                 'Location:    ' + rid2region(d['region']),
                 'Meal Price:    ' + str(round(d['price'], 2)) + ' GBP',
                 'Progress:    ' + str(round(overall_sum, 2)) + ' / '
                 + str(round(d['total_num'] * d['price'], 2)) + ' GBP '
                 + '(' + str(round(progress[1][-1] * 100, 2)) + '%)',
                 'Period:    ' + datetime.fromtimestamp(d['start_time']).strftime('%Y/%m/%d') + ' - '
                 + datetime.fromtimestamp(d['end_time']).strftime('%Y/%m/%d'),
                 'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')]
        pp.savefig(Statistics.get_briefing_page(lines, page_number))
        page_number += 1
        pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number))
        page_number += 1
        pp.savefig(Statistics.get_progress_page(progress, page_number))
        page_number += 1
        pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number))
        page_number += 1

        plt.close('all')
        pp.close()
        return filename

    @staticmethod
    def get_regional_dist(d):
        # Get regional distribution of donation.
        # Takes: project_dict or user_dict
        # Returns: [region_list, ratio_list]
        regional_dist_dict = {}
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                user_dict = Statistics.get_user_dict(uid)
                region = rid2region(user_dict['region'])
                user_num_sum = 0
                for timestamp, num in sub_dict.items():
                    user_num_sum += num
                user_ratio = user_num_sum / d['current_num']
                if region in regional_dist_dict.keys():
                    regional_dist_dict[region] += user_ratio
                else:
                    regional_dist_dict[region] = user_ratio
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
                        if region in regional_dist_dict.keys():
                            regional_dist_dict[region] += user_sum
                        else:
                            regional_dist_dict[region] = user_sum
                for key in regional_dist_dict.keys():
                    regional_dist_dict[key] = regional_dist_dict[key] / projects_sum
            else:
                overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
                for pid, sub_dict in d['donate_history'].items():
                    project_dict = Statistics.get_project_dict(pid)
                    region = rid2region(project_dict['region'])
                    project_num_sum = 0
                    for timestamp, num in sub_dict.items():
                        project_num_sum += num
                    project_ratio = project_num_sum * project_dict['price'] / overall_sum
                    if region in regional_dist_dict.keys():
                        regional_dist_dict[region] += project_ratio
                    else:
                        regional_dist_dict[region] = project_ratio
        regional_dist = sorted(regional_dist_dict.items(), key=lambda x: x[1], reverse=True)
        region_list, ratio_list = zip(*regional_dist)
        regional_dist = [region_list, ratio_list]
        return regional_dist

    @staticmethod
    def get_regional_dist_page(regional_dist, page_number):
        fig = plt.figure()
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.title('Regional Distribution of Donation')
        plt.pie(regional_dist[1], labels=regional_dist[0], autopct='%.2f%%')
        return fig

    @staticmethod
    def get_user_dict(uid):
        duser = DUser()
        user = duser.get_user({'uid': uid})
        return user.to_dict()

    @staticmethod
    def get_user_report(uid):
        # Save report to local directory.
        # Returns: full filename
        d = Statistics.get_user_dict(uid)
        filename = 'u_' + d['uid'] + '.pdf'
        pp = PdfPages('DOC/' + filename)
        overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
        regional_dist = Statistics.fold_data(Statistics.get_regional_dist(d))
        page_number = 1

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- ' + ('Charity' if d['type'] == 1 else 'Guest') + ' Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)

        lines = ['User:    ' + d['name'],
                 'Email:    ' + d['mail'],
                 'Location:    ' + rid2region(d['region']),
                 'Currency:    ' + d['currency_type'],
                 'Total Donation:    ' + str(round(overall_sum, 2)) + ' GBP',
                 'Registration Date:    ' + datetime.fromtimestamp(d['regis_time']).strftime('%Y/%m/%d'),
                 'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')]
        pp.savefig(Statistics.get_briefing_page(lines, page_number))
        page_number += 1
        pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number))
        page_number += 1
        pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number))
        page_number += 1

        # Project section
        if d['type'] == 1:
            for pid in d['project']:
                if pid not in d['donate_history']:
                    continue
                project_dict = Statistics.get_project_dict(pid)
                overall_sum, monthly_sum = Statistics.get_monthly_sum(project_dict)
                progress = Statistics.get_progress(project_dict)
                regional_dist = Statistics.fold_data(Statistics.get_regional_dist(project_dict))

                lines = ['Project:    ' + (project_dict['title'] if len(project_dict['title']) <= 36 else
                                           project_dict['title'][:36] + '...'),
                         'Meal Price:    ' + str(round(project_dict['price'], 2)) + ' GBP',
                         'Progress:    ' + str(round(overall_sum, 2)) + ' / '
                         + str(round(project_dict['total_num'] * project_dict['price'], 2)) + ' GBP '
                         + '(' + str(round(progress[1][-1] * 100, 2)) + '%)',
                         'Period:    ' + datetime.fromtimestamp(project_dict['start_time']).strftime('%Y/%m/%d') + ' - '
                         + datetime.fromtimestamp(project_dict['end_time']).strftime('%Y/%m/%d')]
                pp.savefig(Statistics.get_briefing_page(lines, page_number))
                page_number += 1
                pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number))
                page_number += 1
                pp.savefig(Statistics.get_progress_page(progress, page_number))
                page_number += 1
                pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number))
                page_number += 1
        plt.close('all')
        pp.close()
        return filename
