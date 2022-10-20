import json
from function import *
from datetime import *

class Member():
    def __init__(self, **member_attributes):
        for attr_name, attr_value in member_attributes.items():
            setattr(self, attr_name, attr_value)

class Stats():
    def __init__(self, **stats_attributes):
        for attr_name, attr_value in stats_attributes.items():
            setattr(self, attr_name, attr_value)

class Program():

    members_file = json.load(open("members.json"))
    stats_file = json.load(open("stats.json"))

    def init_mbr(self, member):
        members_file = def_member(member.id, member.name)
        self.members_file.append(members_file)

        maj_file_json(self.members_file, "members")

    def del_mbr(self, member):
        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if mbr.id == member.id:
                index = self.members_file.index(i)
                del self.members_file[index]

                maj_file_json(self.members_file, "members")

    def add_msg(self, member):
        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if mbr.id == member.id:
                index = self.members_file.index(i)
                self.members_file[index]["messages"] += 1
                self.members_file[index]["xp"] += 100
                maj_file_json(self.members_file, "members")
                for stat in self.stats_file:
                    i = stat
                    stat = Stats(**stat)
                    index = self.stats_file.index(i)
                    actifs = self.stats_file[index]["membres_actif"]
                    x = False
                    for id in actifs:
                        if id == member.id:
                            x = True
                    if not x:
                        self.stats_file[index]["membres_actif"].append(member.id)
                        maj_file_json(self.stats_file, "stats")

        for stat in self.stats_file:
            i = stat
            stat = Stats(**stat)
            index = self.stats_file.index(i)
            self.stats_file[index]["d_msg"] += 1
            self.stats_file[index]["m_msg"] += 1
            self.stats_file[index]["y_msg"] += 1
            maj_file_json(self.stats_file, "stats")

    def stats_auto_update(self, time):
        for stat in self.stats_file:
            i = stat
            stat = Stats(**stat)

            index = self.stats_file.index(i)
            if time.day > stat.date[0]:
                msgD = stat.d_msg
                self.stats_file[index]["d_msg"] = 0

                vocalD = stat.d_vocal
                self.stats_file[index]["d_vocal"] = 0

                self.stats_file[index]["date"][0] = time.day

                maj_file_json(self.stats_file, "stats")
                return "day", msgD, vocalD
            elif time.month > stat.date[1]:
                msgM = stat.m_msg
                self.stats_file[index]["d_msg"] = 0
                self.stats_file[index]["m_msg"] = 0

                vocalM = stat.m_vocal
                self.stats_file[index]["d_vocal"] = 0
                self.stats_file[index]["m_vocal"] = 0

                self.stats_file[index]["date"][0] = time.day
                self.stats_file[index]["date"][1] = time.month

                actifs = self.stats_file[index]["membres_actif"]
                self.stats_file[index]["membres_actif"].clear()

                maj_file_json(self.stats_file, "stats")

                inactifs = []
                for mbr in self.members_file:
                    i = mbr
                    mbr = Member(**mbr)

                    if actifs.count(mbr.id) == 0:
                        inactifs.append(mbr.id)

                return "month", msgM, vocalM, inactifs
            elif time.year > stat.date[2]:
                msgY = stat.y_msg
                self.stats_file[index]["d_msg"] = 0
                self.stats_file[index]["m_msg"] = 0
                self.stats_file[index]["y_msg"] = 0

                vocalY = stat.y_vocal
                self.stats_file[index]["d_vocal"] = 0
                self.stats_file[index]["m_vocal"] = 0
                self.stats_file[index]["y_vocal"] = 0

                self.stats_file[index]["date"][0] = time.day
                self.stats_file[index]["date"][1] = time.month
                self.stats_file[index]["date"][2] = time.year

                maj_file_json(self.stats_file, "stats")
                return "year", msgY, vocalY
            else:
                return "Pas de changement", 0, 0


    def add_vocal_time(self, member, x):
        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if mbr.id == member.id:
                index = self.members_file.index(i)
                self.members_file[index]["vocal"] += 1
                self.members_file[index]["xp"] += 1
                maj_file_json(self.members_file, "members")
                for stat in self.stats_file:
                    i = stat
                    stat = Stats(**stat)
                    index = self.stats_file.index(i)
                    actifs = self.stats_file[index]["membres_actif"]
                    present = False
                    for id in actifs:
                        if id == member.id:
                            present = True
                    if not present:
                        self.stats_file[index]["membres_actif"].append(member.id)
                        maj_file_json(self.stats_file, "stats")

        if x == 0:
            for stat in self.stats_file:
                i = stat
                stat = Stats(**stat)
                index = self.stats_file.index(i)
                self.stats_file[index]["d_vocal"] += 1
                self.stats_file[index]["m_vocal"] += 1
                self.stats_file[index]["y_vocal"] += 1
                maj_file_json(self.stats_file, "stats")

    def init_mbr_xp(self, member):
        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if mbr.id == member.id:
                index = self.members_file.index(i)
                self.members_file[index]["xp"] = mbr.messages * 100

                maj_file_json(self.members_file, "members")

    def get_stats(self, member):
        for mbr in self.members_file:
            mbr = Member(**mbr)

            if mbr.id == member.id:
                vocal = calc_time(mbr.vocal)
                lvl_seuil = calc_lvl(mbr.xp)

                return mbr.messages, mbr.points, vocal, mbr.xp ,lvl_seuil

    def get_leaderboard(self):
        rang = ["1er"]
        ldb = {}
        x = 1

        for mbr in self.members_file:
            mbr = Member(**mbr)
            ldb[mbr.name] = mbr.xp
            x += 1
            rang.append(f"{x}e")
        rang.pop(x-1)

        return rang, ldb

    def get_leaderboard_game(self):
        rang = ["1er"]
        ldb = {}
        x = 1

        for mbr in self.members_file:
            mbr = Member(**mbr)
            ldb[mbr.name] = mbr.points
            x += 1
            rang.append(f"{x}e")
        rang.pop(x-1)

        return rang, ldb

    def add_point(self, gagnant):
        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if mbr.id == gagnant:
                index = self.members_file.index(i)
                self.members_file[index]["points"] += 1

                maj_file_json(self.members_file, "members")

    def testing(self):
        inactifs = []
        for stat in self.stats_file:
            i = stat
            stat = Stats(**stat)
            index = self.stats_file.index(i)
            actifs = self.stats_file[index]["membres_actif"]

        for mbr in self.members_file:
            i = mbr
            mbr = Member(**mbr)

            if actifs.count(mbr.id) == 0:
                inactifs.append(mbr.id)
        return inactifs
