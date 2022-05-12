from Common.common import currency2cid, EXCHANGE_RATE, rid2region
from DataBase.models import DProject, DUser, PROJECT_STATUS
import datetime as dt
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time


class Statistics(object):
    # This class contains a number of functions for computing statistical data and generating report.

    @staticmethod
    def fold_pie(data, window=0.5):
        # Fold the last fractions of pie into a whole.
        # Takes: [key_list, value_list]
        value_sum = 0
        sum_of_others = 0
        f_key = []
        f_value = []
        for n in range(len(data[0])):
            value_sum += data[1][n]
            if value_sum > window:
                break
        for i in range(len(data[0])):
            if i <= n:
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
            user_currency = d['currency_type']
            for pid, sub_dict in d['donate_history'].items():
                project_dict = Statistics.get_project_dict(pid)
                owner_dict = Statistics.get_user_dict(project_dict['uid'])
                project_currency = owner_dict['currency_type']
                exchange_rate = EXCHANGE_RATE[currency2cid(user_currency)] / EXCHANGE_RATE[currency2cid(project_currency)]
                if d['type'] == 1:
                    for uid, sub_sub_dict in sub_dict.items():
                        for timestamp, num in sub_sub_dict.items():
                            overall_sum += num * project_dict['price']
                            ym = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m')
                            if ym in monthly_sum_dict.keys():
                                monthly_sum_dict[ym] += num * project_dict['price'] * exchange_rate
                            else:
                                monthly_sum_dict[ym] = num * project_dict['price'] * exchange_rate
                else:
                    for timestamp, num in sub_dict.items():
                        overall_sum += num * project_dict['price']
                        ym = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m')
                        if ym in monthly_sum_dict.keys():
                            monthly_sum_dict[ym] += num * project_dict['price'] * exchange_rate
                        else:
                            monthly_sum_dict[ym] = num * project_dict['price'] * exchange_rate
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
    def get_monthly_sum_page(monthly_sum, page_number, text, currency_type):
        # Generate monthly sum page out of monthly_sum.
        x_iter = range(len(monthly_sum[0]))
        fig = plt.figure()
        plt.grid(axis='y')
        plt.subplots_adjust(bottom=0.4)
        for x, y in zip(x_iter, monthly_sum[1]):
            plt.text(x, y, round(y, 2), ha='center', va='bottom')
        fig.text(0.1, 0.15, text, fontsize=12, ha='left', va='center')
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.title('Monthly Donation')
        plt.xticks(x_iter, monthly_sum[0], rotation=45)
        plt.ylabel('/' + currency_type)
        plt.bar(x_iter, monthly_sum[1])
        return fig

    @staticmethod
    def get_num_sum(d):
        # Return sum of donation (times) and donated meals.
        donation_sum = 0
        num_sum = 0
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                for timestamp, num in sub_dict.items():
                    donation_sum += 1
                    num_sum += num
        else:
            if d['type'] == 1:
                for pid, sub_dict in d['donate_history'].items():
                    for uid, sub_sub_dict in sub_dict.items():
                        for timestamp, num in sub_sub_dict.items():
                            donation_sum += 1
                            num_sum += num
            else:
                for pid, sub_dict in d['donate_history'].items():
                    for timestamp, num in sub_dict.items():
                        donation_sum += 1
                        num_sum += num
        return donation_sum, num_sum

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
    def get_progress_page(progress, page_number, text):
        # Generate progress page out of progress.
        x_iter = range(len(progress[0]))
        fig = plt.figure()
        plt.grid(True)
        plt.subplots_adjust(bottom=0.4)
        for x, y in zip(x_iter, progress[1]):
            plt.text(x, y, round(y, 2), ha='left', va='top')
        fig.text(0.1, 0.15, text, fontsize=12, ha='left', va='center')
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.title('Project Progress')
        plt.xticks(x_iter, progress[0], rotation=45)
        plt.ylim(-0.1, 1.1)
        plt.plot(x_iter, progress[1])
        return fig

    @staticmethod
    def get_project_dict(pid):
        # Return project_dict of the project with given pid.
        project = DProject.get_project({'pid': pid})
        project_owner = DUser.get_user({'uid': project.uid})
        return project.to_dict(currency_type=project_owner.currency_type)

    @staticmethod
    def get_project_report(pid):
        # Save report to local directory.
        # Returns: full filename
        d = Statistics.get_project_dict(pid)
        filename = 'p_' + d['pid'] + '.pdf'
        pp = PdfPages('DOC/' + filename)
        currency_type = Statistics.get_user_dict(d['uid'])['currency_type']
        overall_sum = 0
        progress = [[], [0]]
        donation_sum, num_sum = Statistics.get_num_sum(d)
        if d['donate_history']:
            overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
            progress = Statistics.get_progress(d)
            regional_dist = Statistics.fold_pie(Statistics.get_regional_dist(d))
        project_age = time.time() - (d['end_time'] if progress[1][-1] >= 1 else d['start_time'])
        if progress[1][-1] != 0:
            finish_time = project_age / progress[1][-1] + d['start_time']
            finish_day = datetime.fromtimestamp(finish_time).strftime('%Y/%m/%d')
        page_number = 1

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- Project Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)

        text = 'Project:    ' + (d['title'] if len(d['title']) <= 36 else d['title'][:36] + '...') + '\n\n' + \
               'Charity:    ' + d['charity'] + '\n\n' + \
               'Location:    ' + rid2region(d['region']) + '\n\n' + \
               'Meal Price:    ' + str(round(d['price'], 2)) + ' ' + currency_type + '\n\n' + \
               'Progress:    ' + str(round(overall_sum, 2)) + ' / ' + str(round(d['total_num'] * d['price'], 2)) + ' '\
               + currency_type + ' (' + str(round(progress[1][-1] * 100, 2)) + '%)\n\n' + \
               'Period:    ' + datetime.fromtimestamp(d['start_time']).strftime('%Y/%m/%d') + ' - ' \
               + datetime.fromtimestamp(d['end_time']).strftime('%Y/%m/%d') + '\n\n' + \
               'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')
        fig = plt.figure()
        fig.text(0.1, 0.5, text, fontsize=14, ha='left', va='center')
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        pp.savefig(fig)
        page_number += 1
        if d['donate_history']:
            text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', ' \
                   + str(len(d['donate_history'])) + ' donors have donated ' + str(round(overall_sum, 2)) + ' ' \
                   + currency_type + '\n\n(' + str(num_sum) + ' meals) to this project, which is ' \
                   + str(round(overall_sum / len(d['donate_history']), 2)) + ' ' + currency_type + ' (' \
                   + str(round(num_sum / len(d['donate_history']), 2)) + ' meals)\n\nper person.'
            pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number, text, currency_type))
            page_number += 1
            text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') \
                   + ', this project has completed ' + str(round(progress[1][-1] * 100, 2)) + '% in ' \
                   + str(round(project_age / 86400)) + '\n\ndays, '
            if progress[1][-1] == 0:
                text += 'don\'t give up just yet! You are about to make the\n\nworld a little better!'
            elif progress[1][-1] == 1:
                text += 'congratulations!\n\nYou have made the world a little\n\nbetter!'
            else:
                text += 'estimated finish day is ' + finish_day + '. Keep up the good\n\nwork!'
            pp.savefig(Statistics.get_progress_page(progress, page_number, text))
            page_number += 1
            text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', donors from ' \
                   + str(len(regional_dist[0])) + ' countries (regions) have\n\ndonated to this project.'
            pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number, text))
            page_number += 1

        plt.close('all')
        pp.close()
        return filename

    @staticmethod
    def get_project_title(user_dict):
        # Return titles of a user's projects.
        title = []
        for pid, sub_dict in user_dict['donate_history'].items():
            title.append(Statistics.get_project_dict(pid)['title'])
        return title

    @staticmethod
    def get_regional_dist(d, dist=True):
        # Get regional distribution of donation.
        # Takes: project_dict or user_dict
        # Returns: [region_list, ratio_list]
        regional_dist_dict = {}
        if 'pid' in d:
            for uid, sub_dict in d['donate_history'].items():
                if uid == "Anonymous":
                    region = 'Anonymous donor'
                else:
                    user_dict = Statistics.get_user_dict(uid)
                    region = rid2region(user_dict['region'])
                user_num_sum = 0
                for timestamp, num in sub_dict.items():
                    user_num_sum += num
                if dist:
                    user_ratio = user_num_sum / d['current_num']
                else:
                    user_ratio = user_num_sum
                if region in regional_dist_dict.keys():
                    regional_dist_dict[region] += user_ratio
                else:
                    regional_dist_dict[region] = user_ratio
        else:
            if d['type'] == 1:
                charity_sum = 0
                for pid, sub_dict in d['donate_history'].items():
                    project_dict = Statistics.get_project_dict(pid)
                    charity_sum += project_dict['current_num'] * project_dict['price']
                    for uid, sub_sub_dict in sub_dict.items():
                        if uid == "Anonymous":
                            region = 'Anonymous donor'
                        else:
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
                    if dist:
                        regional_dist_dict[key] = regional_dist_dict[key] / charity_sum
                    else:
                        regional_dist_dict[key] = regional_dist_dict[key]
            else:
                overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
                for pid, sub_dict in d['donate_history'].items():
                    project_dict = Statistics.get_project_dict(pid)
                    region = rid2region(project_dict['region'])
                    project_num_sum = 0
                    for timestamp, num in sub_dict.items():
                        project_num_sum += num
                    if dist:
                        project_ratio = project_num_sum * project_dict['price'] / overall_sum
                    else:
                        project_ratio = project_num_sum * project_dict['price']
                    if region in regional_dist_dict.keys():
                        regional_dist_dict[region] += project_ratio
                    else:
                        regional_dist_dict[region] = project_ratio
        regional_dist = sorted(regional_dist_dict.items(), key=lambda x: x[1], reverse=True)
        region_list, ratio_list = zip(*regional_dist)
        regional_dist = [region_list, ratio_list]
        return regional_dist

    @staticmethod
    def get_regional_dist_page(regional_dist, page_number, text):
        # Generate regional distribution page out of regional_dist.
        fig = plt.figure()
        plt.subplots_adjust(bottom=0.2)
        fig.text(0.1, 0.125, text, fontsize=12, ha='left', va='center')
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        plt.title('Regional Distribution of Donation')
        plt.pie(regional_dist[1], labels=regional_dist[0], autopct='%.2f%%')
        return fig

    @staticmethod
    def get_user_dict(uid):
        # Return user_dict of the user with given uid.
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
        currency_type = d['currency_type']
        overall_sum = 0
        donation_sum, num_sum = Statistics.get_num_sum(d)
        if d['donate_history']:
            overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
            regional_dist = Statistics.fold_pie(Statistics.get_regional_dist(d))
        page_number = 1

        fig = plt.figure()
        fig.text(0.5, 0.55,
                 'Food For All by Apex08',
                 fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.4,
                 '- ' + ('Charity' if d['type'] == 1 else 'Donor') + ' Report -',
                 fontsize=16, ha='center', va='center')
        pp.savefig(fig)

        text = 'User:    ' + d['name'] + '\n\n' + \
               'Email:    ' + d['mail'] + '\n\n' + \
               'Location:    ' + rid2region(d['region']) + '\n\n' + \
               'Currency:    ' + currency_type + '\n\n' + \
               'Total Donation:    ' + str(round(overall_sum, 2)) + ' ' + currency_type + '\n\n' + \
               'Registration Date:    ' + datetime.fromtimestamp(d['regis_time']).strftime('%Y/%m/%d') + '\n\n' + \
               'Report Date:    ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d')
        fig = plt.figure()
        fig.text(0.1, 0.5, text, fontsize=14, ha='left', va='center')
        fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
        pp.savefig(fig)
        page_number += 1
        if d['donate_history']:
            if d['type'] == 1:
                n_donor = 0
                for pid in d['donate_history']:
                    project_dict = Statistics.get_project_dict(pid)
                    n_donor += len(project_dict['donate_history'])
                text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', ' + str(n_donor) \
                       + ' donors have donated ' + str(round(overall_sum, 2)) + ' ' + currency_type + '\n\n(' \
                       + str(num_sum) + ' meals) to your projects, which is ' + str(round(overall_sum / n_donor, 2)) \
                       + ' ' + currency_type + ' (' + str(round(num_sum / n_donor, 2)) + ' meals)\n\nper person.'
            else:
                text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', you have donated ' \
                       + str(round(overall_sum, 2)) + ' ' + currency_type + '\n\n(' + str(num_sum) + ' meals) to ' \
                       + str(len(d['donate_history'])) + ' projects, which is ' \
                       + str(round(overall_sum / len(d['donate_history']), 2)) + ' ' + currency_type + ' (' \
                       + str(round(num_sum / len(d['donate_history']), 2)) + ' meals)\n\nper project.'
            pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number, text, currency_type))
            page_number += 1
            if d['type'] == 1:
                text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', donors from ' \
                       + str(len(regional_dist[0])) + ' countries (regions) have\n\ndonated to your projects.'
            else:
                text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', you have donated to ' \
                       'projects from ' + str(len(regional_dist[0])) + '\n\ncountries (regions).'
            pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number, text))
            page_number += 1

        # Project section
        if d['type'] == 1:
            for pid in d['project']:
                project_dict = Statistics.get_project_dict(pid)
                if project_dict['status'] == PROJECT_STATUS['prepare']:
                    continue
                overall_sum = 0
                progress = [[], [0]]
                donation_sum, num_sum = Statistics.get_num_sum(project_dict)
                if project_dict['donate_history']:
                    overall_sum, monthly_sum = Statistics.get_monthly_sum(project_dict)
                    progress = Statistics.get_progress(project_dict)
                    regional_dist = Statistics.fold_pie(Statistics.get_regional_dist(project_dict))
                project_age = time.time() - (project_dict['end_time'] if progress[1][-1] >= 1 else
                                             project_dict['start_time'])
                if progress[1][-1] != 0:
                    finish_time = project_age / progress[1][-1] + project_dict['start_time']
                    finish_day = datetime.fromtimestamp(finish_time).strftime('%Y/%m/%d')

                text = 'Project:    ' + (project_dict['title'] if len(project_dict['title']) <= 36 else
                                         project_dict['title'][:36] + '...') + '\n\n' + \
                       'Meal Price:    ' + str(round(project_dict['price'], 2)) + ' ' + currency_type + '\n\n' + \
                       'Progress:    ' + str(round(overall_sum, 2)) + ' / ' \
                       + str(round(project_dict['total_num'] * project_dict['price'], 2)) + ' ' + currency_type \
                       + ' (' + str(round(progress[1][-1] * 100, 2)) + '%)\n\n' + \
                       'Period:    ' + datetime.fromtimestamp(project_dict['start_time']).strftime('%Y/%m/%d') + ' - ' \
                       + datetime.fromtimestamp(project_dict['end_time']).strftime('%Y/%m/%d') + '\n\n'
                fig = plt.figure()
                fig.text(0.1, 0.5, text, fontsize=14, ha='left', va='center')
                fig.text(0.95, 0.05, page_number, fontsize=10, ha='center', va='center')
                pp.savefig(fig)
                page_number += 1
                if d['donate_history']:
                    text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', ' \
                           + str(len(project_dict['donate_history'])) + ' donors have donated ' \
                           + str(round(overall_sum, 2)) + ' ' + currency_type + '\n\n(' + str(num_sum) \
                           + ' meals) to this project, which is ' \
                           + str(round(overall_sum / len(project_dict['donate_history']), 2)) + ' ' + currency_type \
                           + ' (' + str(round(num_sum / len(project_dict['donate_history']), 2)) \
                           + ' meals)\n\nper person.'
                    pp.savefig(Statistics.get_monthly_sum_page(monthly_sum, page_number, text, currency_type))
                    page_number += 1
                    text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') \
                           + ', this project has completed ' + str(round(progress[1][-1] * 100, 2)) + '% in ' \
                           + str(round(project_age / 86400)) + '\n\ndays, '
                    if progress[1][-1] == 0:
                        text += 'don\'t give up just yet! You are about to make the\n\nworld a little better!'
                    elif progress[1][-1] == 1:
                        text += 'congratulations!\n\nYou have made the world a little\n\nbetter!'
                    else:
                        text += 'estimated finish day is ' + finish_day + '. Keep up the good\n\nwork!'
                    pp.savefig(Statistics.get_progress_page(progress, page_number, text))
                    page_number += 1
                    text = 'Up to ' + datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d') + ', donors from ' \
                           + str(len(regional_dist[0])) + ' countries (regions) have\n\ndonated to this project.'
                    pp.savefig(Statistics.get_regional_dist_page(regional_dist, page_number, text))
                    page_number += 1
        plt.close('all')
        pp.close()
        return filename

# --------------------------
# Add other functions below.
# --------------------------

    @staticmethod
    def get_history(d):
        series = []
        money_state = []
        for pid, sub_dict in d['donate_history'].items():
            sum_num = {}
            price = Statistics.get_project_dict(pid)['price']
            for uid, u_his in sub_dict.items():
                for timestamp, num in u_his.items():
                    day = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m%d')
                    if day in sum_num.keys():
                        sum_num[day] += num * price
                    else:
                        sum_num[day] = num * price

            end_ym = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
            end_ym = datetime(int(end_ym[:4]), int(end_ym[4:6]), int(end_ym[6:]))
            start = Statistics.get_latest(d)
            delta = dt.timedelta(days=1)
            history = []
            while start < end_ym:
                money = sum_num[str(start.strftime('%Y%m%d'))] if str(start.strftime('%Y%m%d')) in sum_num else 0
                if money == 0:
                    history.append("")
                    money_state.append(0)
                else:
                    history.append("%.2f" % money)
                    money_state.append(money)
                start += delta
            data = {
                'name': Statistics.get_project_dict(pid)['title'],
                'type': 'bar',
                'stack': 'total',
                'label': {
                    'show': 'true'
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': history
            }
            series.append(data)
        return series, sum(money_state), sum(money_state[-30:]), sum(money_state[-60:-30])

    @staticmethod
    def get_latest(d):
        latest = 2147483648
        for pid, no_matter in d['donate_history'].items():
            start = Statistics.get_project_dict(pid)['start_time']
            if start < latest:
                latest = start
        latest = datetime.fromtimestamp(latest).strftime('%Y%m%d')
        return datetime(int(latest[:4]), int(latest[4:6]), int(latest[6:]))

    @staticmethod
    def get_time_line(d):
        time_line = []
        start = Statistics.get_latest(d)
        end_ym = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        end_ym = datetime(int(end_ym[:4]), int(end_ym[4:6]), int(end_ym[6:]))
        delta = dt.timedelta(days=1)
        while start < end_ym:
            time_line.append(start.strftime('%Y/%m/%d'))
            start += delta
        return time_line

    @staticmethod
    def get_monthly_progress(d):
        series = []
        for pid, sub_dict in d['donate_history'].items():
            sum_num = {}
            for uid, u_his in sub_dict.items():
                for timestamp, num in u_his.items():
                    day = datetime.fromtimestamp(int(timestamp)).strftime('%Y%m%d')
                    if day in sum_num.keys():
                        sum_num[day] += num
                    else:
                        sum_num[day] = num

            end_ym = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
            end_ym = datetime(int(end_ym[:4]), int(end_ym[4:6]), int(end_ym[6:]))
            start = Statistics.get_latest(d)
            delta = dt.timedelta(days=1)
            current_num = 0
            progress = []
            finished = False
            while start < end_ym:
                current_num += sum_num[str(start.strftime('%Y%m%d'))] if str(start.strftime('%Y%m%d')) in sum_num else 0
                if current_num == 0 or finished:
                    progress.append("")
                elif current_num == Statistics.get_project_dict(pid)['total_num']:
                    progress.append(100)
                    finished = True
                else:
                    # progress.append(current_num)
                    progress.append("%.2f" % (current_num / Statistics.get_project_dict(pid)['total_num'] * 100))
                start += delta
            data = {
                'name': Statistics.get_project_dict(pid)['title'],
                'type': 'line',
                'data': progress
            }
            series.append(data)
        return series
