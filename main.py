import numpy as np
import math


# Todo: -Calulcate costs in each method(or seperate cost calculation in own function)
#       -Improve algorithm to calculate unequal demand and supply vectors
#       -Add column minima method
#       -Add MODI method
#       -Helper function for calculating transport amount

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

        while j < self.demand_vector.size and i < self.supply_vector.size:
            if self.demand_vector[j] >= self.supply_vector[i]:
                amount = self.supply_vector[i]
                # print("Nachfrage größer", amount)
            else:
                amount = self.demand_vector[j]
                # print("Angebot größer", amount)

            self.demand_vector[j] = self.demand_vector[j] - amount
            self.supply_vector[i] = self.supply_vector[i] - amount
            self.transport_matrix[i][j] = amount

            if self.supply_vector[i] == 0:
                i += 1
            else:
                j += 1

        return self.transport_matrix

    def cm_rule(self):
        columns = list(range(0, self.demand_vector.size))
        rows = list(range(0, self.supply_vector.size))
        i = 0
        j = 0
        minima = 0
        infinity = math.inf

        while len(columns) > 0:
            tmp = self.cost_matrix[:, j]
            tmp = tmp.tolist()

            minima = min(tmp)
            i = tmp.index(minima)

            if i not in rows:
                tmp[i] = infinity
                minima = min(tmp)
                i = tmp.index(minima)

            if self.demand_vector[j] >= self.supply_vector[i]:
                amount = self.supply_vector[i]
                # print("Nachfrage größer", amount)
            else:
                amount = self.demand_vector[j]
                # print("Angebot größer", amount)

            self.demand_vector[j] = self.demand_vector[j] - amount
            self.supply_vector[i] = self.supply_vector[i] - amount
            self.transport_matrix[i][j] = amount

            if self.supply_vector[i] == 0:
                rows.remove(i)

            if self.demand_vector[j] == 0:
                columns.remove(j)
            print(j)

            if j

        return self.transport_matrix


def main():
    transport_matrix = np.zeros((2, 3))
    supply_vector = np.array([20, 40])
    demand_vector = np.array([20, 20, 20])
    cost_matrix = np.array([[10, 15, 9],
                            [11, 30, 4]])

    # test = OR(supply_vector, demand_vector, cost_matrix)
    test2 = OR(supply_vector, demand_vector, cost_matrix)

    # print(test.nwc_rule())

    print(test2.cm_rule())


if __name__ == "__main__":
    main()
