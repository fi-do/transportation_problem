import numpy as np
import math as magic


# Todo: -Improve algorithm to calculate unequal demand and supply vectors
#       -Implement the ability to solve a tp with more stages than one
#       -Add MODI method
#       -Helper function for calculating transport amount
#       -Building useful class
#       -Implement tests
#       -Finding python style guides to improve code
#       -Exception handling

class Solver(object):

    def __init__(self, s_v, d_v, c_m):
        self.supply_vector = s_v
        self.demand_vector = d_v
        self.cost_matrix = c_m
        self.transport_matrix = np.zeros((s_v.size, d_v.size))

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

        total_costs = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs

    def cm_rule(self):
        s_v_tmp = np.copy(self.supply_vector)
        d_v_tmp = np.copy(self.demand_vector)
        t_m_tmp = np.copy(self.transport_matrix)

        columns = list(range(0, d_v_tmp.size))
        rows = list(range(0, s_v_tmp.size))
        infinity = magic.inf

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
                # print("Demand is bigger", amount)
            else:
                amount = d_v_tmp[j]
                # print("Supply  is bigger", amount)

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0:
                rows.remove(i)

            if d_v_tmp[j] == 0:
                columns.remove(j)

        total_costs = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs

    def __costs(self, transport_matrix):

        tmp = np.multiply(transport_matrix, self.cost_matrix)

        return tmp.sum()


def main():
    supply_vector = np.array([20, 40, 30])
    demand_vector = np.array([20, 20, 20, 15, 15])
    cost_matrix = np.array([[10, 15, 9, 13, 12],
                            [11, 30, 4, 13, 12],
                            [12, 13, 4, 1, 122]])

    # Debug
    print("Debug")

    problem = Solver(supply_vector, demand_vector, cost_matrix)

    # Test column minima rule
    matrix, costs = problem.cm_rule()
    print("Column Minima Rule")
    print("Matrix: \n ", matrix)
    print("Total costs: ", costs)

    # Test north west corner rule
    matrix, costs = problem.nwc_rule()
    print("North West Corner Rule")
    print("Matrix: \n", matrix)
    print("Total costs: ", costs)




if __name__ == "__main__":
    main()
