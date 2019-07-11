import numpy as np
import math


# Todo: -Calulcate costs in each method(or seperate cost calculation in own function)
#       -Improve algorithm to calculate unequal demand and supply vectors
#       -Add column minima method
#       -Add MODI method
#       -Helper function for calculating transport amount
#       -Building useful class

class OR(object):

    def __init__(self, s_v, d_v, c_m):
        self.supply_vector = s_v
        self.demand_vector = d_v
        self.cost_matrix = c_m
        self.transport_matrix = np.zeros((s_v.size, d_v.size))
        self.total_costs = 0


    def nwc_rule(self):
        j = 0
        i = 0
        s_v_tmp = np.copy(self.supply_vector)
        d_v_tmp = np.copy(self.demand_vector)
        t_m_tmp = np.copy(self.transport_matrix)

        while j < d_v_tmp.size and i < s_v_tmp.size:
            if d_v_tmp[j] >= s_v_tmp[i]:
                amount = s_v_tmp[i]
                # print("Demand is bigger", amount)
            else:
                amount = d_v_tmp[j]
                # print("Supply is bigger", amount)

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0:
                i += 1
            else:
                j += 1

        return t_m_tmp

    def cm_rule(self):
        s_v_tmp = np.copy(self.supply_vector)
        d_v_tmp = np.copy(self.demand_vector)
        t_m_tmp = np.copy(self.transport_matrix)

        columns = list(range(0, d_v_tmp.size))
        rows = list(range(0, s_v_tmp.size))
        infinity = math.inf

        while len(columns) > 0:

            j = min(columns)

            tmp = self.cost_matrix[:, j]
            tmp = tmp.tolist()

            minima = min(tmp)
            i = tmp.index(minima)

            while i not in rows:
                tmp[i] = infinity
                minima = min(tmp)
                i = tmp.index(minima)

            if d_v_tmp[j] >= s_v_tmp[i]:
                amount = s_v_tmp[i]
                # print("Nachfrage größer", amount)
            else:
                amount = d_v_tmp[j]
                # print("Angebot größer", amount)

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0:
                rows.remove(i)

            if d_v_tmp[j] == 0:
                columns.remove(j)

        return t_m_tmp


def main():
    supply_vector = np.array([20, 40, 30])
    demand_vector = np.array([20, 20, 20, 15, 15])
    cost_matrix = np.array([[10, 15, 9, 13, 12],
                            [11, 30, 4, 13, 12],
                            [12, 13, 4, 1, 122]])

    test = OR(supply_vector, demand_vector, cost_matrix)

    # Debug Ausgabe
    print("Column minima rule")
    print(test.cm_rule())
    print("North west corner rule")
    print(test.nwc_rule())
    print("Column minima rule")
    print(test.cm_rule())

if __name__ == "__main__":
    main()
