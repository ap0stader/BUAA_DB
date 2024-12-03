from typing import List
from utils.utils import get_place_table

week_trans = {
    1: "一", 2: "二", 3: "三", 4: "四",
    5: "五", 6: "六", 7: "日",
    "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "日": 7,
}

class ResourceManager:
    def __init__(self, data: str | List[int]):
        self.table = get_place_table() # {resource_id: resource_name}
        if type(data) == str:
            self._str = data
            self._list = self.from_str(data)
        elif type(data) == list:
            # 31:16 resource_id, 15:8 week, 7:4 day, 3:0 ti
            self._list = data
            self._str = self.from_list(data)

    def from_str(self, data: str):
        result = []
        for i in data.split(';'):
            week, day, ti, name = i.split(' ')
            week, day, ti = week[1:-2], day[2], ti[1:-1]
            weeks = week.split(',')
            resource_id = self.table[name]
            day_id = week_trans[day]
            if '-' in ti:
                ti_l, ti_r = map(int, ti.split('-'))
            else:
                ti_l = ti_r = int(ti)
            for continue_week in weeks:
                if '-' in continue_week:
                    week_l, week_r = map(int, week.split('-'))
                    for week_id in range(week_l, week_r + 1):
                        for ti_id in range(ti_l, ti_r + 1):
                            result.append((resource_id << 16) | (week_id << 8) | (day_id << 4) | ti_id)
                else:
                    week_id = int(continue_week)
                    for ti_id in range(ti_l, ti_r + 1):
                        result.append((resource_id << 16) | (week_id << 8) | (day_id << 4) | ti_id)
        return result
    
    def from_list(self, data: List[int]):
        mp = {}
        for i in data:
            j = i & 0xffff00f0
            if j not in mp:
                mp[j] = []
            mp[j].append(i)
        # print('mp:', mp)
        strs = []
        for k, v in mp.items():
            resource_id = k >> 16
            day = (k >> 4) & 0xf
            use = [[0] * 20 for _ in range(20)]
            # print(k, v)
            for i in v:
                week = (i >> 8) & 0xff
                ti = i & 0xf
                # print('week, ti: ', week, ti)
                use[week][ti] = 1
            # print('use:', use)
            mp_ = {}
            for week in range(20):
                i, j = 0, 0
                while i < 20:
                    if not use[week][i]:
                        i += 1
                        continue
                    j = i
                    while j + 1 < 20 and use[week][j + 1] == 1:
                        j += 1
                    if (i, j) not in mp_:
                        mp_[(i, j)] = []
                    mp_[(i, j)].append(week)
                    i = j + 1
            # print('mp_: ', mp_)
            for k_, weeks in mp_.items():
                l, r = k_
                i, j = 0, 0
                cur_week = []
                while i < len(weeks):
                    j = i
                    while j + 1 < len(weeks) and weeks[j + 1] == weeks[j] + 1:
                        j += 1
                    if i == j:
                        cur_week.append(str(weeks[i]))
                    else:
                        cur_week.append(f"{weeks[i]}-{weeks[j]}")
                    i = j + 1
                # print('cur_week: ', cur_week)
                week_str = ','.join(cur_week)
                # print('week_str: ', week_str)
                if l == r:
                    strs.append(f'[{week_str}周] 星期{week_trans[day]} 第{l}节 {self.table[resource_id]}')
                else:
                    strs.append(f'[{week_str}周] 星期{week_trans[day]} 第{l}-{r}节 {self.table[resource_id]}')
        # print(strs)
        return '; '.join(strs)
    
    @property
    def str(self) -> str:
        return self._str
    
    @property
    def list(self) -> List[int]:
        return self._list